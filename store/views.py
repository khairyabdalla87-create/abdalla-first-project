from django.shortcuts import render , get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product,Category,Cartitem,Cart
from .serializers import ProductSerializer, CategorySerializer,CartItemSerializer, CartSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny, IsAdminUser
# Create your views here.

class ProductList(APIView):
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
         if self.request.method == "GET":
             return [AllowAny()]
         else:
            return [IsAdminUser()]
    def get(self,request):
        products= Product.objects.all()
        name = request.query_params.get("name")
        category = request.query_params.get("category")
        max_price = request.query_params.get("max_price")
        min_price = request.query_params.get("min_price")
        if name:
            products=products.filter(name__icontains=name)
        if category:
            products = products.filter(category_id=category)
        if max_price:
            products = products.filter(price__lte=max_price)
        if min_price:
            products = products.filter(price__gte=min_price)
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
    def post(self,request):
        serizaler = ProductSerializer(data=request.data)
        if serizaler.is_valid():
            serizaler.save()
            return Response(serizaler.data,status=201)
        else:
            return Response(
                serizaler.errors, status=400
            )

class Productdetails(APIView):
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
             if self.request.method == "GET":
                 return [AllowAny()]
             else:
                return [IsAuthenticated()]
    def get(self,request,pk):
        product= get_object_or_404(Product,pk=pk)
        serialzer = ProductSerializer(product)
        return Response(serialzer.data) 
    def put(self,request,pk):
        product = Product.objects.get(pk=pk)
        serizaler = ProductSerializer(product,data=request.data)
        if serizaler.is_valid():
            serizaler.save()
            return Response(serizaler.data)
        else:
            return Response(serizaler.errors,status=400)
    def delete(self,request,pk):
        product= Product.objects.get(pk=pk)
        product.delete()
        return Response(status=204)

class Categorylist(APIView):
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]
    
    def get(self,request):
        category = Category.objects.all()
        serilazer = CategorySerializer(category,many=True)
        return Response(serilazer.data)
    def post(self,request):
        serlizer = CategorySerializer(data=request.data)
        if serlizer.is_valid():
            serlizer.save()
            return Response(serlizer.data,status=201)
        else:
            return Response (serlizer.errors,status=400)
class Categorydetails(APIView):
    authentication_classes=[TokenAuthentication]
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        else:
            return[IsAuthenticated()]

    def get(self,request,pk):
        category= get_object_or_404(Category,pk=pk)
        serilzar = CategorySerializer(category)
        return Response(serilzar.data,status=200)
    def put(self,request,pk):
        category=Category.objects.get(pk=pk)
        serizlar= CategorySerializer(category,data=request.data)
        if serizlar.is_valid():
            serizlar.save()
            return Response(serizlar.data,status=400)
        else:
            return Response(serizlar.errors)
    def delete(self,request,pk):
        category= Category.objects.get(pk=pk)
        category.delete()
        return Response(status=204)

class Cartitemlist(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        items =Cartitem.objects.filter(cart__user=request.user)
        serilzer = CartItemSerializer(items,many=True)
        return Response (serilzer.data)
    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        product_id = request.data.get("product")
        quantity = request.data.get("quantity")
        product = get_object_or_404(Product, pk=product_id)
        if quantity > product.stock:
            return Response(
        {"error": "Not enough stock"},status=400)
        
        if quantity <= 0:
            return Response(
                {"error": "Quantity must be greater than 0"},status=400)
        item = Cartitem.objects.filter(
        cart=cart,
        product=product
            ).first()
        if item:
            item.quantity += quantity
            item.save()
        else:
            item = Cartitem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
                    )    
        seriazler = CartItemSerializer(item)
        return Response(seriazler.data, status=201)
    
class Cartitemdetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        item = get_object_or_404(
        Cartitem,
        pk=pk,
        cart__user=request.user)

        item.delete()

        return Response(
        {"message": "Item removed from cart"},
        status=200
    )
    def patch(self, request, pk):
        item = get_object_or_404(
        Cartitem,
        pk=pk,
        cart__user=request.user
        )
        quantity = int(request.data.get("quantity"))

        if quantity <= 0:
            return Response(
            {"error": "Quantity must be greater than 0"},status=400)
        item.quantity = quantity
        item.save()
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=200)
class createcart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart = Cart.objects.get_or_create(
            user=request.user
        )
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=201)
        