from django.shortcuts import redirect, render
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #kunin ung order
        order = Order.objects.get(id=pk)
        #kunin din ung order items
        items = OrderItem.objects.filter(order=pk)
        
        if request.POST:
            status = request.POST['shipping_status']
            
            #check kung true or false
            if status == "true":
                #Get the order
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
                
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            
            messages.success(request, "Shipping status Updated!")
            return redirect('home')
        
        return render(request, "payment/orders.html", {"order":order, "items":items})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')

    
def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            #check kung true or false
            now = datetime.datetime.now()
            order.update(shipped=False)
        
            messages.success(request, "Shipping status Updated!")
            return redirect('home')
        return render(request, "payment/shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            #check kung true or false
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
        
            messages.success(request, "Shipping status Updated!")
            return redirect('home')
        return render(request, "payment/not_shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')


def process_order(request):
    if request.method == 'POST':
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods()  # No parentheses here
        quantities = cart.get_quants()  # No parentheses here
        totals = cart.cart_total()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)

        # Get shipping session data
        my_shipping = request.session.get('my_shipping')

        # Get order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = (
            f"{my_shipping['shipping_address1']} \n"
            f"{my_shipping['shipping_address2']} \n"
            f"{my_shipping['shipping_city']} \n"
            f"{my_shipping['shipping_state']} \n"
            f"{my_shipping['shipping_zipcode']} \n"
            f"{my_shipping['shipping_country']}"
        )
        amount_paid = totals

        # Create order
        if request.user.is_authenticated:
            user = request.user

            # Create order
            create_order = Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid
            )
            create_order.save()

            # Add order items
            for product in cart_products:
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price

                # Get quantity
                quantity = quantities.get(str(product.id), 0)

                # Create order item
                create_order_item = OrderItem(
                    order=create_order,
                    product_id=product_id,
                    user=user,
                    quantity=quantity,
                    price=price
                )
                create_order_item.save()

            #delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    #delete the key
                    del request.session[key]
            
            # Delete  cart from database or old cart field shits
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database (old_cart field)
            current_user.update(old_cart="")
                    
            messages.success(request, "Order Placed!")
            return redirect('home')

        else:
            # Create order for guest (not logged in)
            create_order = Order(
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid
            )
            create_order.save()

            # Add order items
            for product in cart_products:
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price

                # Get quantity
                quantity = quantities.get(str(product.id), 0)

                # Create order item
                create_order_item = OrderItem(
                    order=create_order,
                    product_id=product_id,
                    quantity=quantity,
                    price=price
                )
                create_order_item.save()

            #delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    #delete the key
                    del request.session[key]
                    
                    
            
            
            messages.success(request, "Order Placed!")
            return redirect('home')

    else:
        # Handle non-POST requests
        messages.error(request, "Access Denied")
        return redirect('home')



def billing_info(request):
    if request.POST:
        #get the fucking cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        
        #Create a session with shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping #yan pocha pwede na sana ma reference sa process order umay
        
        # Check to see if user is login
        if request.user.is_authenticated:
            #Get the billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form" : billing_form}) 
        else:
            #Not login
            #Get the billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form" : billing_form}) 
        
        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form}) 
    else:
        messages.success(request, "Access Denied")
        return redirect('home')
# Create your views here.
def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
        #check out as login user
        
        #shipping user
        try:
            shipping_user = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            # Handle the case where no shipping address exists
            shipping_user = None # putang ina mo inabot ako ng 3 hours sayo
        #shipping_form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    else:
        #check out as guest
        shipping_form = ShippingForm(request.POST or None)
        
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})

def payment_success(request):
    
    return render(request, "payment/payment_success.html", {})   