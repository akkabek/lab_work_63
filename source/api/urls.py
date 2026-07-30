from rest_framework import routers

from api.views import PostViewSet, CommentViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet,'post')
router.register(r'comments', CommentViewSet,'comment')

urlpatterns = router.urls