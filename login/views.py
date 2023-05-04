from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from rest_framework import generics
from inventory.models import Product
from .serializers import ProductSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.decorators import method_decorator

# Create your views here.


def loginaction(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # The password entered by the user is correct
            login(request, user)
            return render(request, 'Dash.html')
        else:
            # The password entered by the user is incorrect
            error_message = "Incorrect username or password."
            context = {'error_message': error_message}
            return render(request, 'login_page.html', context)
    else:
        context = {}
        return render(request, 'login_page.html', context)

# for api Products


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProductList, self).dispatch(*args, **kwargs)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProductDetail, self).dispatch(*args, **kwargs)


# for invntory_tracking
import requests
def inventorytrackaction(request):
    api_url = 'http://localhost:8000/api/products/'
    response = requests.get(api_url)
    # products = response.json()

    # product_list = []
    # for product in products:
    #     product_dict = {
    #         'id': product['id'],
    #         'name': product['name'],
    #         'price': product['price'],
    #         'quantity': product['quantity'],
    #         'location': product['location'],
    #         'reorderpoint': product['reorderpoint'],
    #         'created_at': product['created_at'],
    #         'expirationdate': product['expirationdate'],
    #         'brand': product['brand'],
    #     }
    #     product_list.append(product_dict)
    if response.status_code == 200:
        data = response.json()
    else:
        # Handle error response
        data = []


    return render(request, 'inventorytrack.html', {'data':data})



# for user API


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserList, self).dispatch(*args, **kwargs)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = User

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserDetail, self).dispatch(*args, **kwargs)
    





