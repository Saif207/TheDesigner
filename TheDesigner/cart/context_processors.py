from .cart import Cart

#Create a context processor to make the cart available in every template

def cart(request):
    #Return the default data from our Cart
    return {'cart': Cart(request)}

