from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Count
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from blog.models import Post, Like, Comment, CustomUser
from blog.permissions import IsOwnerOrReadOnly
from blog.serializers import PostSerializer, LikeSerializer, CommentSerializer, UserSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsOwnerOrReadOnly, ]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(like_count=Count('likes', distinct=True),
                         comment_count=Count('comments', distinct=True)).order_by('-created')
        return qs

    # def get_serializer_context(self):
    #     # import ipdb
    #     # ipdb.set_trace()
    #     return {'top_comments': 'hello'}


class LikeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     queryset = qs.filter()
    #     # import ipdb
    #     # ipdb.set_trace()
    #     return queryset


class UserListView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })
