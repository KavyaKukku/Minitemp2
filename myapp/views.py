from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from myapp.models import *


def login(request):
    return render(request,'login.html')

def login_post(request):
    username=request.POST['text1']
    password=request.POST['text2']
    a1=Login.objects.filter(username=username,password=password)
    if a1.exists():
        a2=Login.objects.get(username=username,password=password)
        request.session['lid']=a2.id
        if a2.type=='admin':
            return HttpResponse("<script>alert('Login Successfully');window.location='/myapp/adminhome/'</script>")
        elif a2.type=='houseowner':
            return HttpResponse("<script>alert('Login Successfully');window.location='/myapp/ownerhome/'</script>")
        elif a2.type=='user':
            return HttpResponse("<script>alert('Login Successfully');window.location='/myapp/userhome/'</script>")
        else:
            return HttpResponse("<script>alert('Invalid username and password');window.location='/myapp/login/'</script>")
    else:
        return HttpResponse("<script>alert('User not found');window.location='/myapp/login/'</script>")


#Admin


def adminhome(request):
    return render(request,'Admin/admin_index.html')

def logout(request):
    request.session['lid']=''
    return HttpResponse("<script>alert('Log Out Successfully');window.location='/myapp/login/'</script>")


def change_pswd(request):
    return render(request, 'Admin/change_pswd.html')

def change_pswd_post(request):
    current_password=request.POST['textfield']
    new_password=request.POST['textfield2']
    confirm_password=request.POST['textfield3']

    res = Login.objects.get(id=request.session['lid'])
    if res.password == current_password:
        if new_password == confirm_password:
            res.password=new_password
            res.save()
            return HttpResponse("<script>alert('Password Changed');window.location='/myapp/login/'</script>")
        else:
            return  HttpResponse("<script>alert('Password Mismatch');window.location='/myapp/change_pswd/'</script>")
    else:
        return HttpResponse("<script>alert('User not Found');window.location='/myapp/change_pswd/'</script>")



def Manage_owner(request):
    res = HouseOwner.objects.filter(status='pending')
    return render(request, 'Admin/Manage_owner.html',{'data':res})

def Manage_owner_post(request):
    search=request.POST['search']
    res = HouseOwner.objects.filter(status='pending',place__icontains=search)
    return render(request, 'Admin/Manage_owner.html',{'data':res})


def viewacceptorreject(request):
    res=HouseOwner.objects.filter(status='approved')
    return render(request,'Admin/accept.html',{'data':res})

def accept_post(request):
    search=request.POST['search']
    res = HouseOwner.objects.filter(status='approved',place__icontains=search)
    return render(request, 'Admin/accept.html', {'data': res})

def approve_owner(request,id):
    res = HouseOwner.objects.filter(LOGIN__id=id).update(status='approved')
    std = Login.objects.filter(id=id).update(type='houseowner')
    return HttpResponse("<script>alert('Approved Successfully');window.location='/myapp/Manage_owner/'</script>")


def rejected(request):
    res = HouseOwner.objects.filter(status='Rejected')
    return render(request, 'Admin/rejected.html',{'data':res})

def rejected_post(request):
    search = request.POST['search']
    res = HouseOwner.objects.filter(status='Rejected',place__icontains=search)
    return render(request, 'Admin/rejected.html', {'data': res})


def rejected_owner(request,id):
    res = HouseOwner.objects.filter(LOGIN__id=id).update(status='Rejected')
    std = Login.objects.filter(id=id).update(type='Rejected')
    return HttpResponse("<script>alert('Rejected Successfully');window.location='/myapp/Manage_owner/'</script>")


def payment_report(request):
    res=Payment.objects.all()
    return render(request, 'Admin/payment_report.html',{'data':res})

def payment_report_post(request):
    search = request.POST['textfield']
    to = request.POST['t2']
    res=Payment.objects.filter(date__range=[search,to])
    return render(request, 'Admin/payment_report.html',{'data':res})


def review_rating(request):
    res = Review.objects.all()
    return render(request, 'Admin/review rating.html',{'data':res})

def review_rating_post(request):
    search = request.POST['textfield']
    review = request.POST['t2']
    res = Review.objects.filter(date__range=[search,review])
    return render(request, 'Admin/review rating.html', {'data': res})



