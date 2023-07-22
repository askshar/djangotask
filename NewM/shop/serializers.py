from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('id', 'title', 'order', 'sub_category', 'products')

    def validate_title(self, value):
        parent_id = self.instance.parent_id if self.instance else self.initial_data.get('parent_id')
        if Category.objects.filter(title=value, parent_id=parent_id).exists():
            raise serializers.ValidationError("Category with same title already exists under the same parent.")
        return value
    
    def get_sub_category(self, category):
        subcategories = Category.objects.filter(parent_id=category)
        serializer = CategorySerializer(subcategories, many=True)
        return serializer.data
    
    def get_products(self, category):
        products = Product.objects.filter(categories=category)
        return products.values_list('id', flat=True)


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'categories')

    def validate_price(self, value):
        if value<0:
            raise serializers.ValidationError("Price can not be negative, please enter valid price.")
        return value