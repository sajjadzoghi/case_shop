from rest_framework import serializers

from product.models import Product, Category, ProductMedia


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    images = MediaSerializer(many=True)
    final_price = serializers.SerializerMethodField()
    voters_number = serializers.SerializerMethodField()
    rate_average = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_final_price(self, obj):
        return obj.final_price

    def get_voters_number(self, obj):
        return obj.voters_number

    def get_rate_average(self, obj):
        return obj.rate_average
