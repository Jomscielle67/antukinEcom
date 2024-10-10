from store.models import Product, Profile

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')  # Use 'cart' key for session storage instead of 'session_key'
        if not cart:
            cart = self.session['cart'] = {}  # Initialize cart if it doesn't exist
        self.cart = cart

    # The rest of the methods remain the same


    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        
        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price' : str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True

        # Deal with login user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #convert dictionary shits {'3': 1, '4': 6} etc etc
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to Profile Model
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        
        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price' : str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True

        # Deal with login user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #convert dictionary shits {'3': 1, '4': 6} etc etc
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to Profile Model
            current_user.update(old_cart=str(carty))
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        # Get product ids from the cart
        product_ids = self.cart.keys()
        
        # Use ids to lookup products in the database
        products = Product.objects.filter(id__in=product_ids)
        
        # Return the products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        
        #Get cart
        ourcart = self.cart
        ourcart[product_id] = product_qty
        
        self.session.modified = True
        
        # Deal with login user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #convert dictionary shits {'3': 1, '4': 6} etc etc
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to Profile Model
            current_user.update(old_cart=str(carty))
            
        thing = self.cart
        return thing
    
    def delete(self, product):
    
        product_id = str(product)
        #delete from dictionary
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True
        
        # Deal with login user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #convert dictionary shits {'3': 1, '4': 6} etc etc
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to Profile Model
            current_user.update(old_cart=str(carty))
        
    def cart_total(self):
        #GET PRODUCT IDS
        product_ids = self.cart.keys()
        # look those keys in our products database model.
        products = Product.objects.filter(id__in=product_ids)
        #get quantities
        quantities = self.cart
        #start counting from 0
        total = 0
        for key, value in quantities.items():
            # Convert key string into int so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total