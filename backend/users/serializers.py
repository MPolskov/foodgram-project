# from rest_framework import serializers
# from django.core import validators
# from rest_framework.validators import UniqueValidator
# from djoser.serializers import TokenCreateSerializer
# from django.contrib.auth import authenticate
# from rest_framework import serializers
# from djoser.conf import settings

# from djoser.compat import get_user_email_field_name

# from .models import CustomUser

# UNIQ_NAME_ERROR = 'Выберите другое имя пользователя'
# ERROR_REGEX_MSG = 'Имя пользователя содержит недопустимые символы'
# REGEX = r'^[\w.@+-]+\Z'


# from djoser.serializers import UserCreateSerializer



# class UserCreateSerializer(UserCreateSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ("id", "email", "username", "first_name", "last_name", "password")


# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'id',
#             'email',
#             'first_name',
#             'last_name'
#         )


# class UserCreateSerializer(serializers.Serializer):
#     email = serializers.EmailField(
#         max_length=User.EMAIL_MAX_LENGTH,
#         required=True,
#         validators=(
#             UniqueValidator(
#                 queryset=User.objects.all()
#             ),
#         )
#     )
#     username = serializers.RegexField(
#         regex=REGEX,
#         max_length=User.USERNAME_MAX_LENGTH,
#         required=True,
#         validators=(
#             validators.RegexValidator(
#                 REGEX,
#                 ERROR_REGEX_MSG
#             ),
#             UniqueValidator(
#                 queryset=User.objects.all()
#             )
#         )
#     )
#     first_name = serializers.CharField(
#         max_length=User.USERNAME_MAX_LENGTH,
#         required=True,
#     )
#     last_name = serializers.CharField(
#         max_length=User.USERNAME_MAX_LENGTH,
#         required=True,
#     )
#     password = serializers.RegexField(
#         regex=REGEX,
#         max_length=User.USERNAME_MAX_LENGTH,
#         required=True,
#         validators=(
#             validators.RegexValidator(
#                 REGEX,
#                 ERROR_REGEX_MSG),
#         )
#     )

#     class Meta:
#         model = User
#         fields = (
#             'username',
#             "id",
#             'email',
#             'first_name',
#             'last_name'
#         )

#     def validate(self, data):
#         if data['username'] == 'me':
#             raise serializers.ValidationError(
#                 UNIQ_NAME_ERROR
#             )
        
#         return data
    

# class UserTokenSerializer(serializers.Serializer):
#     email = serializers.EmailField(
#         max_length=User.EMAIL_MAX_LENGTH,
#         required=True,
#     )
#     password = serializers.CharField(required=True)

#     class Meta:
#         model = User
#         fields = ('password', 'email')


# class CustomTokenCreateSerializer(TokenCreateSerializer):

#     def validate(self, attrs):
#         password = attrs.get("password")
#         params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
#         self.user = authenticate(
#             request=self.context.get("request"), **params, password=password
#         )
#         if not self.user:
#             self.user = User.objects.filter(**params).first()
#             if self.user and not self.user.check_password(password):
#                 self.fail("invalid_credentials")
#         if self.user:
#             return attrs
#         self.fail("invalid_credentials")
