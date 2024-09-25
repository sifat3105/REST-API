from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BookViewSet, SubmitReview, ProductReviews, CustomTokenObtainPairView, SomeProtectedView

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/<slug:product_slug>/submit-review/', SubmitReview.as_view(), name='submit-review'),
    path('products/<slug:product_slug>/reviews/', ProductReviews.as_view(), name='product-reviews'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('protected/', SomeProtectedView.as_view(), name='protected_view'),
]


