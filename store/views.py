from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product,Category
from .serializers import ProductSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
# Create your views here.

class ProductList(APIView):
    def get(self,request):
        products= Product.objects.all()
        name = request.query_params.get("name")
        category = request.query_params.get("category")
        if name:
            products=products.filter(name__icontains=name)
        if category:
            products = products.filter(category_id=category)

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