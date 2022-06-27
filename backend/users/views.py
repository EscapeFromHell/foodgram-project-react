from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram.pagination import LimitPageNumberPagination

from .models import Subscribe, User
from .serializers import SubscriptionSerializer, TokenCreateSerializer


class TokenView(ObtainAuthToken):
    def _action(self, serializer):
        if serializer.user.is_blocked:
            return Response(
                {'errors': 'Аккаунт заблокирован!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super()._action(serializer)

    def post(self, request, *args, **kwargs):
        serializer = TokenCreateSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        user = get_object_or_404(User, email=email)
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'auth_token': f'{token}'},
            status=status.HTTP_200_OK
        )


class SubscribeViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination
    lookup_url_kwarg = 'user_id'

    def get_subscribtion_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return SubscriptionSerializer(*args, **kwargs)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        self.get_serializer
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_subscribtion_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_subscribtion_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_subscribe(self, request, author):
        if request.user == author:
            return Response(
                {'errors': 'Нельзя подписаться на себя!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            subscribe = Subscribe.objects.create(
                user=request.user,
                author=author,
            )
        except IntegrityError:
            return Response(
                {'errors': 'Нельзя подписаться дважды!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_subscribtion_serializer(subscribe.author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_subscribe(self, request, author):
        try:
            Subscribe.objects.get(user=request.user, author=author).delete()
        except Subscribe.DoesNotExist:
            return Response(
                {'errors': 'Вы не подписаны на данного пользователя!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=('post', 'delete',),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, user_id=None):
        try:
            author = get_object_or_404(User, pk=user_id)
        except Http404:
            return Response(
                {'detail': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND,
            )
        if request.method == 'POST':
            return self.create_subscribe(request, author)
        return self.delete_subscribe(request, author)
