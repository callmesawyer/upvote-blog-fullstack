from rest_framework import serializers
from django.contrib.auth import get_user_model
from blog.models import Post, Like, Comment, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'image')


class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField(allow_null=True)
    comment_count = serializers.ReadOnlyField(allow_null=True)
    top_comments = serializers.SerializerMethodField()
    author_details = serializers.SerializerMethodField()
    post_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author_details', 'title', 'body', 'created', 'like_count', 'comment_count',
                  'top_comments', 'post_likes']
        read_only_fields = ['likes', 'comments']

    def create(self, validated_data):
        validated_data['author_id'] = self.context['request'].user.id
        return Post.objects.create(**validated_data)

    def get_author_details(self, obj):
        return UserSerializer(obj.author, context=self.context).data

    def get_top_comments(self, obj):
        return CommentSerializer(obj.comments.all().order_by('-created')[:2], many=True, context=self.context).data

    def get_post_likes(self, obj):
        return LikeSerializer(obj.likes.all(), many=True, context=self.context).data


class LikeSerializer(serializers.ModelSerializer):
    author_details = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['post', 'author_details', 'created']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        new_like, created = Like.objects.get_or_create(author=validated_data['author'], post=validated_data['post'])
        if not created:
            Like.objects.filter(author=validated_data['author'], post=validated_data['post']).delete()
        return new_like

    def get_author_details(self, obj):
        return UserSerializer(obj.author, context=self.context).data


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'created']
        read_only_fields = ['author', ]

    def create(self, validated_data):
        validated_data['author_id'] = self.context['request'].user.id
        # import ipdb
        # ipdb.set_trace()
        return Comment.objects.create(**validated_data)
