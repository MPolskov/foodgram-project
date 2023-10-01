from djoser.views import UserViewSet
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from api.pagination import CustomPagination
from .serializers import FollowSerializer
from .models import Follow

User = get_user_model()

ERROR_MSG_ADD_FOLLOW = 'Вы уже подписаны на этого пользователя!'
ERROR_MSG_DELETE_FOLLOW = 'Вы не подписаны на этого пользователя!'


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPagination

    @action(
        detail=True,
        methods=['post', 'delete']
    )
    def subscribe(self, request, id):
        user = self.request.user
        if request.method == 'POST':
            if user.follower.filter(following=id).exists():
                return Response(
                    {'errors': ERROR_MSG_ADD_FOLLOW},
                    status=status.HTTP_400_BAD_REQUEST
                )
            author = get_object_or_404(User, id=id)
            serializer = FollowSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(
                user=user,
                following=author
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        subscription = user.follower.filter(following=id)
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'errors': ERROR_MSG_DELETE_FOLLOW},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(
        detail=False,
        methods=['get'],
        pagination_class=CustomPagination
    )
    def subscriptions(self, request):
        user = self.request.user
        authors_id = user.follower.values('following')
        authors = User.objects.filter(id__in=authors_id)
        paginated_queryset = self.paginate_queryset(authors)
        serializer = FollowSerializer(
            paginated_queryset,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
