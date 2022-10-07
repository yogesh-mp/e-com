import rest_framework.pagination
from rest_framework import permissions
from django.http import JsonResponse
from .serializers import OrdersSerializer, ProductsSerializer, GetAuthSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.authentication import TokenAuthentication
from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework import generics


class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, )
    allowed_methods = ["get", "post"]

    def get(self, request):
        response = {}
        customer = request.GET.get("customer")
        orders = Orders.objects.filter(customer__id=customer)
        order_serializer = OrdersSerializer(orders, many=True)
        if not orders:
            response["status"] = False
            response["message"] = "There are no Order history for this customer"
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
        print(orders)
        return Response(order_serializer.data)

    def post(self, request):
        response = {}
        data = dict()
        data["customer_id"] = request.data.get("customer_id")
        data["product_id"] = request.data.get("product_id")
        data["quantity"] = request.data.get("quantity")
        data["placed_date"] = datetime.now()
        order_serializer = OrdersSerializer(data=data)
        if order_serializer.is_valid():
            order_serializer.save()
            response["data"] = order_serializer.data
            response["status"] = True
            return JsonResponse(response, status=status.HTTP_200_OK)
        else:
            response["errors"] = order_serializer.errors
            response["status"] = False
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)


class ProductsView(generics.ListAPIView):
    allowed_methods = ["get"]
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    pagination_class = rest_framework.pagination.PageNumberPagination


class GetAuthKeyView(APIView):
    allowed_methods = ["get"]

    def get(self, request):
        response = dict()
        data = dict()
        data["username"] = request.GET.get("username")
        data["password"] = request.GET.get("password")
        data["customer_id"] = request.GET.get("customer")
        serializer = GetAuthSerializer(data=data)
        if serializer.is_valid():
            response["data"] = Token.objects.all().last().key
            response["status"] = True
            return JsonResponse(response, status=status.HTTP_200_OK)
        else:
            response["errors"] = serializer.errors
            response["status"] = False
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)