def view_complaint(request):
    res=Complaint.objects.all()
    l = []

    for i in res:
        if i.LOGIN.type == "user":
            u = User.objects.get(LOGIN_id=i.LOGIN.id)
            l.append({'id':u.id,'name': u.name, 'email': u.email, 'complaint': i.complaint, 'date': i.date,'status':i.status, 'reply': i.reply})
        elif i.LOGIN.type == "houseowner":
            c = HouseOwner.objects.filter(LOGIN_id=i.LOGIN.id)
            if c.exists():
                c2 = HouseOwner.objects.get(LOGIN_id=i.LOGIN.id)
                l.append({'id':c2.id,'name': c2.name, 'email': c2.email, 'complaint': i.complaint, 'date': i.date,'status':i.status, 'reply': i.reply})
    return render(request, 'Admin/view_complaint.html',{'data':l})

def view_complaint_post(request):
    fromdate = request.POST['fdate']
    todate = request.POST['tdate']
    res = Complaint.objects.filter(date__range=[fromdate, todate])
    l = []

    for i in res:
        if i.LOGIN.type == "user":
            u = User.objects.get(LOGIN_id=i.LOGIN.id)
            l.append({'name': u.name, 'email': u.email, 'complaint': i.complaint, 'date': i.date,'status':i.status, 'reply': i.reply})
        elif i.LOGIN.type == "houseowner":
            c = HouseOwner.objects.filter(LOGIN_id=i.LOGIN.id)
            if c.exists():
                c2 = HouseOwner.objects.get(LOGIN_id=i.LOGIN.id)
                l.append({'name': c2.name, 'email': c2.email,'complaint': i.complaint, 'date': i.date,'status':i.status, 'reply': i.reply})

    return render(request, 'Admin/view_complaint.html',{'data':l})


def reply_cm(request,id):
    return render(request, 'Admin/reply.html',{'id':id})

def reply_post(request):
    reply=request.POST['textfield']
    id=request.POST['rid']
    Complaint.objects.filter(id=id).update(reply=reply,status='replied')
    return HttpResponse("<script>alert('Sending Successfully');window.location='/myapp/view_complaint/'</script>")



def view_house(request,id):
    res = Home.objects.filter(OWNER_id=id)
    request.session['oid']=id
    return render(request, 'Admin/view_house.html',{'data':res})

def view_house_post(request):
    search = request.POST['search']
    res = Home.objects.filter(OWNER_id=request.session['oid'],place__icontains=search)
    return render(request, 'Admin/view_house.html',{'data':res})



#House Owner
def signup(request):
    return render(request,'House Owner/signup_index.html')

def ownerhome(request):
    return render(request,'House Owner/ownerhome.html')

def owner_pswd(request):
    return render(request, 'House Owner/owner_pswd.html')

def owner_pswd_post(request):
    current_password=request.POST['textfield']
    new_password=request.POST['textfield2']
    confirm_password=request.POST['textfield3']

    res = Login.objects.get(id=request.session['lid'])
    if res.password == current_password:
        if new_password == confirm_password:
            res.password = new_password
            res.save()
            return HttpResponse("<script>alert('Password Changed');window.location='/myapp/login/'</script>")
        else:
            return HttpResponse("<script>alert('Password Mismatch');window.location='/myapp/owner_pswd/'</script>")
    else:
        return HttpResponse("<script>alert('User not Found');window.location='/myapp/owner_pswd/'</script>")


def add_house(request):
    return render(request, 'House Owner/add_house.html')


def add_house_post(request):
    image = request.FILES['img']
    amount = request.POST['textfield']
    proof = request.FILES['fileField']
    phone = request.POST['textfield2']
    place = request.POST['textfield3']
    post = request.POST['textfield4']
    pincode = request.POST['textfield5']
    district = request.POST['textfield6']
    property = request.POST['select3']
    latitude = request.POST['textfield7']
    longitude = request.POST['textfield17']
    period = request.POST['textfield9']
    area = request.POST['textfield8']
    room = request.POST['select1']
    bathroom = request.POST['select2']
    furnishing = request.POST['select4']
    parking = request.POST['parking']
    kitchen = request.POST['kitchen']
    description = request.POST['description']

    # image
    date = datetime.now().strftime('%Y%m%d-%H%M%S')+".jpg"
    fs = FileSystemStorage()
    fs.save(date, image)
    photopath = fs.url(date)

    # idproof
    date2 = datetime.now().strftime('%Y%m%d-%H%M%S')+"2.jpg"
    fs2 = FileSystemStorage()
    fs2.save(date2, proof)
    proofpath = fs2.url(date2)

    obj=Home()
    obj.OWNER=HouseOwner.objects.get(LOGIN=request.session['lid'])
    obj.image=photopath
    obj.rental_amount=amount
    obj.proof=proofpath
    obj.phoneno=phone
    obj.place=place
    obj.post=post
    obj.pincode=pincode
    obj.district=district
    obj.property_type=property
    obj.latitude=latitude
    obj.longitude=longitude
    obj.rental_period=period
    obj.area_sqft=area
    obj.rooms=room
    obj.bathrooms=bathroom
    obj.furnishing=furnishing
    obj.parking=parking
    obj.kitchen=kitchen
    obj.description=description
    obj.reqstatus='pending'
    obj.save()

    return HttpResponse("<script>alert('Added Successfully');window.location='/myapp/ownerhome/'</script>")

