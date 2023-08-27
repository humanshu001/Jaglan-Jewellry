from django.contrib import admin
from django.urls import path
from home import views

app_name='home'
urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("about",views.about , name='about'),
    path("contact",views.contact , name='contact'),
    path("buy", views.buy, name='buy'),
    path("sell", views.sell, name='sell'),
    path("exchange", views.exchange, name='exchange'),
    path("insurance", views.insurance, name='insurance'),
    path("goldloan", views.goldloan, name='goldloan'),

    # Feedback Urls
    path("feedback",views.feedback, name="feedback"),
    # All Authentication Urls
    path("register",views.register , name='register'),
    path("login", views.loginUser, name='login'),
    path("log_out", views.log_out, name='log_out'),

    # All Wishlist Urls
    path("wishlist", views.wishlist, name='wishlist'),
    path("add-to-wishlist", views.addtowishlist, name='addtowishlist'),
    path("delete-wishlist-item", views.deletewish, name='deletewish'),

    # All Shopping Urls
    path("shop",views.shop , name='shop'), 
    path("shop/<str:slug>/",views.shopproducts , name='shopproducts'), 
    path("shop/<slug:cate_slug>/<slug:pro_slug>",views.productdetail , name='productdetail'), 

    # All Cart Urls
    path("cart", views.cart, name='cart'),
    path("add-to-cart", views.addtocart, name='addtocart'),
    path("update-cart", views.updatecart, name='updatecart'),
    path("delete-cart-item", views.deletecart, name='deletecart'),
    path('checkout', views.checkout, name='checkout'),
    path('placeorder', views.placeorder, name='placeorder'),

    # All Policies Urls
    path("returnpolicy",views.returnpolicy , name='returnpolicy'),
    path("exchangepolicy",views.exchangepolicy , name='exchangepolicy'),
    path("goldloanpolicy",views.goldloanpolicy , name='goldloanpolicy'),
    path("termscondition",views.termscondition , name='termscondition'),
    path("sellpolicy",views.sellpolicy , name='sellpolicy'),
    path("insurancepolicy",views.insurancepolicy , name='insurancepolicy'),
    path("privacypolicy",views.privacypolicy , name='privacypolicy'),
    path("customersupport",views.customersupport , name='customersupport'),  
]
  