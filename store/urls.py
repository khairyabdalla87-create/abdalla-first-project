from django.urls import path
from . import views
urlpatterns = [
    path('products',views.ProductList.as_view()),
    path('products/<pk>/',views.Productdetails.as_view()),
    path('category',views.Categorylist.as_view()),
    path('category/<pk>/',views.Categorydetails.as_view())
]