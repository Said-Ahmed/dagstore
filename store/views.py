from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import viewsets

from .models import Product, Category
from .serializers import ProductListSerializer, CategorySerializer, ProductDetailSerializer


class ProductApiViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'price']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        products = super().get_queryset()
        category_slug = self.request.query_params.get('category_slug', None)

        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                products = products.filter(category=category)
            except Category.DoesNotExist:
                return Product.objects.none()

        return products

    def get_object(self):
        product = get_object_or_404(Product,
                                    uuid=self.kwargs.get('uuid'),
                                    slug=self.kwargs.get('slug'),
                                    available=True)

        return product


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer