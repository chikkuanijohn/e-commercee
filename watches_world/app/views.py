from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User

# Create your views here.
def watches_world_login(req):
        if 'shop' in req.session:
            return redirect(shop_home)
        if 'user' in req.session:
            return redirect(user_home)
        if req.method=='POST':
            uname=req.POST['uname']
            password=req.POST['password']
            data=authenticate(username=uname,password=password)
            if data:
                login(req,data)
                if data.is_superuser:
        
                    req.session['shop']=uname 
                    return redirect(shop_home)
                else:
                    req.session['user']=uname 
                    return redirect(user_home)
            else:
                messages.warning(req,'invalid username or password')
                return redirect(watches_world_login)  
        else:
            return render(req,'login.html')

def watches_world_logout(req):
    logout(req)
    req.session.flush() 
    return redirect(watches_world_login)
#--------------------admin----------------------
def shop_home(req):
    
    if 'shop' in req.session:
        data=Product.objects.all()
        category=Category.objects.all()
        return render(req,'shop/home.html',{'Products':data,'category':category})
    else:
       return redirect(watches_world_login)



def add_products(req) :
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            des=req.POST['descrip']
            price=req.POST['price']
            offer_price=req.POST['off_price']
            stock=req.POST['stock']
            file=req.FILES['img']
            cate=req.POST['category']
            cate=Category.objects.get(pk=cate)
            data=Product.objects.create(pid=pid,name=name,des=des,price=price,offer_price=offer_price,category=cate,stock=stock,img=file)
            data.save()
            return redirect(shop_home)
        else:
            cate=Category.objects.all()
            
            return render(req,'shop/addproduct.html',{'cate':cate})
    else:
        return redirect(watches_world_login)    
    
def edit_product(req,pid) :
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            des=req.POST['descrip']
            pprice=req.POST['price']
            offer_price=req.POST['offer_price']
            cate=req.POST['category']
            pstock=req.POST['stock']
            file=req.FILES.get('img')
            if file:
                 Product.objects.filter(pk=pid).update(pid=pid,name=name,des=des,price=pprice,offer_price=offer_price,category=cate,stock=pstock,img=file)
                 data=Product.objects.get(pk=pid)
                 data.img=file
                 data.save()
            else:
               Product.objects.filter(pk=pid).update(pid=pid,name=name,des=des,price=pprice,offer_price=offer_price,category=cate,stock=pstock,img=file)
               return redirect(shop_home)
        else:
            data=Product.objects.get(pk=pid)
            cate=Category.objects.all()
            return render(req,'shop/edit_product.html',{'data':data, 'cate':cate})

def delete_product(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)    

def add_category(req):
    if 'shop' in req.session:
        if req.method=='POST':
            c_name=req.POST['cate_name']
            c_name=c_name.lower()
            try:
                cate=Category.objects.get(Category_name=c_name)
            except:
                data=Category.objects.create(Category_name=c_name)
                data.save()
            return redirect(add_category)
        categories=Category.objects.all()
        return render(req,'shop/cate.html' ,{'cate':categories})
    else:
        return render(req,'shop/cate.html')





def view_bookings(req):
    buy=Buy.objects.all()[::-1]
    return render(req,'shop/view_bookings.html',{'view_bookings':buy})

#-------------user------------------------------
def user_home  (req)  :
    return render(req,'user/user_home.html')
def pro_dtl(req,pid):
    if 'user' in req.session:
        try:
            data=Product.objects.get(pk=pid)
        except:
            messages.warning(req,'sorry the details are not avaliable')
            return redirect(pro_dtl)  
         
        return render(req,'user/product_dtl.html',{'Products':data})
    else:
        return redirect(user_home)
    
 

def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswd)
            data.save()
        except:
            messages.warning(req,'invalid username or password')
            return redirect(register)   
        return redirect(wathes_world_login) 
    else:
        return render(req,'user/register.html') 
    

def about(req):
    return render(req,'user/about.html') 


def contact(req):
    return render(req,'user/contact.html')


def booking(req):
    user=User.objects.get(username=req.session['user'])
    buy=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/booking.html',{'booking':buy})

def cart(req):
    return render(req,'user/cart.html')

# def cart(request):
#     # Add logic to handle the cart view
#     return render(request, 'user/cart.html')




def product_view(req,pid):
       data=Product.objects.get(pk=pid)
       return render(req,'user/view_pro.html',{'product':data})

def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(user=user,product=product)
        cart.qty+=1
        cart.save()
    except:
        data=Cart.objects.create(product=product,user=user,qty=1)
        data.save()
    return redirect(view_cart)



def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})



def cart_pro_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    product=cart.product
    user=cart.user
    qty=cart.qty
    price=product.offer_price*qty
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(booking)




def pro_buy(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=product.offer_price
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(booking)





