from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from order.api.serializer import OrderItemSerializer
from order.models import OrderItem, Coupon


class AddOrderItemsView(APIView):

    def get(self, request):
        customers = OrderItem.objects.all()
        serializer = OrderItemSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print('*' * 100)
        print(request.data)
        serializer = OrderItemSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckCouponView(APIView):

    def post(self, request):
        coupon = Coupon.objects.get(code=request.data['coupon'], customers=request.user)
        if coupon:
            return Response({'amount': coupon.amount, 'code': coupon.code}, status=status.HTTP_200_OK)
        return Response({'code': ['کد واردشده معتبر نیست.']}, status=status.HTTP_406_NOT_ACCEPTABLE)
