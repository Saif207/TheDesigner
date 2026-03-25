from django.shortcuts import render,redirect
from .models import Product, Category,Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
from django import forms
from django.db.models import Q

def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products': products})

def about(request):
    return render(request,'about.html') 

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # use email as username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username=email, password=password)
            login(request, user)
            messages.success(request, "Name and Password is registered - Please Fill out the User Info Below")
            return redirect('update_info')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return redirect('register')
    return render(request, 'register.html', {'form': form})    

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request,"User Has been Updated")
            return redirect("home")
        return render(request,"update_user.html",{"user_form":user_form})
    
    else:
        messages.success(request,"You Must be Logged In To Access That Page!!")
        return redirect("home")


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.error(request, "Category does not exist.")
        return redirect('home')
    

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html',{"categories":categories})


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user,request.POST)
            #Is the form vaild
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password has been Updated...")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                    return redirect('update_password')
                
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})
        
    else:
        messages.success(request, "You Must be Logged In To View This Page")
        return redirect('home')
    

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()

            messages.success(request,"Your Info Has been Updated")
            return redirect("home")
        return render(request,"update_info.html",{"form":form})
    
    else:
        messages.success(request,"You Must be Logged In To Access That Page!!")
        return redirect("home")


def search(request):
    #Check if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        #Query the Products DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
            #test for null
        if not searched:
            messages.success(request,"That Product Does Not Exist")
            return render(request, "search.html", {})
        return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})