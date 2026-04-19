from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib import messages

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        #Create a session with shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        #check to see if user is logged in
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products,"quantities":quantities,"totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
        else:
             billing_form = PaymentForm()
             return render(request, "payment/billing_info.html", {"cart_products":cart_products,"quantities":quantities,"totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

    else:
      messages.success(request, "Access Denied")
      return redirect('home')

def payment_success(request):
    return render(request, "payment/payment_success.html",{})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        #Checking as logged in user
        #Shipping User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {"cart_products":cart_products,"quantities":quantities,"totals":totals, "shipping_form":shipping_form})
    else:
        #Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products":cart_products,"quantities":quantities,"totals":totals, "shipping_form":shipping_form})
    

def process_order(request):
    if request.POST:

        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        
        payment_form = PaymentForm(request.POST or None)
        #Get Shipping session Data
        my_shipping = request.session.get('my_shipping')


        #Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        phone = my_shipping['shipping_phone']
        #Create shipping address from session Info
        shipping_address = f"{my_shipping['shipping_block']}\n{my_shipping['shipping_street']}\n{my_shipping['shipping_house']}\n{my_shipping['shipping_area']}\n{my_shipping['shipping_governorate']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        #Create Order
        if request.user.is_authenticated:
            user = request.user
            #Create Order
            create_order = Order(user=user, full_name=full_name, email=email, phone=phone, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            messages.success(request,"Order Placed Successfully")
            return redirect ("home")
        else:
            #Not Logged In
            #Create Order
            create_order = Order(full_name=full_name, email=email, phone=phone, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            messages.success(request,"Order Placed Successfully")
            return redirect ("home")

    else:
        messages.success(request,"Access Denied")
        return redirect ("home")