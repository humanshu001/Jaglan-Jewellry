from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login,logout,authenticate 
from django.contrib import messages
from datetime import datetime
from home.models import *
from django.http.response import JsonResponse
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User
import random

# Create your views here.


# All Cart Functions
def cart(request):
    if request.user.is_anonymous:
        return redirect("/login")
    cart= Cart.objects.filter(user=request.user)
    context= {'cart': cart}
    return render(request, "cart.html", context)
def addtocart(request):
    if request.method =="POST":
        if request.user.is_authenticated:
            prod_id= int(request.POST.get('product_id'))
            product_check= Product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse({'status': "already in cart"})
                else:
                    prod_qty= int(request.POST.get("product_qty"))
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status': "add successfully"})
                    else:
                        return JsonResponse({'status': "only "+ str(product_check.quantity) + " left"})
            else:
                return JsonResponse({'status': "no such product"})
        else:
            return JsonResponse({'status': "log in to cantinue"})
    return redirect("/")  
def updatecart(request):
    if request.method =="POST":
        prod_id= request.POST.get('product_id')
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
           prod_qty= request.POST.get('product_qty') 
           cart= Cart.objects.get(product_id=prod_id, user=request.user)
           cart.product_qty= prod_qty
           cart.save()
           return JsonResponse({'status': "Updated successfully"})
    return redirect('/')
def deletecart(request):
    if request.method =="POST":
        prod_id= request.POST.get('product_id')
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
           prod_qty= request.POST.get('product_qty') 
           cartitem= Cart.objects.get(product_id=prod_id, user=request.user)
           cartitem.delete()
           return JsonResponse({'status': "deleted successfully"})
    return redirect('/')
def checkout(request):
    rawcart= Cart.objects.filter(user= request.user)
    prod_id= request.POST.get('product_id')
    for item in rawcart:
        product_qty= request.POST.get('product_qty') 
        if item.product_qty > item.product.quantity: 
            checkitem= Cart.objects.get(id= item.id)  # type: ignore
            checkitem.delete()
    userprofile= Profile.objects.filter(user=request.user).first()

    cartitems= Cart.objects.filter(user= request.user)
    total_price= 0
    for item in cartitems:
        total_price= total_price + (item.product.selling_price) * (item.product_qty)
    
    context= {'cartitems': cartitems, "total_price": total_price, "userprofile":userprofile}
    return render(request, "checkout.html", context)
def placeorder(request):
    if request.method == "POST":

        currentuser= User.objects.filter(id= request.user.id).first()

        if currentuser and not currentuser.first_name:  # Check if currentuser is not None
            currentuser.first_name = request.POST.get('firstname')
            currentuser.last_name = request.POST.get('lastname')
            currentuser.save()

        if not Profile.objects.filter(user= request.user):
            userprofile= Profile()
            userprofile.user= request.user
            userprofile.phone= request.POST.get('phone')
            userprofile.address= request.POST.get('address')
            userprofile.city= request.POST.get('city')
            userprofile.state= request.POST.get('state')
            userprofile.country= request.POST.get('country')
            userprofile.pin= request.POST.get('pin')
            userprofile.save()

        neworder= Order()
        neworder.user=  request.user
        neworder.firstname= request.POST.get('firstname')
        neworder.lastname= request.POST.get('lastname')
        neworder.email= request.POST.get('email')
        neworder.phone= request.POST.get('phone')
        neworder.address= request.POST.get('address')
        neworder.city= request.POST.get('city')
        neworder.state= request.POST.get('state')
        neworder.country= request.POST.get('country')
        neworder.pin= request.POST.get('pin')

        neworder.payment_mode= request.POST.get('payment_mode')

        cart= Cart.objects.filter(user=request.user)
        cart_total_price= 0
        for item in cart:
            cart_total_price= cart_total_price + item.product.selling_price * item.product_qty

        neworder.total_price= cart_total_price
        trackno= 'jaglan'+str(random.randint(1111111111,9999999999))
        while Order.objects.filter(tracking_no= trackno) is None:
            trackno= 'jaglan'+str(random.randint(1111111111,9999999999))

        neworder.tracking_no= trackno
        neworder.save()


        neworderitems= Cart.objects.filter(user=request.user)
        for item in neworderitems:
            Orderitem.objects.create(
                order= neworder,
                product= item.product,
                price=item.product.selling_price,
                quantity= item.product_qty
            )

            #to decrease the product quantity form available stock
            orderproduct = item.product
            orderproduct.quantity= orderproduct.quantity - item.product_qty
            orderproduct.save()


         #to clear cart
        Cart.objects.filter(user=request.user).delete()

        messages.success(request,"Your Order has been placed successfully")

    return redirect('/')

