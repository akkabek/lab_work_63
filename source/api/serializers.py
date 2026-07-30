from rest_framework import serializers

from posts.models import Comment, Post

class PostReadSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'image', 'caption', 'created_at',
            'likes_count', 'comments_count', 'is_liked',
        )
        read_only_fields = ('id', 'author', 'created_at')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False
        return obj.is_liked_by(request.user)


class PostWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'image', 'caption')
        read_only_fields = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created_at')
        read_only_fields = ('id', 'author', 'created_at')