def edit_house(request,id):
    data=Home.objects.get(id=id)
    return render(request, 'House Owner/edit_house.html',{'data':data})

def edit_house_post(request):

    id = request.POST['id']
    amount = request.POST['textfield']
    phone = request.POST['textfield2']
    place = request.POST['textfield3']
    post = request.POST['textfield4']
    pincode = request.POST['textfield5']
    district = request.POST['textfield6']
    property = request.POST['select3']
    location = request.POST['textfield7']
    period = request.POST['textfield9']
    area = request.POST['textfield8']
    room = request.POST['select1']
    bathroom = request.POST['select2']
    furnishing = request.POST['select4']
    parking = request.POST['parking']
    kitchen = request.POST['kitchen']
    description = request.POST['description']
    obj = Home.objects.get(id=id)
    # image
    if 'Img' in request.FILES:
        image = request.FILES['Img']
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
        fs = FileSystemStorage()
        fs.save(date, image)
        photopath = fs.url(date)
        obj.image = photopath
        obj.save()

    # idproof
    if 'fileField' in request.FILES:
        proof = request.FILES['fileField']
        date2 = datetime.now().strftime('%Y%m%d-%H%M%S') + "2.jpg"
        fs2 = FileSystemStorage()
        fs2.save(date2, proof)
        proofpath = fs2.url(date2)
        obj.proof = proofpath
        obj.save()

    obj.OWNER = HouseOwner.objects.get(LOGIN=request.session['lid'])

    obj.rental_amount = amount
    obj.phoneno = phone
    obj.place = place
    obj.post = post
    obj.pincode = pincode
    obj.district = district
    obj.property_type = property
    obj.location = location
    obj.rental_period = period
    obj.area_sqft = area
    obj.rooms = room
    obj.bathrooms = bathroom
    obj.furnishing = furnishing
    obj.parking = parking
    obj.kitchen = kitchen
    obj.description = description
    obj.reqstatus='pending'
    obj.save()

    return HttpResponse("<script>alert('Edit successfully');window.location='/myapp/ownerview_house/'</script>")


def delete_house(request,id):
    data=Home.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Deleted successfully');window.location='/myapp/ownerview_house/'</script>")

def edit_profile(request,id):
    obj=HouseOwner.objects.get(LOGIN_id=request.session['lid'])
    return render(request, 'House Owner/edit_profile.html',{'data':obj})

def edit_profile_post(request):
    id = request.POST['id']
    name = request.POST['textfield']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']
    gender = request.POST['radio']
    dob = request.POST['textfield4']
    place = request.POST['textfield5']
    post = request.POST['textfield6']
    pincode = request.POST['textfield7']
    district = request.POST['textfield8']
    aadhar = request.POST['textfield10']
    obj = HouseOwner.objects.get(LOGIN_id=request.session['lid'])
    # id proof
    if 'fileField' in request.FILES:
        idproof = request.FILES['fileField']
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
        fs = FileSystemStorage()
        fs.save(date, idproof)
        proofpath = fs.url(date)
        obj.idproof = proofpath


    obj.name = name
    obj.email = email
    obj.phoneno = phone
    obj.gender = gender
    obj.dob = dob
    obj.place = place
    obj.post = post
    obj.pincode = pincode
    obj.district = district
    obj.Aadhar=aadhar
    obj.save()
    return HttpResponse("<script>alert('Edit successfully');window.location='/myapp/view_profile/'</script>")


def owner_signup(request):
    return render(request, 'House Owner/signup_index.html')

