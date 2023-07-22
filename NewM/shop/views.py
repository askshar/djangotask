from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('order', 'id')
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        parent_id = request.data.get('parent_id')
        if parent_id is not None:
            try:
                parent_category = Category.objects.get(id=parent_id)
            except Category.DoesNotExist:
                return Response({"parent_id": ["Invalid parent category ID."]}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(parent_id=parent_category)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return super().create(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        categories = request.data.get('categories', [])
        root_categories = Category.objects.filter(id__in=categories, parent_id__isnull=True)
        if root_categories.exists():
            root_category_ids = root_categories.values_list('id', flat=True)
            return Response(
                {"categories": [f"Category {cid} is a root category and cannot assigned to products." for cid in root_category_ids]},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)