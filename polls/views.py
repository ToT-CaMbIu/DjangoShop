from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Category,Brand,Product,CartItem,Cart,Order,ShopCharacteristic,Coupon
from .forms import RegistrationForm,LogingForm,OrderForm
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.conf import settings
from decimal import Decimal
from keras.models import model_from_json
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from keras import backend
import operator
import numpy as np
import time
import requests

def index(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories':categories,
        'products':products,
        'cart':cart,
    }
    return render(request, "base.html", context)

def product_view(request,product_slug):
    categories = Category.objects.all()
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    product = Product.objects.get(slug = product_slug)
    context = {
        'product':product,
        'cart':cart,
    }
    return render(request, "product.html", context)
    
def category_view(request,category_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    category = Category.objects.get(slug = category_slug)
    products_of_category = Product.objects.filter(category = category).filter(available = True)
    context = {
        'category':category,
        'products_of_category':products_of_category,
        'cart':cart,
    }
    return render(request, "category.html", context)

def cart_view(request):
    categories = Category.objects.all()
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    context = {
        'cart':cart,
    }
    flg = False
    for tmp in cart.items.all():
        if tmp.product.available is False:
            cart.final_price -= tmp.product.price
            cart.items.remove(tmp)
            flg = True

    if flg:
        cart.save()

    return render(request, "cart.html", context)

def cart_adding_view(request,product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    product = Product.objects.get(slug = product_slug)
    #return HttpResponse(f"<h2>{item_total//2}</h2>")
    #item, _ = CartItem.objects.get_or_create(product=product,item_total = product.price)
    item = CartItem.objects.create(product=product,item_total = product.price)
    for tmp in cart.items.all():
        if tmp.product.slug == item.product.slug:
            return HttpResponseRedirect('/cart/')
    if item.product.available:
        cart.items.add(item)
        #return HttpResponse(f"<h2>{cart.final_price//2}</h2>")
        cart.final_price = str(Decimal(cart.final_price) + Decimal(item.product.price))
        cart.price_before_sale = str(Decimal(cart.price_before_sale) + Decimal(item.product.price))
        if cart.is_sale:
                cart.final_price = cart.price_before_sale
                cart.is_sale = False
        cart.save()
        return HttpResponseRedirect('/cart/')
    return HttpResponseRedirect('/cart/')

def cart_deleting_view(request,product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    product = Product.objects.get(slug = product_slug)
    #item, _ = CartItem.objects.get_or_create(product=product,item_total = product.price)
    flg = False
    for tmp in cart.items.all():
        if tmp.product.slug == product.slug and tmp.product.id == product.id:
            cart.final_price = str(Decimal(cart.final_price) - Decimal(tmp.product.price)) 
            cart.price_before_sale = str(Decimal(cart.price_before_sale) - Decimal(tmp.product.price)) 
            if cart.is_sale:
                cart.final_price = cart.price_before_sale
                cart.is_sale = False
            cart.items.remove(tmp)
            flg = True
    if flg:
        cart.save()
    return HttpResponseRedirect('/cart/')

def registration_view(request):
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all()
        if form.is_valid():
            new_user = form.save(commit = False)
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            new_user.username = username
            new_user.set_password(password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.email = email
            new_user.save()
            login_user = authenticate(username=username, password=password)
            if login_user:
                login(request, login_user)
                return HttpResponseRedirect(reverse('base'))
        context = {
            'form':form,
        }
        return render(request,'registration.html',context)

def search_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    search_list = []
    categories = Category.objects.all()
    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)
        if search_query[:4] != 'url:':
            for tmp in Product.objects.all():
                if search_query.upper() in tmp.title.upper() or search_query.upper() in tmp.brand.name.upper():
                    search_list.append(tmp)
        else:
            search_query = (search_query.replace(' ',''))[4:]
            categories = [tmp.name for tmp in categories]
            categories.sort()
            backend.clear_session()
            json_file = open("/Users/kirillgrigorev/UniversityWork/7th_term/trpo/DjangoShop/neuro.json", "r")
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)
            loaded_model.load_weights("/Users/kirillgrigorev/UniversityWork/7th_term/trpo/DjangoShop/neuro.h5")
            try:
                #time.sleep(5)
                loaded_model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
                response = requests.get(search_query)
                img = Image.open(BytesIO(response.content))
                img = img.resize((224, 224))
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                x = preprocess_input(x)
                prediction = loaded_model.predict(x)
                tmp = categories[np.argmax(prediction)]
                #time.sleep(2)
                backend.clear_session()
                category = Category.objects.get(name = tmp)
                products_of_category = Product.objects.filter(category = category).filter(available = True)
                context = {
                    'category':category,
                    'products_of_category':products_of_category,
                    'cart':cart,
                }
                return render(request, "category.html", context)
                #return HttpResponse(f"<h2>{tmp}</h2>")
            except:
                return HttpResponse(f"<h2>Cannot do this operation, please, try again</h2>")

        context = {
            'search_list':search_list,
            'cart':cart,
        }
    if len(search_list) > 0:
        return render(request,'search.html',context)
    else:
        return HttpResponse("<h2>No any products with entered substring</h2>")

def loging_view(request):
    form = LogingForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))

    context = {
        'form':form,
    }
    return render(request,'login.html',context)

