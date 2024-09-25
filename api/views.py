from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer, ReviewSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Product, Review
from django.db import IntegrityError
from rest_framework.views import APIView
from collections import Counter



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    


class SubmitReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_slug):
        user = request.user
        product = get_object_or_404(Product, slug=product_slug)

        # Check if user has already submitted a review for this product
        review_exists = Review.objects.filter(product=product, user=user).exists()
        if review_exists:
            return Response({'error': 'You have already submitted a review for this product.'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate and save the review
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=user, product=product)
                return Response({'message': 'Review submitted successfully!'}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'A review by this user for this product already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

class ProductReviews(APIView):
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        reviews = Review.objects.filter(product=product)
        ratings = reviews.values_list('rating', flat=True)

        # Calculate average rating
        if ratings:
            rating_out_of_5 = sum(ratings) / len(ratings)
            rating_out_of_5 = round(rating_out_of_5, 1) if rating_out_of_5 not in {5, 4, 3, 2, 1} else rating_out_of_5
        else:
            rating_out_of_5 = 0

        # Count star ratings
        counter = Counter(ratings)
        total_ratings = sum(counter.values())
        star_5 = counter.get(5, 0)
        star_4 = counter.get(4, 0)
        star_3 = counter.get(3, 0)
        star_2 = counter.get(2, 0)
        star_1 = counter.get(1, 0)

        # Calculate percentage for each star rating
        def calc_percent(star_count):
            return round((star_count / total_ratings) * 100) if total_ratings > 0 else 0

        stars = {
            'star_5': star_5,
            'star_4': star_4,
            'star_3': star_3,
            'star_2': star_2,
            'star_1': star_1,
            'star_5_percent': calc_percent(star_5),
            'star_4_percent': calc_percent(star_4),
            'star_3_percent': calc_percent(star_3),
            'star_2_percent': calc_percent(star_2),
            'star_1_percent': calc_percent(star_1),
        }

        # Serialize reviews
        serialized_reviews = ReviewSerializer(reviews, many=True).data

        return Response({
            'reviews': serialized_reviews,
            'rating_out_of_5': rating_out_of_5,
            'stars': stars,
            'total_ratings': total_ratings,
        })

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth import authenticate


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class SomeProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated"})