# All Authentication Functions
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, "Registration successful." )
            return redirect("/login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})
def log_out(request):
    logout(request)
    return redirect("/login")      

def loginUser(request):
     if request.method =="POST":
        username= request.POST.get("username")
        password= request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In successfully") 
            return redirect("/")
        else:
            messages.error(request, "Enter Valid Username and Password") 
            return render(request, "login.html")
     return render(request,"login.html")

# Feedback functions
def feedback(request):
    if request.method == "POST":
        user= request.user
        feedback = request.POST.get('feedback')
        feed= Feedback(user=user,feedback=feedback)
        feed.save()
        messages.success(request, 'Thankyou For Your Feedback') 
    return redirect('/')
    



# All Main Functions
def homepage(request):
    if request.user.is_anonymous:
        return redirect("/login")
    category= Category.objects.filter(status=0)
    context= {'category':category}
    return render(request, "home.html",context)
def about(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "about.html")
def contact(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')    
            phone = request.POST.get('phone')
            date= request.POST.get("date")    
            message = request.POST.get('message')
            contact = AppointmentRequest(name=name, email=email, phone=phone, preferred_date =date , message=message,)
            contact.save()
            messages.success(request, 'Appointment Booked') 
    return render(request, "contact.html")
def buy(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "buy.html")
def sell(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "sell.html")
def insurance(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "insurance.html")
def exchange(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "exchange.html")
def goldloan(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "goldloan.html")




# All Shopping Functions
def shop(request):
    if request.user.is_anonymous:
        return redirect("/login")
    category= Category.objects.filter(status=0)
    context= {'category':category}
    return render(request, "shop.html", context)
def shopproducts(request, slug):
    if(Category.objects.filter(slug=slug, status=0)):
        products = Product.objects.filter(category__slug=slug)
        category_name= Category.objects.filter(slug=slug).first()
        context = {'products':products, 'category_name': category_name}
        return render(request, "shopproducts.html", context)
    else:
        messages.warning(request, "not found")
        return redirect("shop")
def productdetail(request, cate_slug, pro_slug):
    if(Category.objects.filter(slug=cate_slug, status=0)):
        if(Product.objects.filter(slug=pro_slug, status=0)):
            products= Product.objects.filter(slug=pro_slug, status=0).first()
            category_name= Category.objects.filter(slug=cate_slug).first()
            context = {'products':products, 'category_name': category_name}
        else:
            messages.error(request, "not found")
            return redirect("/shop")
    else:
        messages.error(request, "not found")
        return redirect("/shop")
    return render(request, "productdetail.html", context)






#  All Wishlist Functions
def wishlist(request):
    if request.user.is_anonymous:
        return redirect('/login')
    wishlist= Wishlist.objects.filter(user=request.user)
    context= {'wishlist': wishlist}
    return render(request, "wishlist.html", context)
def addtowishlist(request):
    if request.method =="POST":
        prod_id= int(request.POST.get('product_id'))
        product_check= Product.objects.get(id=prod_id)
        if(product_check):
            if(Wishlist.objects.filter(user=request.user.id, product_id=prod_id)):
                return JsonResponse({'status': "Already in Wishlist"})
            else:
                Wishlist.objects.create(user=request.user, product_id= prod_id)
                return JsonResponse({'status': "Product Added to Wishlist Successfully"})
        else:
            return JsonResponse({"status": "No Such Product Found"})
    return redirect("/")
def deletewish(request):
    if request.method =="POST":
        prod_id= request.POST.get('product_id')
        if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
           wishlistitem= Wishlist.objects.get(product_id=prod_id, user=request.user)
           wishlistitem.delete()
           return JsonResponse({'status': "deleted from wishlist successfully"})
    return redirect('/')           




# All Policies functions
def returnpolicy(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "returnpolicy.html")
def exchangepolicy(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "exchangepolicy.html")
def goldloanpolicy(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "goldloanpolicy.html")
def termscondition(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "termscondition.html")
def sellpolicy(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "sellpolicy.html")
def insurancepolicy(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "insurancepolicy.html")
def privacypolicy(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "privacypolicy.html")
def customersupport(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "customersupport.html")
