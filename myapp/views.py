import smtplib

from django.contrib import messages
from django.db.models.aggregates import Count, Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User ,Group
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime,date

# Create your views here.

def login_page(request):
    return render(request,'loginpage.html')
def logout_page(request):
    logout(request)
    return redirect('/myapp/login_page/')
def login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(request,username=username,password=password)
    if user is not None:
        print('hello')
        login(request,user)
        if user.groups.filter(name='admin').exists():
            return redirect("/myapp/admin_home/")
        elif user.groups.filter(name='customer').exists():
            return redirect('/myapp/customer_home/')
        elif user.groups.filter(name='serviceprovider').exists():

            provider = ServiceProvider.objects.get(LOGIN=user)

            if provider.status == 'pending':
                messages.warning(request, 'Please wait for admin verification')
                return redirect('/myapp/login_page/')

            elif provider.status == 'rejected':
                messages.warning(request, 'You are rejected by the admin')
                return redirect('/myapp/login_page/')

            elif provider.status == 'blocked':
                messages.warning(request, 'You are blocked by the admin')
                return redirect('/myapp/login_page/')

            elif provider.status == 'accepted':
                login(request, user)
                return redirect('/myapp/provider_home/')
            else:
                messages.warning(request,'User not found')
                return redirect('/myapp/login_page/')
    else:
        messages.warning(request,'User not found')
        return redirect('/myapp/login_page/')

        

def signupchoice(request):
    return render(request,'signupchoice.html')
@login_required(login_url='/myapp/login_page/')
def changepassword(request):
    return render(request,'changepassword.html')

def changepassword_post(request):
    currentpass=request.POST['currentpass']
    newpass=request.POST['newpass']
    confirmpass=request.POST['confirmpass']

    user=request.user
    if user.check_password(currentpass):
        if newpass == currentpass:
            messages.warning( request, 'Current password and New password cannot be Same!')
            return redirect('/myapp/changepassword/')
        elif newpass == confirmpass:
            user.set_password(newpass)
            user.save()
            logout(request)
            return redirect('/myapp/login_page')
        else:
            return redirect('/myapp/changepassword/')
    
    else:
        messages.warning(request,'wrong current password')
        return redirect('/myapp/changepassword/')

def forgot_password(request):
    return render(request,'forgot_password.html')

def forgotpassword_post(request):


    email=request.POST['email']

    if User.objects.filter(username=email).exists():

        import random
        new_pass = random.randint(0000, 9999)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("accidentdetection8@gmail.com", "kmqjfzkrdyvzkqav")  # App Password
        to = email
        subject = "Reset Password"
        body = " hello  user .Your new password is " + str(new_pass)
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail("s@gmail.com", to, msg)  # Disconnect from the server
        server.quit()

        user = User.objects.get(username=email)
        user.set_password(str(new_pass))
        user.save()

        return redirect('/myapp/login_page/')
    else:
        messages.warning(request, 'email not  exists')
        return redirect('/myapp/forgot_password/')

# =================================================CUSTOMERS==========================================================================
def customersignup(request):
    return render(request,'customer/customersignup.html')

def customersignup_post(request):
    name=request.POST['name']
    phone=request.POST['phone']
    place=request.POST['place']
    email=request.POST['email']
    dob=request.POST['dob']
    photo=request.FILES['photo']
    password=request.POST['password']

    
    today=datetime.now()
    yearofbirth= datetime.strptime(dob, "%Y-%m-%d").date()
    age=today.year-yearofbirth.year
   
    if age<18:
        messages.warning(request,'you cant register here baby come back after turning 18😗')
        return redirect('/myapp/customersignup/')
    else:

        if User.objects.filter(username=email).exists():
            messages.warning(request,'username already exists..!')
            return redirect('/myapp/customersignup/')
        else:
            a=User.objects.create_user(username=email,password=password)
            a.groups.add(Group.objects.get(name='customer'))
            
            
            ob=Customer()
            ob.name=name
            ob.place=place
            ob.dob=dob
            ob.photo=photo
            ob.email=email
            ob.phone=phone
            ob.LOGIN=a
            ob.save()
            return redirect('/myapp/login_page/')

