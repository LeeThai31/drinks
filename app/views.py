from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from.models import *   
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def change_account(request):
    if request.user.is_authenticated:
        customer = request.user
        # Lấy và tạo order
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # Truy cập all đơn hàng đã đặt
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    categories = Category.objects.filter(is_sub=False)

    if request.method == 'POST':
        form = ChangeUserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # Xử lý sau khi thay đổi thông tin thành công
            return redirect('login')  # Điều chỉnh URL đích của bạn
    else:
        form = ChangeUserProfileForm(instance=request.user)

    context = {'form': form,
               'cartItems': cartItems,
               'user_not_login': user_not_login,
               'user_login': user_login,
               'categories': categories,
               }
    return render(request, 'app/change_account.html', context)
def profile(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
        user_info = {
            'username': customer.username,
            'email': customer.email,
            'password':customer.password,
        }
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories =  Category.objects.filter(is_sub = False)
    context={'user_info': user_info,'items':items,'order':order,'cartItems' :cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories':categories}
    return render(request,'app/profile.html',context)
def hotline(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories =  Category.objects.filter(is_sub = False)
    context={'items':items,'order':order,'cartItems' :cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories':categories}
    return render(request,'app/hotline.html',context)
def introduct(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories =  Category.objects.filter(is_sub = False)
    context={'items':items,'order':order,'cartItems' :cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories':categories}
    return render(request,'app/introduct.html',context)
def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete =False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    categories =  Category.objects.filter(is_sub = False)
    context = {'products': products,'items':items,'order':order,'cartItems' :cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories':categories}
    return render(request,'app/detail.html',context)
def category(request):
    categories =  Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
        context = {'categories':categories,'products':products,'active_category':active_category}
        return render(request,'app/category.html',context)
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    products = Product.objects.all()
    return render(request, 'app/search.html', {'rearched': searched,'keys': keys, 'products': products, 'cartItems' :cartItems,'user_not_login':user_not_login,'user_login':user_login})
def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context= {'form': form}
    return render(request, 'app/register.html', context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password =password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request,'tài khoản hoặc mật khẩu không chính xác')
            
    context= {}
    return render(request, 'app/login.html', context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories =  Category.objects.filter(is_sub = False)
    products = Product.objects.all()
    context= {'products': products, 'cartItems' :cartItems, 'user_not_login':user_not_login,'user_login':user_login,'categories':categories}
    return render(request, 'app/home.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete =False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories =  Category.objects.filter(is_sub = False)
    context = {'items':items,'order':order,'cartItems' :cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories':categories}
    return render(request,'app/cart.html',context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories =  Category.objects.filter(is_sub = False)
    context = {'items':items,'order':order,'cartItems' :cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories':categories}
    return render(request, 'app/checkout.html',context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete =False)
    orderItem, created = OrderItem.objects.get_or_create(order =order,product =product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)
