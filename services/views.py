from datetime import date
from pickle import FALSE
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import ClothType, Discounds, Feedback, Payment, ServiceType, Address,OrderNumber, Orders, Status
from django.contrib import messages
from django.contrib.auth.hashers import check_password
import datetime
import time
from django.db.models import Sum

# Create your views here.


def newlaundry(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            date = datetime.datetime.now()
            clothtype = request.POST.get('clothtype')
            no = request.POST.get('noofclothes')
            noofclothes=int(no)
            servicetypes = request.POST.get('servicetype')
            ser=ServiceType.objects.get(id=servicetypes)
            cost = ser.price
            servicetyname=ser.servicetypes
            serviceid = ser.id
            statusid = int(1)
            userid = request.user.id
            
            if OrderNumber.objects.filter(userid_id=userid).exists():
                on=OrderNumber.objects.get(userid_id=userid)
                orderno=on.orders
                on.orders=int(on.orders)+1
                on.save()
                if Discounds.objects.filter(orders__lte=orderno).exists():
                    d=Discounds.objects.get(orders__lte=orderno)
                    discound=d.discounds
                    homedelivery = request.POST.get('delivery')
                    if homedelivery == "True":
                        totalcost = ((cost*noofclothes)+50)-discound
                    else:
                        totalcost = (cost*noofclothes)-discound
                else:
                    discound=0
                    homedelivery = request.POST.get('delivery')
                    if homedelivery == "True":
                        totalcost = ((cost*noofclothes)+50)-discound
                    else:
                        totalcost = (cost*noofclothes)-discound
                ord=Orders.objects.create(date=date,noofclothes=noofclothes,cost=cost,discound=discound,totalcost=totalcost,userid_id=userid,serviceid_id=serviceid,homedelivery=homedelivery,servicetypes=servicetyname,clothtype=clothtype,statusid_id=statusid)
                ord.save()
            else:
                on=OrderNumber.objects.create(userid_id=userid,orders=1)
                on.save()
                orderno=1 
                homedelivery = request.POST.get('delivery')
                if homedelivery == "True":
                    totalcost = ((cost*noofclothes)+50)
                else:
                    totalcost = (cost*noofclothes)
                ord=Orders.objects.create(date=date,noofclothes=noofclothes,cost=cost,discound=0,totalcost=totalcost,userid_id=userid,serviceid_id=serviceid,homedelivery=homedelivery,servicetypes=servicetyname,clothtype=clothtype,statusid_id=statusid)
                ord.save()

            
            return redirect('checkout')

        else:
            ctypes = ClothType.objects.all()
            stypes = ServiceType.objects.all()
            add = Address.objects.filter(userid_id=request.user.id)
            return render(request,'newlaundry.html', {'ctypes':ctypes,'stypes':stypes,'add':add})
    else:
        return redirect("/")


def checkout(request):

    order=Orders.objects.last()

    if request.method=='POST':
        if request.POST.get('delivery') =='paid':
            ordid = order.id
            p="True"
            pay = Payment.objects.create(payed=p,orderid_id=ordid)
            pay.save()
            return render(request,'transaction.html')
        elif request.POST.get('delivery') == 'cod':
            ordid = order.id
            p="False"
            pay = Payment.objects.create(payed=p,orderid_id=ordid)
            pay.save()
            return redirect('index')
    
    return render(request,'checkout.html',{'order':order})


def transaction(request):
    return render(request,'transaction.html')
    

def feedback(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            message = request.POST['message']
            uid = request.user.id
            feed = Feedback.objects.create(userid_id = uid,message = message)
            feed.save()
            messages.info(request,'Feedback Posted')
            return redirect('feedback')
        else:
            return render(request,'feedback.html')
    else:
        return redirect("/")


def orderhistory(request):
    if request.user.is_authenticated:
        if Orders.objects.filter(userid_id=request.user.id).exists():
            if Orders.objects.filter(userid_id=request.user.id,statusid_id='6'):
                hist = Orders.objects.filter(userid_id=request.user.id,statusid_id='6').order_by('date')
                return render(request,'orderhistory.html',{'hist':hist})
            else:
                return render(request,'orderhistory.html')
        else:
            return render(request,'orderhistory.html')
    else:
        return redirect("/")

def profileupdate(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            address=request.POST['address']
            if Address.objects.filter(userid_id=request.user.id).exists():
                add = Address.objects.get(userid_id=request.user.id)
                add.address=address
                add.save()
                messages.info(request,'Address updated')
                return redirect('profileupdate')
            else:
                add = Address.objects.create(userid_id=request.user.id,address=address)
                add.save()
                messages.info(request,'Address added')
                return redirect('profileupdate')
        else:
            add = Address.objects.filter(userid_id=request.user.id)
            return render(request,'profileupdate.html', {'add':add})
    else:
        return redirect("/")


def active(request):
    if request.user.is_authenticated:
        if Orders.objects.filter(userid_id=request.user.id).exists():
            if Orders.objects.filter(userid_id=request.user.id).exclude(statusid_id='6'):
                hist = Orders.objects.filter(userid_id=request.user.id).exclude(statusid_id='6')
                return render(request,'active.html',{'hist':hist})
            else:
                return render(request,'active.html')

        return render(request,'active.html')
    else:
        return redirect("/")


def changepassword(request):
    if request.user.is_staff:
        if request.method =='POST':
            cpassword = request.POST['cpassword']
            n1password = request.POST['n1password']
            n2password = request.POST['n2password']
            currentpassword = request.user.password
            if check_password(cpassword,currentpassword) == True:
                if n1password == n2password:
                    u = User.objects.get(username=request.user.username)
                    u.set_password(n1password)
                    u.save()
                    messages.info(request,'Password Changed')
                    return redirect('changepassword')
                else:
                    messages.info(request,'Password not matching')
                    return redirect('changepassword')
            else:
                messages.info(request,'Current Password Entered is Wrong')
                return redirect('changepassword')
        else:
            return render(request,'changepassword.html')
 
    elif request.user.is_authenticated:
        if request.method =='POST':
            cpassword = request.POST['cpassword']
            n1password = request.POST['n1password']
            n2password = request.POST['n2password']
            currentpassword = request.user.password

            if check_password(cpassword,currentpassword) == True:
                if n1password == n2password:
                    u = User.objects.get(username=request.user.username)
                    u.set_password(n1password)
                    u.save()
                    messages.info(request,'Password Changed')
                    return redirect('changepassword')
                else:
                    messages.info(request,'Password not matching')
                    return redirect('changepassword')
            else:
                messages.info(request,'Current Password Entered is Wrong')
                return redirect('changepassword')
        else:
            return render(request,'changepassword.html')
    else:
        return redirect("/")

def adddetails(request):
    if request.user.is_staff:
        if request.POST.get('addclothtype'):
            clothtypes = request.POST['clothtype']
            c = ClothType.objects.create(clothtypes=clothtypes)
            c.save()
            messages.info(request,'Record added')
            return redirect('adddetails')
        elif request.POST.get('addnewservice'):
            newservice = request.POST['newservice']
            price = request.POST['price']
            s = ServiceType.objects.create(servicetypes=newservice,price=price)
            s.save()
            messages.info(request,'Record added')
            return redirect('adddetails')
        return render(request,'adddetails.html')
    else:
        return redirect("/")

def reports(request):
    if request.user.is_staff:
        if request.method == 'POST':
            fromdate=request.POST['fdate']
            todate=request.POST['tdate']
            s=0
            if Orders.objects.filter(date__gte=fromdate,date__lte=todate).order_by('id'):
                ord=Orders.objects.filter(date__gte=fromdate,date__lte=todate).order_by('id')
                for orders in ord:
                    s=s+orders.totalcost
            order = Orders.objects.filter(date__gte=fromdate,date__lte=todate).order_by('id')
            messages.info(request,'Report Generated')
            return render(request,'reports.html',{'order':order,'s':s})
        else:
            return render(request,'reports.html')

def allreports(request):
        if request.user.is_staff:
            users = User.objects.filter(is_staff=False).count()
            staffs = User.objects.filter(is_staff=True).count()
            order = Orders.objects.count()
            totalcost = Orders.objects.aggregate(Sum('totalcost'))
            #listval = totalcost.values()
            return render(request,'allreports.html',{'users':users,'staffs':staffs,'order':order,'totalcost':totalcost})

def allorders(request):
    if request.user.is_staff:
        order=Orders.objects.all().order_by('date')
        return render(request,'allorders.html',{'order':order})
    

def changestatus(request):
    if request.user.is_staff:
        if request.method == 'POST':
            status=request.POST.get('statusd')
            orderid=request.POST.get('update')
            if Orders.objects.filter(id=orderid).exists():
                order = Orders.objects.get(id=orderid)
                order.statusid_id=status
                order.save()
                messages.info(request,'Status changed')
                return redirect('changestatus')
        elif Orders.objects.exclude(statusid='6'):
            order = Orders.objects.exclude(statusid='6').order_by('id')
            s=Status.objects.all()
            return render(request,'changestatus.html',{'order':order,'s':s})
        else:
            return render(request,'changestatus.html')
    else:
        return redirect("/")



def adduser(request):
    if request.user.is_staff:
        if  request.method =='POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            checks = request.POST.get('checks',False)

            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('adduser')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('adduser')
            elif checks == 'True':
                user = User.objects.create_user(username = username,  first_name = fname,  last_name = lname, password = password, email = email, is_staff = True)
                user.save()
                messages.info(request,'Staff Added')
                return redirect('adduser')
            else:
                user = User.objects.create_user(username = username,  first_name = fname,  last_name = lname, password = password, email = email)
                user.save()
                messages.info(request,'User Added')
                return redirect('adduser')
        else:
            return render(request,'adduser.html')
    else:
        return redirect("/")


def adddiscound(request):
    if request.user.is_staff:
        if request.method =='POST':
            orderno = request.POST['ordernumber']
            discound = request.POST['discound']
            dis = Discounds.objects.create(discounds = discound,orders = orderno)
            dis.save()
            messages.info(request,'Discound Added')
            return redirect('adddiscound')
        else:
            return render(request,'adddiscound.html')
    else:
        return redirect("/")


def vfeedback(request):
    if request.user.is_staff:
        feed = Feedback.objects.all()
        return render(request,'vfeedback.html',{'feed':feed})
    else:
        return redirect("/")

def unpaid(request):
    if request.user.is_staff:
        if request.method == 'POST':
            p="True"
            orderid=request.POST.get('update')
            if Payment.objects.filter(orderid_id=orderid).exists():
                pay = Payment.objects.get(orderid_id=orderid)
                pay.payed=p
                pay.save()
                messages.info(request,'Status changed')
                return redirect('unpaid')
        pay = Payment.objects.all().exclude(payed=True)
        return render(request,'unpaid.html',{'pay':pay})
    else:
        return redirect("/")


def cdelivery(request):
    if request.user.is_staff:
        if Orders.objects.filter(homedelivery=True).exclude(statusid_id='6').exists():
            for ord in Orders.objects.filter(homedelivery=True).exclude(statusid_id='6'):
                addid=ord.userid_id
                add = Address.objects.get(userid_id=addid)
                return render(request,'cdelivery.html',{'ord':ord,'add':add})
        else:
            return render(request,'cdelivery.html')
    else:
        return redirect("/")