def checkusername(request):
    email=request.GET.get('email')
    print(email,'hellooo')
    if User.objects.filter(username=email).exists():
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'no'})
    
# @login_required(login_url='/myapp/login_page/')
def customer_home(request):
    ob=Request.objects.filter(CUSTOMER__LOGIN=request.user,status='payment pending').count()
    a=Customer.objects.get(LOGIN=request.user)
    return render(request,'customer/customer_home.html',{'data':ob,'datas':a})

@login_required(login_url='/myapp/login_page/')
def manage_customer_profile(request):
    ob=Customer.objects.get(LOGIN=request.user)
    return render(request,'customer/manage_customer_profile.html',{'datas':ob})

@login_required(login_url='/myapp/login_page/')
def edit_customer_profile(request,id):
    ob=Customer.objects.get(id=id)
    return render(request,'customer/edit_customer_profile.html',{'data':ob})



def edit_customer_profile_post(request):
    name = request.POST['name']
    phone = request.POST['phone']
    place = request.POST['place']
    email = request.POST['email']
    dob = request.POST['dob']
    olddob = request.POST['olddob']
    today = date.today()
    new_dob = datetime.strptime(dob, "%Y-%m-%d").date()
    max_dob = date(today.year - 18, today.month, today.day)
    if new_dob > today:
        messages.warning(request, 'Enter a valid DOB')
        return redirect('/myapp/manage_customer_profile/')

  
    age = today.year - new_dob.year
    if (today.month, today.day) < (new_dob.month, new_dob.day):
        age -= 1

    ob = Customer.objects.get(LOGIN=request.user)

    if 'photo' in request.FILES:
        ob.photo = request.FILES['photo']
    ob.name = name
    ob.email = email
    ob.place = place
    ob.phone = phone
    if age <= 18:
        ob.dob = olddob
    else:
        ob.dob = dob
    ob.save()
    return redirect('/myapp/manage_customer_profile/')

@login_required(login_url='/myapp/login_page/')
def send_complaint(request,id):
    if Complaints.objects.filter(REQUEST_id=id).exists():
        ob=Complaints.objects.filter(REQUEST_id=id)
        return render(request,'customer/view_replay.html',{'data':ob})
    else:
        ob=Request.objects.get(id=id)
        return render(request,'customer/send_complaint.html',{'data':ob})

def send_complaint_post(request):
    rid=request.POST['rid']
    complaints=request.POST['complaints']
    if Complaints.objects.filter(CUSTOMER__LOGIN=request.user,REQUEST_id=rid):
        messages.warning(request,' Dont be oversmart brother...!🤡')
        return redirect('/myapp/request_status/')
    else:
        ob=Complaints()
        ob.REQUEST=Request.objects.get(id=rid)
        ob.CUSTOMER=Customer.objects.get(LOGIN=request.user)
        ob.date=datetime.now()
        ob.status='pending'
        ob.complaints=complaints
        ob.save()
        return redirect('/myapp/request_status/')
    

# ==================================================SERVICE PROVIDER=========================================================        
def provider_signup(request):
    return render(request,'serviceprovider/provider_signup.html')

