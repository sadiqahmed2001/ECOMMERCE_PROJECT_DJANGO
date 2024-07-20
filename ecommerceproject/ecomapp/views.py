from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Product,Cart,Order
from django.db.models import Q
import razorpay


def demo(request):
    return render(request,"demo.html")

def index(request):
    context={}
    products=Product.objects.all()
    print(products)
    context["Products"]=products
    print(request.user.is_authenticated)
    return render(request,"index.html",context)

def register(request):
    context={}
    if request.method=="POST":
        n=request.POST["name"]
        e=request.POST["email"]
        p=request.POST["password"]
        cp=request.POST["cpassword"]
        print(n,e,p,cp)

        if n=="" or e=="" or p=="" or cp=="":
            context["error_message"]="Fields Cannot be empty please fill all the fields"
            return render(request,'registration.html',context)
        elif p != cp:
            context["error_message"]="password cannot match please rewrite again"
            return render(request,'registration.html',context)
        else:
            u=User.objects.create(username=n,email=e)
            u.set_password(p)
            u.save()
            context["success"]="Registration successfully!!!!"
            return render(request,"registration.html",context)
    return render(request,"registration.html")


def ulogin(request):
    context={}
    if request.method=="POST":
        e=request.POST["uname"]
        p=request.POST["upassword"]
        print(e,p)
        if e=="" or p=="" :
            context["error_message"]="Fields Cannot be empty please fill all the fields"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=e,password=p)
            print(u)
            if u is not None:
                login(request,u)
                return redirect('/index')
            else:
                context["error_message"]="username and password not matched"
                return render(request,'login.html',context)
            
            return HttpResponse(u)

    return render(request,"login.html")


def ulogout(request):
    logout(request)
    return redirect('/index')
    return render(request,"logout.html")

def store(request):
    return render(request,"mystore.html")

def product_details(request,pid):
    context={}
    products=Product.objects.filter(id=pid)
    context["products"]=products
    return render(request,"product_details.html",context)

def filterbycategory(request,cid):
    context={}
    products=Product.objects.filter(category=int(cid))
    context["Products"]=products
    return render(request,'index.html',context)

def sortbyprice(request,sp):
    if sp=="0":
        products=Product.objects.order_by("-price").filter(is_active=True)
    else:
        products=Product.objects.order_by("price").filter(is_active=True)
    context={}
    context["Products"]=products
    return render(request,"index.html",context)

def filterbyprice(request):
    l=request.GET["minimum"]
    h=request.GET["maximum"]
    q1=Q(price__gte=l)
    q2=Q(price__lte=h)
    products=Product.objects.filter(q1&q2)
    context={'Products':products}
    return render(request,"index.html",context)

def addtocart(request,pid):
    context={}
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1&q2)
        n=len(c)
        context["products"]=p
        if n==1:
            context["msg"]="Product is already Existed"
            return render(request,'product_details.html',context)
        else:
            cart=Cart.objects.create(pid=p[0],userid=u[0])
            cart.save()
            context["msg"]="Product is add in cart successfully"
            return render(request,'product_details.html',context)
    else:
        return redirect("/login")

def viewcart(request):
    context={}
    if request.user.is_authenticated:
        c=Cart.objects.filter(userid=request.user.id)
        context["carts"]=c
        totalqty=0
        totalprice=0
        actualprice=0
        for i in c:
            totalqty=totalqty+i.qty
            totalprice=totalprice+i.qty*i.pid.price
            actualprice=actualprice+i.pid.price
        print(totalqty)
        print(totalprice)
        print(actualprice)
        context["price"]=totalprice
        context["items"]=totalqty
        context["actual"]=actualprice
        return render(request,'cart.html',context)
    else:
        return redirect("/ulogin")
    
def removecart(request,cid):
    context={}
    c=Cart.objects.filter(id=cid)
    c.delete()
    context["msg"]="cart removed successfully"
    c=Cart.objects.filter(userid=request.user.id)
    
    context["carts"]=c
    # print(c)
    return render(request,"cart.html",context)

def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    if x=="1":
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    return redirect("/viewcart")

import random
def placeorder(request):
    c=Cart.objects.filter(userid=request.user.id)
    oid=random.randint(11111,99999)
    print(oid)
    amount=0

    for x in c:
        amount=x.qty*x.pid.price
        o=Order.objects.create(order_id=oid,amt=amount,p_id=x.pid,user_id=x.userid)
        o.save()
    return redirect("/fetchorder")

def fetchorder(request):
    context={}
    orders=Order.objects.filter(user_id=request.user.id)
    context["orders"]=orders
    sum=0
    context['n']=len(orders)
    for order in orders:
        sum=order.amt
    context["total"]=sum
    print(sum)
    return render(request,"placeorder.html",context)


def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_JjQ72OskgZ3YwQ", "Wve5BMxfecpjBRVbi04U19sj"))
    context = {}
    orders = Order.objects.filter(user_id=request.user.id)
    context["orders"] = orders
    order_info = orders.aggregate(total_amount='amt', last_order_id='order_id')
    data = {
        "amount": order_info['total_amount'] * 100,
        "currency": "INR",
        "receipt": order_info['last_order_id']
    }
    payment = client.order.create(data=data)
    context["payment"] = payment
    return render(request, "pay.html", context)

    return HttpResponse("successfully")

def paymentsuccess(request):
    return HttpResponse("payment success")




