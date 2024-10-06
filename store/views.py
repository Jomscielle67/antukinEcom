from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json # JavaScript Object Notation para syang Disctionary pero sa javascript
from cart.cart import Cart

def search(request):
    #Determined if they filled out the form
    if request.method == 'POST':
        searched = request.POST['searched'] #gawat search pinangalan ko, like kunin mo ung input box na may pangalan na searched.
        # Query the products DB
        searched = Product.objects.filter(Q(name__icontains= searched) | Q(description__icontains= searched)) # para maibalik basta may matched
        if not searched:
            messages.success(request, 'That product does not exist please try again.')
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})

def update_info(request):
    if request.user.is_authenticated:
        # Get the current user profile
        current_user = Profile.objects.get(user__id=request.user.id)
        
        # Try to get the current user's shipping info
        try:
            shipping_user = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            # Handle the case where no shipping address exists
            shipping_user = None # putang ina mo inabot ako ng 3 hours sayo

        # Get the original user form
        form = UserInfoForm(request.POST or None, instance=current_user)

        # Get the shipping form
        if shipping_user:
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        else:
            shipping_form = ShippingForm(request.POST or None)

        if form.is_valid() and shipping_form.is_valid():
            form.save()
            if shipping_user:
                shipping_form.save()
            else:
                # Create a new ShippingAddress if it doesn't exist
                new_shipping_address = shipping_form.save(commit=False)
                new_shipping_address.user = request.user
                new_shipping_address.save()

            messages.success(request, 'Your info has been updated!')
            return redirect('home')

        return render(request, "update_info.html", {"form": form, 'shipping_form': shipping_form})
    else:
        messages.success(request, 'You must be logged in to access that page.')
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated. Please log in again.")
                return redirect('login')
            else:
                # Handle form errors and render the form again if it's invalid
                for error in form.errors.values():
                    messages.error(request, error)
                return render(request, "update_password.html", {'form': form})  # Add this line to return the form even with errors
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})
    else:
        messages.success(request, 'You must be logged in to access that page.')
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance = current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            messages.success(request, 'User has been updated!')
            return redirect('home')
        return render(request, "update_user.html", {"user_form": user_form})
    else:
        messages.success(request, 'You must be login to access that page.')
        return redirect('home')    


def category(request, foo):
    #replace dash to space
    foo = foo.replace('-', ' ').lower()
    # grab the category from the url
    try:
        #look up the category
        category = Category.objects.get(name__iexact=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, ("That category doesn't exist."))
        return redirect('home')
    
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})
    
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product' : product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products' : products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username'] #ung nasa webpage na may name='username'
        password = request.POST['password'] #ung nasa webpage na may name= 'password'
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            #Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            #Get their saved cart from database
            saved_cart = current_user.old_cart
            #Convert database string to python dictionary
            if saved_cart:
                #Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                #add the loaded cart dictionary to our session
                #Get the cart 
                cart = Cart(request)
                #Loop thru the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            
            messages.success(request,("You have been Logged in Successfully."))
            return redirect('home')
        else:
            messages.success(request,("There was an Error, Please Try again"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been Logged out! Thanks for stopping by."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username =  form.cleaned_data['username']
            password =  form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("USERNAME CREATED! - Please fill out your User Info below."))
            return redirect('update_info')
        else:
            messages.success(request, ("whoops theres a problem registring, Please Try Again!"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})
    