def provider_signup_post(request):
    name=request.POST['name']
    phone=request.POST['phone']
    place=request.POST['place']
    email=request.POST['email']
    dob=request.POST['dob']
    photo=request.FILES['photo']
    password=request.POST['password']
    gender=request.POST['gender']
    servicetype=request.POST['servicetype']
    today=datetime.now()
    yearofbirth= datetime.strptime(dob, "%Y-%m-%d").date()
    age=today.year-yearofbirth.year
       
    if age<18:
            messages.warning(request,'you cant register here baby come back after turning 18😗')
            return redirect('/myapp/customersignup/')
    else:
    
        if User.objects.filter(username=email).exists():
            messages.warning(request,'username already exists..!')
            return redirect('/myapp/customersignup/')
        else:
            a=User.objects.create_user(username=email,password=password)
            a.groups.add(Group.objects.get(name='serviceprovider'))
            ob=ServiceProvider()
            ob.name=name
            ob.place=place
            ob.dob=dob
            ob.photo=photo
            ob.email=email
            ob.phone=phone
            ob.gender=gender
            ob.servicetype=servicetype
            ob.LOGIN=a
            ob.save()
            return redirect('/myapp/login_page/')

@login_required(login_url='/myapp/login_page/')
def provider_home(request):
    ob=ServiceProvider.objects.get(LOGIN=request.user)
    a=Request.objects.filter(status='pending',SERVICEPROVIDER__LOGIN=request.user).count()
    b=Request.objects.filter(status='paid',SERVICEPROVIDER__LOGIN=request.user).count()
    c=Request.objects.filter(status='paid',SERVICEPROVIDER__LOGIN=request.user).aggregate(salary=Sum('amount'))
    return render(request,'serviceprovider/provider_home.html',{'data':ob,'count':a,'counts':b,'salary':c})
@login_required(login_url='/myapp/login_page/')
def provider_profile(request):
    ob=ServiceProvider.objects.get(LOGIN=request.user)
    return render(request,'serviceprovider/provider_profile.html',{'data':ob})
@login_required(login_url='/myapp/login_page/')
def provider_editprofile(request):
    ob=ServiceProvider.objects.get(LOGIN=request.user)
    return render(request,'serviceprovider/provider_editprofile.html',{'data':ob})

def provider_editprofile_post(request):
    name=request.POST['name']
    phone=request.POST['phone']
    place=request.POST['place']
    email=request.POST['email']
    dob=request.POST['dob']
    gender=request.POST['gender']
    servicetype=request.POST['servicetype']

    ob=ServiceProvider.objects.get(LOGIN=request.user)
    if 'photo' in request.FILES:
        photo=request.FILES['photo']
        ob.photo=photo
        ob.save()
    ob.name=name
    ob.phone=phone
    ob.place=place
    ob.email=email
    ob.dob=dob
    ob.gender=gender
    ob.servicetype=servicetype
    ob.save()
    return redirect('/myapp/provider_profile/')
@login_required(login_url='/myapp/login_page/')
def view_providers(request):
    ob=ServiceProvider.objects.all()
    return render(request,'customer/view_providers.html',{'data':ob})
@login_required(login_url='/myapp/login_page/')
def send_request(request,id):
    ob=ServiceProvider.objects.get(id=id)
    return render(request,'customer/send_request.html',{'data':ob})

def send_request_post(request):
    latitude=request.POST['latitude']
    longitude=request.POST['longitude']
    place=request.POST['place']
    post=request.POST['post']
    pin=request.POST['pin']
    sid=request.POST['sid']
    problem=request.POST['problem']


    ob=Request()
    ob.SERVICEPROVIDER_id=sid
    ob.CUSTOMER=Customer.objects.get(LOGIN=request.user)
    ob.latitude=latitude
    ob.longitude=longitude
    ob.pin=pin
    ob.place=place
    ob.post=post
    ob.status='pending'
    ob.date=datetime.now()
    ob.Problem=problem
    ob.save()
    return redirect('/myapp/request_status/')
@login_required(login_url='/myapp/login_page/')
def request_status(request):
    ob=Request.objects.filter(CUSTOMER__LOGIN=request.user).order_by('-id')
    return render(request,'customer/request_status.html',{'data':ob})
@login_required(login_url='/myapp/login_page/')
def payment(request):
    return render(request,'customer/payment.html')
