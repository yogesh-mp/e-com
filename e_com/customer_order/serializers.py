from rest_framework import serializers
from .models import Product, Customer, Orders


class OrdersSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)
    placed_date = serializers.DateTimeField()

    custom_validated_data_dict = {}

    def validate_customer_id(self, value):
        if cus_obj := Customer.objects.filter(id=value).first():
            self.custom_validated_data_dict["customer"] = cus_obj
        else:
            raise serializers.ValidationError("Invalid Customer ID!!!")

    def validate_product_id(self, value):
        if prod_obj := Product.objects.filter(id=value).first():
            self.custom_validated_data_dict["product"] = prod_obj
        else:
            raise serializers.ValidationError("Invalid Product ID!!!")

    def create(self, validated_data):
        print("Create called")
        product = self.custom_validated_data_dict.get("product")
        quantity = product.quantity - int(validated_data.get("quantity"))
        product.quantity = quantity
        product.save()
        self.custom_validated_data_dict["quantity"] = validated_data["quantity"]
        self.custom_validated_data_dict["placed_date"] = validated_data["placed_date"]
        return Orders.objects.create(**self.custom_validated_data_dict)

    def update(self, instance, validated_data):
        return instance


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class GetAuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    customer_id = serializers.IntegerField(required=True)

    custom_validated_data_dict = {}

    def validate_customer_id(self, value):
        if cus_obj := Customer.objects.filter(id=value).first():
            self.custom_validated_data_dict["customer"] = cus_obj
        else:
            raise serializers.ValidationError("Invalid Customer ID!!!")

    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]
        cus_obj = self.custom_validated_data_dict["customer"]
        if cus_obj.user_name == username and cus_obj.password == password:
            return attrs
        raise serializers.ValidationError(
            "Provided username and password is invalid or doesn't match with Customer ID!!!")


    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance
