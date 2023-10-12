from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.pagination import CustomPagination
from .errors_msg import ERROR_MSG_DELETE_FOLLOW
from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    '''Переопределенное представление пользователя.'''

    ACTIONS_AUTH = ('me', 'subscribe', 'subscriptions')

    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in self.ACTIONS_AUTH:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    @action(
        detail=True,
        methods=['post', 'delete']
    )
    def subscribe(self, request, id):
        '''Action для подписки/отписки на автора.'''

        user = self.request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
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
        methods=['get']
    )
    def subscriptions(self, request):
        '''Action для вывода списка подписок на авторов.'''

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
