from rest_framework import routers

from api.views import PostViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet,'post')

urlpatterns = router.urls