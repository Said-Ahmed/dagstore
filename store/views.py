from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Product, Category
from .serializers import ProductListSerializer, ProductDetailSerializer


class ProductApiViewSet(viewsets.ViewSet):
    def list(self, request, category_slug=None, *args, **kwargs):
        products = Product.objects.filter(available=True)

        if category_slug:
            category = get_object_or_404(Category,slug=category_slug)
            products = products.filter(category=category)
        serializer = ProductListSerializer(products, many=True)

        return Response(
            {
                'response': serializer.data
             }, status=status.HTTP_200_OK
        )

    def retrieve(self, request, uuid, slug, *args, **kwargs):
        product = get_object_or_404(Product,
                                    uuid=uuid,
                                    slug=slug,
                                    available=True)
        serializer = ProductDetailSerializer(product)

        return Response(
            {
                'response': serializer.data
             }, status=status.HTTP_200_OK
        )

