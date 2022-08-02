from django.shortcuts import render
from .models import Customer, Product, Cart, OrderPlaced
from django.views import View
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages

def home(request):
 topwears = Product.objects.filter(category='TW')
 bottomwears = Product.objects.filter(category='BW')
 mobiles = Product.objects.filter(category='M')
 return render(request, 'app/home.html',{'topwears':topwears ,'bottomwears':bottomwears, 'mobiles':mobiles})

def product_detail(request,pk):
 product = Product.objects.get(pk=pk)
 return render(request, 'app/productdetail.html', {'product':product})

def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

#def profile(request):
# return render(request, 'app/profile.html')

def address(request):
 address = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':address})

def orders(request):
 return render(request, 'app/orders.html')


def mobile(request,data=None):
 mobiles = Product.objects.filter(category='M')
 if data==None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
  return render(request, 'app/mobile.html',{'mobiles':mobiles})
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
  return render(request, 'app/mobile.html',{'mobiles':mobiles})
 else:
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 return render(request, 'app/mobile.html', {'mobiles': mobiles})

def login(request):
 return render(request, 'app/login.html')

#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
 def get(self, request):
  forms = CustomerRegistrationForm()
  return render(request,'app/customerregistration.html', {'form': forms})
 def post(self, request):
  forms = CustomerRegistrationForm(request.POST)
  if forms.is_valid():
   messages.success(request, "Congratulations !! Registered Successfully ")
   forms.save()
  return render(request, 'app/customerregistration.html', {'form': forms})

def checkout(request):
 return render(request, 'app/checkout.html')

class Profile(View):
 def get(self,request):
  forms = CustomerProfileForm
  return render(request,'app/profile.html', {'form':forms, 'active':'btn-primary'})
 def post(self,request):
  forms = CustomerProfileForm(request.POST)
  if forms.is_valid():
   user = request.user
   name = forms.cleaned_data['name']
   locality = forms.cleaned_data['locality']
   city = forms.cleaned_data['city']
   state = forms.cleaned_data['state']
   zipcode = forms.cleaned_data['zipcode']
   reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
   messages.success(request, "Congratulations ! Profile Updated Successfully")
   reg.save()
  return render(request,'app/profile.html',{'form':forms})