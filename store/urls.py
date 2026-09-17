from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
urlpatterns = [
    path('products/',views.ProductList.as_view()),
    path('products/<pk>/',views.Productdetails.as_view()),
    path('category/' ,views.Categorylist.as_view()),
    path('category/<pk>/',views.Categorydetails.as_view()),
    path('token',obtain_auth_token),
    path('cart/',views.Cartitemlist.as_view()),
    path('cart/<int:pk>/', views.Cartitemdetails.as_view()),
    path('cart/create/',views.createcart.as_view())
]