@login_required(login_url='/myapp/login_page/')
def userpayment(request,bid,amount):

    amount= float(amount)
    print(amount,'helllloooooooooooooooooo')
    request.session["id"]=bid
    return redirect('/myapp/raz_pay/'+str(amount))

@login_required(login_url='/myapp/login_page/')
def raz_pay(request, amount):

    import razorpay

    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(
        auth=(razorpay_api_key, razorpay_secret_key)
    )

    # Convert amount from rupees to paise
    amount = float(amount)
    amount_paise = int(round(amount * 100))

    # Razorpay order
    order_data = {
        'amount': amount_paise,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': 1
    }

    # Create order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': amount,
        'amount_paise': amount_paise,
        'currency': 'INR',
        'order_id': order['id'],
    }

    return render(request, 'customer/pp.html', context)


def userpayment_post(request):

    id = request.session["id"]



    bobj = Request.objects.get(id=id)

    bobj.status = "paid"

    bobj.save()
    return redirect('/myapp/request_status/')

@login_required(login_url='/myapp/login_page/')
def view_request(request):
    ob=Request.objects.filter(SERVICEPROVIDER__LOGIN=request.user).order_by('-id')
    return render(request,'serviceprovider/view_request.html',{'data':ob})

def accept_request(request,id):
    ob=Request.objects.get(id=id)
    ob.status='accepted'
    ob.save()
    return redirect('/myapp/view_request/')

def reject_request(request,id):
    ob=Request.objects.get(id=id)
    ob.status='rejected'
    ob.save()
    return redirect('/myapp/view_request/')

def completed(request,id):
    ob=Request.objects.get(id=id)
    ob.status='completed'
    ob.save()
    return redirect('/myapp/view_request/')

def add_payment_amount_post(request,id):
    amount=request.POST['amount']
    ob=Request.objects.get(id=id)
    ob.amount=amount
    ob.status='payment pending'
    ob.save()
    return redirect('/myapp/view_request/')


# ========================================================ADMIN================================================
@login_required(login_url='/myapp/login_page/')
def admin_home(request):
    a=ServiceProvider.objects.filter(status='pending').count()
    b=ServiceProvider.objects.filter(status='accepted').count()
    c=Customer.objects.all().count()
    d=Complaints.objects.filter(status='pending').count()
    return render(request,'admin/admin_home.html',{'pcount':a,'ppcount':b,'ccount':c,'Ccount':d})

@login_required(login_url='/myapp/login_page/')
def view_serviceproviders(request):
    ob = ServiceProvider.objects.filter(status='accepted').annotate(total=Count('id'))
    return render(request,'admin/view_serviceproviders.html',{'data': ob})
@login_required(login_url='/myapp/login_page/')
def providers_requests(request):
    ob=ServiceProvider.objects.filter(status='pending')
    return render(request,'admin/providers_requests.html',{'data':ob})

def block_provider(request,id):
    ob=ServiceProvider.objects.get(id=id)
    ob.status='blocked'
    ob.save()
    return redirect('/myapp/view_serviceproviders/')

def verify_provider(request,id):
    ob=ServiceProvider.objects.get(id=id)
    ob.status='accepted'
    ob.save()
    return redirect('/myapp/providers_requests/')
@login_required(login_url='/myapp/login_page/')
def view_customers(request):
    ob=Customer.objects.all()
    return render(request,'admin/view_customers.html',{'data':ob})
@login_required(login_url='/myapp/login_page/')
def view_complaints(request):
    ob=Complaints.objects.all()
    return render(request,'admin/view_complaints.html',{'data':ob})
@login_required(login_url='/myapp/login_page/')
def replay(request,id):
    ob=Complaints.objects.get(id=id)
    return render(request,'admin/replay.html',{'data':ob})

def replay_post(request):
    replys=request.POST['replys']
    cid=request.POST['cid']
    ob=Complaints.objects.get(id=cid)
    ob.status=replys
    ob.save()
    return redirect('/myapp/view_complaints/')

