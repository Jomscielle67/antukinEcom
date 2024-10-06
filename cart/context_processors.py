from .cart import Cart

#Create context processor so our cart will work on all pages of our site
def cart(request):
    
    return {'cart': Cart(request)}  