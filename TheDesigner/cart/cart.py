from store.models import Product,Profile


class Cart():
    def __init__(self, request):
        self.session = request.session

        #Get request
        self.request = request

        #Get the current session key if it exists
        cart = self.session.get('session_key')
        #If the user is new, ni session key! , Create one
        if 'session_key' not in request.session:
            cart= self.session['session_key'] = {}
        #Make sure cart is available on all pages of sites
        self.cart = cart

        #Make sure cart is available on all pages of site
    def db_add(self,product,quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass

        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True
        #Deal with loggedIn user
        if self.request.user.is_authenticated:
            #Get the current user Profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #convert {'3':1,'2':4} to {"3":1, "2",4}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save carty to the profile model
            current_user.update(old_cart= carty)    

    def add(self, product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass

        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True
        #Deal with loggedIn user
        if self.request.user.is_authenticated:
            #Get the current user Profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #convert {'3':1,'2':4} to {"3":1, "2",4}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save carty to the profile model
            current_user.update(old_cart= carty)

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #Get ids from cart
        product_ids = self.cart.keys()
        #Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        #returns those looked up product
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        #Get the cart
        ourcart = self.cart
        #update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True
        
        if self.request.user.is_authenticated:
                #Get the current user Profile
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                #convert {'3':1,'2':4} to {"3":1, "2",4}
                carty = str(self.cart)
                carty = carty.replace("\'","\"")
                #save carty to the profile model
                current_user.update(old_cart= carty)
        thing = self.cart
        return thing
    
    def delete(self,product):
        product_id = str(product)
        #delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified =True

        if self.request.user.is_authenticated:
                #Get the current user Profile
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                #convert {'3':1,'2':4} to {"3":1, "2",4}
                carty = str(self.cart)
                carty = carty.replace("\'","\"")
                #save carty to the profile model
                current_user.update(old_cart= carty)

    def cart_total(self):
        #Get product id
        product_ids = self.cart.keys()
        #lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        #get quantities
        quantities = self.cart
        #start counting at 0
        total = 0
        for key, value in quantities.items():
            #convert key string into int so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_Price * value)
                    else:
                        total = total + (product.price* value)
        return   total