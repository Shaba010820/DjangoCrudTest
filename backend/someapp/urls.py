from django.urls import path, include
from .views import AuthorViewSet, BookViewSet, FavoriteViewSet, UserRegisterLoginView, IndexView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'author', AuthorViewSet, basename='author')
router.register(r'book', BookViewSet, basename='book')
router.register(r'favorite', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('api/', include(router.urls)),
    path('index/', IndexView.as_view(), name='index'),
    path('api/auth', UserRegisterLoginView.as_view(), name='sign-in')
]
