class Cart():
    def __init__(self, request):
        self.session = request.session
        
        #Get the current session key if it exists
        cart = self.session.get('session_key')

        #If there is no session key, create one
        if 'session_key' not in self.session:
            cart = self.session['session_key'] = {}


        #Make sure that the cart is available in every site
        self.cart = cart
