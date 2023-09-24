# from django.conf import settings
# from django.contrib.auth.tokens import default_token_generator
# # from django.core.mail import send_mail
# from django.shortcuts import get_object_or_404
# from rest_framework import permissions, status, viewsets, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.exceptions import ValidationError
# from rest_framework_simplejwt.tokens import AccessToken
# from django.db import IntegrityError
# from rest_framework.views import APIView
# from djoser.views import TokenCreateView

# # from api.permissions import IsAdministrator
# from .models import User
# from .serializers import (
#     UserSerializer,
#     UserCreateSerializer,
#     UserTokenSerializer,
#     CustomTokenCreateSerializer
# )

# VALID_ERROR = 'Такой логин или email уже существуют'
# AUTH_ERROR = 'Неверный логин или пароль'


# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('username',)
#     permission_classes = (permissions.AllowAny,)
#     lookup_field = 'username'
#     http_method_names = ['get', 'post', 'patch', 'delete']

#     @action(
#         methods=['patch', 'get'],
#         detail=False,
#         permission_classes=[permissions.IsAuthenticated]
#     )
#     def me(self, request):
#         if request.method == 'GET':
#             serializer = UserSerializer(self.request.user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         serializer = UserSerializer(
#             self.request.user,
#             data=request.data,
#             partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save(role=request.user.role, partial=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def create(self, request, *args, **kwargs):
#         serializer = UserCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             user, _ = User.objects.get_or_create(
#                 **serializer.validated_data)
#         except IntegrityError:
#             return Response(
#                 VALID_ERROR,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         user.save()
#         return_data = {
#             'username': user.username,
#             "id": user.id,
#             'email': user.email,
#             'first_name': user.first_name,
#             'last_name': user.last_name
#         }
#         return Response(data=return_data, status=status.HTTP_200_OK)

    


