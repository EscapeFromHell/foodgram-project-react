from rest_framework import serializers
from rest_framework.authtoken.models import Token

from recipes.nested import RecipeShortReadSerializer

from .models import User


class TokenCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True
    )
    email = serializers.EmailField(
        required=True
    )

    class Meta:
        model = Token
        fields = ('password', 'email')


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('is_subscribed_user')

    class Meta:
        model = User
        fields = (
            'email', 'id',  'username', 'first_name',
            'last_name', 'password', 'is_subscribed',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }

    def is_subscribed_user(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and obj.subscribing.filter(user=user).exists()
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                f'Запрещено использовать username "{value}"'
            )
        return value


class SubscriptionSerializer(UserSerializer):
    recipes = RecipeShortReadSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count',)

    def get_recipes_count(self, obj):
        return obj.recipes.count()