def owner_signup_post(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']
    gender = request.POST['radio']
    dob = request.POST['textfield4']
    place = request.POST['textfield5']
    post = request.POST['textfield6']
    pincode = request.POST['textfield7']
    district = request.POST['textfield8']
    password=request.POST['textfield9']
    aadhar=request.POST['textfield10']
    idproof = request.FILES['proof']


    #id proof
    fs = FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d-%H%M%S')

    fs.save(date,idproof)
    photopath=fs.url(date)


    if Login.objects.filter(username=email).exists():
        return HttpResponse("<script>alert('Already exixsts');window.location='/myapp/owner_signup/'</script>")

    l=Login()
    l.username=email
    l.password=password
    l.type='pending'
    l.save()


    hw=HouseOwner()
    hw.name = name
    hw.email = email
    hw.phoneno = phone
    hw.gender = gender
    hw.dob = dob
    hw.place = place
    hw.post = post
    hw.pincode = pincode
    hw.district = district
    hw.idproof = photopath
    hw.Aadhar=aadhar
    hw.LOGIN=l
    hw.status='pending'
    hw.save()

    return HttpResponse("<script>alert('successfully signup');window.location='/myapp/login/'</script>")



def owner_rating(request):
    res = Review.objects.all()
    return render(request, 'House Owner/review_rating.html',{'data':res})

def owner_rating_post(request):
    search = request.POST['textfield']
    review = request.POST['t2']
    res = Review.objects.filter(date__range=[search,review])
    return render(request, 'House Owner/review_rating.html')


def send_complaint(request):
    return render(request, 'House Owner/send_complaint.html')

def send_complaint_post(request):
    complaint = request.POST['textarea']

    c=Complaint()
    c.complaint=complaint
    c.status='Pending'
    c.reply='Pending'
    c.date=datetime.now()
    c.LOGIN_id=request.session['lid']
    c.save()
    return HttpResponse("ok")


def ownerview_house(request):
    res = Home.objects.filter(OWNER__LOGIN_id=request.session['lid'])
    return render(request, 'House Owner/ownerview_house.html', {'data':res})

def ownerview_house_post(request):
    search = request.POST['search']
    res = Home.objects.filter(OWNER__LOGIN_id=request.session['lid'],place__icontains=search)
    return render(request, 'House Owner/ownerview_house.html', {'data':res})


def view_payment(request):
    res=Payment.objects.all()
    return render(request, 'House Owner/view_payment.html',{'data':res})

def view_payment_post(request):
    search = request.POST['textfield']
    to = request.POST['t2']
    res=Payment.objects.filter(date__range=[search,to])
    return render(request, 'House Owner/view_payment.html',{'data':res})


def view_profile(request):
    res=HouseOwner.objects.get(LOGIN=request.session['lid'])
    return render(request, 'House Owner/view_profile.html',{'data':res})
#
# def view_profile_post(request):
#     search = request.POST['search']
#     return render(request, 'House Owner/view_profile.html')
#

def view_reply(request):
    data=Complaint.objects.filter(LOGIN=request.session['lid'])
    return render(request, 'House Owner/view_reply.html',{'data':data})

def view_reply_post(request):
    search = request.POST['textfield']
    reply = request.POST['t2']
    data = Complaint.objects.filter(date__range=[search, reply], LOGIN=request.session['lid'])
    return render(request, 'House Owner/view_reply.html',{'data':data})


def view_request(request):
    # re=Request.objects.all()
    re=Request.objects.filter(HOME__OWNER__LOGIN_id=request.session['lid'],status='pending')
    return render(request, 'House Owner/view_request.html',{'data':re})

def view_request_post(request):
    search = request.POST['search']
    re=Request.objects.filter(HOME__OWNER__LOGIN_id=request.session['lid'],USER__name__icontains=search,status='pending')
    return render(request, 'House Owner/view_request.html',{'data':re})

def accept_user(request,id):
    obj=Request.objects.filter(id=id).update(status='Approved')
    res=Home.objects.filter(id=id).update(reqstatus='Approved')
    return HttpResponse('''<script>alert('Accepted Successfully');window.location='/myapp/view_request/'</script>''')

def reject_user(request,id):
    obj=Request.objects.filter(id=id).update(status="Rejected")
    res=Home.objects.filter(id=id).update(reqstatus='Rejected')

    return HttpResponse('''<script>alert('Rejected Successfully');;window.location='/myapp/view_request/'</script>''')


def view_accepted_user(request):
    obj = Request.objects.filter(status="Approved")
    return render(request,'House Owner/view_accepted_user.html',{"data":obj})


def view_accepted_user_post(request):
    search = request.POST['search']
    obj = Request.objects.filter(USER__name__icontains=search)
    return render(request,'House Owner/view_accepted_user.html',{"data":obj})


#user


def userhome(request):
    return render(request,'User/userhome.html')


def user_pswd(request):
    return render(request, 'User/change_pswd.html')

def user_pswd_post(request):
    current_password = request.POST['textfield']
    new_password = request.POST['textfield2']
    confirm_password = request.POST['textfield3']

    res = Login.objects.get(id=request.session['lid'])
    if res.password == current_password:
        if new_password == confirm_password:
            res.password = new_password
            res.save()
            return HttpResponse("<script>alert('Password Changed');window.location='/myapp/login/'</script>")
        else:
            return HttpResponse("<script>alert('Password Mismatch');window.location='/myapp/user_pswd/'</script>")
    else:
        return HttpResponse("<script>alert('User not Found');window.location='/myapp/user_pswd/'</script>")



def edit_userprofile(request):
    obj=User.objects.get(LOGIN__id=request.session['lid'])
    return render(request, 'User/edit_userprofile.html',{'data':obj})

def edit_userprofile_post(request):
    id = request.POST['id']
    name = request.POST['textfield']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']
    gender = request.POST['radio']
    dob = request.POST['textfield4']
    place = request.POST['textfield5']
    post = request.POST['textfield6']
    pincode = request.POST['textfield7']
    district = request.POST['textfield8']
    obj = User.objects.get(LOGIN_id=request.session['lid'])

    #id proof

    if 'fileField' in request.FILES:
        idproof = request.FILES['fileField']
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
        fs = FileSystemStorage()
        fs.save(date, idproof)
        proofpath = fs.url(date)
        obj.idproof = proofpath


    obj.name = name
    obj.email = email
    obj.phoneno = phone
    obj.gender = gender
    obj.dob = dob
    obj.place = place
    obj.post = post
    obj.pincode = pincode
    obj.district = district
    obj.save()
    return HttpResponse("<script>alert('Edit successfully');window.location='/myapp/view_userprofile/'</script>")



def user_report(request):
    obj=Payment.objects.filter(REQUEST__USER__LOGIN_id=request.session['lid'])
    return render(request, 'User/payment_report.html',{'data':obj})

def user_report_post(request):
    search = request.POST['textfield']
    report = request.POST['t2']

    obj=Payment.objects.filter(view_house_userdate__range=[search,report])
    return render(request, 'User/payment_report.html',{'data':obj})


def search_house(request):
    res=Request.objects.filter(HOME__reqstatus='pending')
    return render(request, 'User/search_house.html',{'data':res})

def view_house_user(request):
    approved_home_ids = Request.objects.filter(status='approved').values_list('HOME_id', flat=True)
    res = Home.objects.exclude(id__in=approved_home_ids) 
       
    return render(request, 'User/search_house.html', {'data': res})

def search_house_post(request):
    search = request.POST.get('t1', '')  # Get the search term with a default empty string
    category = request.POST.get('category', '')  # Get the category with a default empty string
    ptype=request.POST.get('property','')
    # Get all home IDs with approved requests
    approved_home_ids = Request.objects.filter(status='approved').values_list('HOME_id', flat=True)

    # Initialize the queryset excluding approved homes
    res = Home.objects.exclude(id__in=approved_home_ids)

    # Apply filters based on category and search term
    if category:
        res = res.filter(furnishing__icontains=category)
    
    if search:
        res = res.filter(place__icontains=search) | res.filter(rooms__icontains=search)
        
    if ptype:
        res = res.filter(property_type__icontains=ptype)

            

    # Render the result to the template
    return render(request, 'User/search_house.html', {'data': res})
# def search_house_post(request):
    search = request.POST['t1']
    category = request.POST['category']
    
    approved_home_ids = Request.objects.filter(status='approved').values_list('HOME_id', flat=True)
    if category:
        res = res.filter(furnishing__icontains=category)
    
    if search:
        res = res.filter(place__icontains=search) | res.filter(rooms__icontains=search)

    # if category=='':
    #     # res = Home.objects.exclude(id__in=approved_home_ids)
    #     res=res.filter(place__icontains=search) | res.filter(rooms__icontains=search)
    #     # res=Home.objects.filter(place__icontains=search)|Home.objects.filter(rooms__icontains=search)
    # elif search=='':
    #     res = res.filter(furnishing__icontains=category) | res.filter(rooms__icontains=search)
    #     # res=Home.objects.filter(furnishing__icontains=category)|Home.objects.filter(rooms__icontains=search)
    # else:
    #     res = res.filter(furnishing__icontains=category,place__icontains=search) | res.filter(rooms__icontains=search)

    #     # res=Home.objects.filter(furnishing__icontains=category,place__icontains=search)|Home.objects.filter(rooms__icontains=search)

    return render(request, 'User/search_house.html',{'data':res})




def send_review(request):
    return render(request, 'User/sendreviewrating.html')

def send_review_post(request):
    review = request.POST['textfield']
    rating = request.POST['rating']

    rs=Review()
    rs.date = datetime.now()
    rs.rating=rating
    rs.review=review
    rs.USER = User.objects.get(LOGIN_id=request.session['lid'])
    rs.save()
    return HttpResponse("ok")


def user_signup(request):
    return render(request, 'User/signup_user.html')

def user_signup_post(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']
    gender = request.POST['radio']
    dob = request.POST['textfield4']
    place = request.POST['textfield5']
    post = request.POST['textfield6']
    pincode = request.POST['textfield7']
    district = request.POST['textfield8']
    password = request.POST['textfield9']
    idproof = request.FILES['proof']

    # id proof
    date = datetime.now().strftime('%Y%m%d-%H%M%S')
    fs = FileSystemStorage()
    fs.save(date, idproof)
    photopath = fs.url(date)


    if Login.objects.filter(username=email).exists():
        return HttpResponse("<script>alert('Already exixsts');window.location='/myapp/user_signup/'</script>")


    l = Login()
    l.username = email
    l.password = password
    l.type = 'user'
    l.save()

    us = User()
    us.name = name
    us.email = email
    us.phoneno = phone
    us.gender = gender
    us.dob = dob
    us.place = place
    us.post = post
    us.pincode = pincode
    us.district = district
    us.idproof = photopath
    us.LOGIN = l
    us.status = 'pending'
    us.save()

    return HttpResponse("<script>alert('Signup Successfully');window.location='/myapp/login/'</script>")


def user_complaint(request):
    return render(request, 'User/send_complaint.html')

def user_complaint_post(request):
    complaint = request.POST['textarea']
    c = Complaint()
    c.complaint = complaint
    c.status = 'Pending'
    c.reply = 'Pending'
    c.date = datetime.now()
    c.LOGIN_id = request.session['lid']
    c.save()
    return HttpResponse("<script>alert('Sending Successfully');window.location='/myapp/userhome/'</script>")



def user_reply(request):
    data=Complaint.objects.filter(LOGIN=request.session['lid'])
    return render(request, 'User/view_reply.html',{'data':data})

def user_reply_post(request):
    search = request.POST['textfield']
    reply = request.POST['t2']
    data=Complaint.objects.filter(date__range=[search,reply],LOGIN=request.session['lid'])
    return render(request, 'User/view_reply.html',{'data':data})


def view_request_status(request):
    res = Request.objects.filter(USER__LOGIN_id=request.session['lid'])
    return render(request, 'User/view_request_status.html',{'data':res})

def view_request_status_post(request):
    search = request.POST['textfield']
    to = request.POST['t2']
    res = Request.objects.filter(date__range=[search, to])
    return render(request, 'User/view_request_status.html',{'data':res})


def view_userprofile(request):
    res=User.objects.get(LOGIN_id=request.session['lid'])
    return render(request, 'User/view_userprofile.html',{'data':res})

def view_userprofile_post(request):
    search = request.POST['search']
    return render(request, 'User/view_userprofile.html')


def user_request(request):
    id=request.POST['id']
    rental_period = request.POST['rental_period']
    r=Request()
    r.HOME=Home.objects.get(id=id)
    r.USER=User.objects.get(LOGIN_id=request.session['lid'])
    r.date=datetime.now().today()
    r.rental_period=rental_period
    r.status='pending'
    r.save()

    h=Home.objects.filter(id=id).update(reqstatus='pending')

    return HttpResponse("<script>alert('Successfull');window.location='/myapp/view_house_user/'</script>")

def user_request_post(request):
    search = request.POST['search']
    return render(request,'User/send_request.html')

def payment(request,id,aid):
    import razorpay
    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    # amount = 200
    amount= float(aid)

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
    }

    obj = Payment()
    obj.REQUEST_id = id
    obj.date = datetime.today()
    obj.amount = float(amount)
    obj.status = 'paid'
    obj.save()

    Request.objects.filter(id=id).update(status='paid')

    return render(request, 'User/payment.html',{ 'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],"id":id})

