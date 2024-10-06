from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    # Get the cart
    cart = Cart(request)

    # Test for POST
    if request.method == 'POST' and request.POST.get('action') == 'post':
        # Get product ID from POST data
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        # Lookup product in the DB
        product = get_object_or_404(Product, id=product_id)

        # Save to Session
        cart.add(product=product, quantity=product_qty)

        # Lets get cart quantity
        cart_quantity = cart.__len__()
        
        # Return response with product name
        # response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'Qty': cart_quantity })
        messages.success(request, ("Product added to cart."))
        return response

    # If request is not POST, return a bad request response
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_delete(request):
    cart = Cart(request)

    # Test for POST
    if request.method == 'POST' and request.POST.get('action') == 'post':
        # Get product ID from POST data
        product_id = int(request.POST.get('product_id'))
        # Call delete Function
        cart.delete(product=product_id)
        
        response = JsonResponse ({'product' : product_id})
        messages.success(request, ("Product removed from cart."))
        return response
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_update(request):
    cart = Cart(request)

    # Test for POST
    if request.method == 'POST' and request.POST.get('action') == 'post':
        # Get product ID from POST data
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        cart.update(product=product_id, quantity=product_qty)
        
        response = JsonResponse ({'qty' :product_qty})
        messages.success(request, ("Product updated."))
        return response
        
