from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from posts.models import Like, Post, Comment

from .permissions import IsAuthorOrReadOnly
from .serializers import PostReadSerializer, PostWriteSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.select_related('author').all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return PostWriteSerializer
        return PostReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()

        if request.method == 'POST':
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if not created:
                return Response({'detail': 'Публикация уже лайкнута.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {'liked': True, 'likes_count': post.likes_count},
                status=status.HTTP_201_CREATED,
            )

        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        if not deleted:
            return Response({'detail': 'Лайк не найден.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {'liked': False, 'likes_count': post.likes_count},
            status=status.HTTP_200_OK,
        )

class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.select_related('author', 'post').all()
        post_id = self.request.query_params.get('post')
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
