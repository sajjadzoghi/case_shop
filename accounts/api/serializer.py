from django.contrib.auth import get_user_model
from rest_framework import serializers

Customer = get_user_model()


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'