def coupon_usage_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    if request.method == 'GET':
        search_query = request.GET.get('coupon_box', None)
        characteristics = ShopCharacteristic.objects.get(save_id = 1)
        try:
            if Coupon.objects.get(name = search_query) and not cart.is_sale:
                #cart.final_price = VARS_OF_COUPONS_VIEW[search_query]
                cart.final_price = Coupon.objects.get(name = search_query).coupon_sale
                characteristics.total_usage_of_coupons += 1
                characteristics.save() 
                cart.is_sale = True          ###
        except:
            return HttpResponse(f"<h2>{search_query} is not correct coupon!</h2>")

    cart.save()       

    return HttpResponseRedirect('/cart/')

# def checkout_view(request):
# 	try:
# 		cart_id = request.session['cart_id']
# 		cart = Cart.objects.get(id=cart_id)
# 		request.session['total'] = cart.items.count()
# 	except:
# 		cart = Cart()
# 		cart.save()
# 		cart_id = cart.id
# 		request.session['cart_id'] = cart_id
# 		cart = Cart.objects.get(id=cart_id)
# 	categories = Category.objects.all()
# 	context = {
# 		'cart': cart,
# 	}
# 	return render(request, 'checkout.html', context)

def order_create_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	form = OrderForm(request.POST or None)
	categories = Category.objects.all()
	context = {
		'form': form,
		'cart': cart,
	}
	return render(request, 'order.html', context)

def make_order_view(request):
  try:
	  cart_id = request.session['cart_id']
	  cart = Cart.objects.get(id=cart_id)
	  request.session['total'] = cart.items.count()
  except:
	  cart = Cart()
	  cart.save()
	  cart_id = cart.id
	  request.session['cart_id'] = cart_id
	  cart = Cart.objects.get(id=cart_id)

  form = OrderForm(request.POST or None)
  categories = Category.objects.all()
  characteristics = ShopCharacteristic.objects.get(save_id = 1)
  if form.is_valid():
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    phone = form.cleaned_data['phone']
    buying_type = form.cleaned_data['buying_type']
    address = form.cleaned_data['address']
    comments = form.cleaned_data['comments']
    date = form.cleaned_data['date']

    for tmp in cart.items.all():
      if tmp.product.available and int(tmp.product.count_in_stock) <= 0:
        return HttpResponse(f"<h2>product {tmp.product.title} is no longer in stock</h2>")

    get_new_order = Order.objects.create(
			user=request.user,
			items=cart,
			total=cart.final_price,
			first_name=first_name,
			last_name=last_name,
			phone=phone,
			address=address,
			buying_type=buying_type,
			comments=comments,
      date = date
		)

    context = {
		  'order': get_new_order,
      'cart':cart,
      'key':settings.RAVE_PUBLIC_KEY,
      'amount':Decimal(cart.final_price),
	  }
    return render(request, 'payment.html', context)

  context = {
    'form': form,
		'cart': cart,
	}
  return render(request, 'order.html',context)

def account_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    order = Order.objects.filter(user=request.user).order_by('-id')
    categories = Category.objects.all()
    context = {
		  'order': order,
      'cart':cart,
	  }
    return render(request, 'account.html', context)
    
def payment_failure_view(request,order_id):
  try:
    cart_id = request.session['cart_id']
    cart = Cart.objects.get(id=cart_id)
    request.session['total'] = cart.items.count()
  except:
    cart = Cart()
    cart.save()
    cart_id = cart.id
    request.session['cart_id'] = cart_id
    cart = Cart.objects.get(id=cart_id)
  return render(request, 'payment_failure.html')

def payment_success_view(request,order_id):
  try:
    cart_id = request.session['cart_id']
    cart = Cart.objects.get(id=cart_id)
    request.session['total'] = cart.items.count()
  except:
    cart = Cart()
    cart.save()
    cart_id = cart.id
    request.session['cart_id'] = cart_id
    cart = Cart.objects.get(id=cart_id)
  order = Order.objects.get(id=int(order_id))
  order.is_accepted = True
  order.save()
  for tmp in cart.items.all():
      if tmp.product.available and int(tmp.product.count_in_stock) > 0:
          tmp.product.count_in_stock = int(tmp.product.count_in_stock) - 1
          if int(tmp.product.count_in_stock) <= 0:
              tmp.product.available = False
          tmp.product.save()
  characteristics = ShopCharacteristic.objects.get(save_id = 1)
  characteristics.total_money = str(Decimal(cart.final_price) + Decimal(characteristics.total_money))
  characteristics.save()
  Cart.objects.filter(id=cart_id).delete()
  del request.session['cart_id']
  del request.session['total']
  return render(request, 'payment_success.html')