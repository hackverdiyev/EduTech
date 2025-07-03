from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from problems.models import *
from random import randint
from base.models import *
from time import time
import openai
import json

standard_symbols=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0','.','_']
subjects={'math':'Math','physics':'Physics','astronomy':'Astronomy','chemistry':'Chemistry','biology':'Biology','history':'History','junior':'Junior'}
openai.api_key="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"

def islogin(request):
    if 'username' in request.session:
        return Account.objects.get(username=request.session['username'])
    return False

def create_restore_request(username,email,password="",fullname=""):
    try:
        Verification.objects.get(username=username).delete()
    except:
        pass
    Verification(username=username,email=email,password=password,fullname=fullname,six_digit_code=randint(100000,999999),time=time()*1000).save()
    send_mail(
        "Şifrə Yeniləmə",
        f"Olimpus Verification Code\nThis verification code was sent to your email for help getting back into a Olimpus Account:\n\n{Verification.objects.get(username=username).six_digit_code}\n\nDon’t know why you received this?\n\nSomeone who couldn’t remember their Olimpus Account details probably gave your email address by mistake. You can safely ignore this email.\n\nTo protect your account,don’t forward this email or give this code to anyone.\n\nOlimpus Team",
        "settings.EMAIL_HOST_USER",
        [email],
        True
    )

def base(request):
    problems_count,problems = len(Problem.objects.all()),Problem.objects.all().order_by('-pub_date')[:10]
    return render(request,'base.html',{"problems_count":problems_count,"problems": problems,"subjects":subjects,"islogin":islogin(request)})

def contact(request):
    if request.method=='POST':
        ContactMessage(full_name=request.POST["fullname"],email=request.POST["email"],message=request.POST["message"]).save()
        return redirect("/contact")
    return render(request,"contact.html",{"subjects":subjects,"islogin":islogin(request)})

def login(request):
    if islogin(request):
        return redirect("/")
    if request.method=='POST':
        try:
            if Account.objects.get(username=request.POST["username"]).password==request.POST["password"]:
                request.session['username']=request.POST["username"]
                return redirect("/")
            return render(request,'login.html',{"error":2,"subjects":subjects,"islogin":False})
        except:
            return render(request,'login.html',{"error":1,"subjects":subjects,"islogin":False})
    return render(request,'login.html',{"subjects":subjects,"islogin":False})

def logout(request):
    if islogin(request):
        del request.session['username']
    return redirect('/')

def register(request):
    if islogin(request):
        return redirect("/")
    if request.method=='POST':
        try:
            Account.objects.get(username=request.POST["username"])
            return render(request,'register.html',{"error":1,"subjects":subjects,"islogin":False})
        except:
            if len(request.POST["username"])<4 or len(request.POST["username"])>20:
                return render(request,'register.html',{"error":2,"subjects":subjects,"islogin":False})
            a=0
            for i in request.POST["username"]:
                if i not in standard_symbols:
                    a=1
                    break
            if a:
                return render(request,'register.html',{"error":3,"subjects":subjects,"islogin":False})
            a=1
            for i in request.POST["username"]:
                if i in standard_symbols[:52]:
                    a=0
                    break
            if a:
                return render(request,'register.html',{"error":4,"subjects":subjects,"islogin":False})
            try:
                Account.objects.get(email=request.POST["email"].lower())
                return render(request,'register.html',{"error":5,"subjects":subjects,"islogin":False})
            except:
                if len(request.POST["email"].lower().split('@'))!=2 or len(request.POST["email"].lower().split('@')[0])==0 or len(request.POST["email"].lower().split('@')[1].split('.'))!=2 or len(request.POST["email"].lower().split('@')[1].split('.')[0])==0 or len(request.POST["email"].lower().split('@')[1].split('.')[1])==0 or len(request.POST["email"].lower())>50:
                    return render(request,'register.html',{"error":6,"subjects":subjects,"islogin":False})
                if request.POST["password"]!=request.POST["password_repeat"]:
                    return render(request,'register.html',{"error":7,"subjects":subjects,"islogin":False})
                if len(request.POST["password"])<8 or len(request.POST["password"])>50:
                    return render(request,'register.html',{"error":8,"subjects":subjects,"islogin":False})
                a=0
                for i in request.POST["password"]:
                    if i not in standard_symbols:
                        a=1
                        break
                if a:
                    return render(request,'register.html',{"error":9,"subjects":subjects,"islogin":False})
                a=1
                for i in request.POST["password"]:
                    if i in standard_symbols[:26]:
                        a=0
                        break
                if not a:
                    a=1
                    for i in request.POST["password"]:
                        if i in standard_symbols[26:52]:
                            a=0
                            break
                if not a:
                    a=1
                    for i in request.POST["password"]:
                        if i in standard_symbols[52:62]:
                            a=0
                            break
                if a:
                    return render(request,'register.html',{"error":10,"subjects":subjects,"islogin":False})
                create_restore_request(request.POST["username"],request.POST["email"].lower(),request.POST["password"],request.POST["fullname"])
                return redirect(f'/verification/{request.POST["username"]}/register')
    return render(request,'register.html',{"subjects":subjects,"islogin":False})

def verification(request,username,request_type):
    user=islogin(request)
    if request.method=='POST':
        if request.POST["code"]==f"{Verification.objects.get(username=username).six_digit_code}":
            if time()*1000-Verification.objects.get(username=username).time<300000:
                if request_type=='register':
                    Account(username=username,fullname=Verification.objects.get(username=username).fullname,email=Verification.objects.get(username=username).email,password=Verification.objects.get(username=username).password).save()
                    request.session['username']=username
                    Verification.objects.get(username=username).delete()
                    return redirect("/")
                if request_type=='restore':
                    Verification.objects.get(username=username).delete()
                    return redirect(f'/select_password/{username}')
                if request_type=='change_email':
                    user.email=Verification.objects.get(username=username).email
                    user.save()
                    Verification.objects.get(username=username).delete()
                    return redirect("/profile")
            return render(request,'verification.html',{"error":2,"username":username,"time":Verification.objects.get(username=username).time,"subjects":subjects,"islogin":user})
        return render(request,'verification.html',{"error":1,"username":username,'request_type':request_type,"time":Verification.objects.get(username=username).time,"subjects":subjects,"islogin":user})
    if request.META.get('HTTP_REFERER')==None:
        return redirect('/restore_password')
    return render(request,'verification.html',{"username":username,'request_type':request_type,"time":Verification.objects.get(username=username).time,"subjects":subjects,"islogin":user})

def verification_again(request,username,request_type):
    if request.META.get('HTTP_REFERER')==None:
        return redirect('/restore_password')
    create_restore_request(username,Verification.objects.get(username=username).email)
    return redirect(f'/verification/{username}/{request_type}')

def restore_password(request):
    user=islogin(request)
    if request.method=='POST':
        try:
            if Account.objects.get(username=request.POST["username"]).email==request.POST["email"].lower():
                create_restore_request(request.POST["username"],Account.objects.get(username=request.POST["username"]).email)
                return redirect(f'/verification/{request.POST["username"]}/restore')
            return render(request,'restore_password.html',{"error":2,"subjects":subjects,"islogin":user})
        except:
            return render(request,'restore_password.html',{"error":1,"subjects":subjects,"islogin":user})
    return render(request,'restore_password.html',{"subjects":subjects,"islogin":user})

def select_password(request,username):
    user=Account.objects.get(username=username)
    if request.method=='POST':
        if request.POST["password"]!=request.POST["password_repeat"]:
            return render(request,'select_password.html',{"error":1,"subjects":subjects,"islogin":user})
        if len(request.POST["password"])<8 or len(request.POST["password"])>50:
            return render(request,'select_password.html',{"error":2,"subjects":subjects,"islogin":user})
        a=0
        for i in request.POST["password"]:
            if i not in standard_symbols:
                a=1
                break
        if a:
            return render(request,'select_password.html',{"error":3,"subjects":subjects,"islogin":user})
        a=1
        for i in request.POST["password"]:
            if i in standard_symbols[:26]:
                a=0
                break
        if not a:
            a=1
            for i in request.POST["password"]:
                if i in standard_symbols[26:52]:
                    a=0
                    break
        if not a:
            a=1
            for i in request.POST["password"]:
                if i in standard_symbols[52:62]:
                    a=0
                    break
        if a:
            return render(request,'select_password.html',{"error":4,"subjects":subjects,"islogin":user})
        user.password=request.POST["password"]
        user.save()
        return redirect('/login')
    if request.META.get('HTTP_REFERER')==None:
        return redirect('/restore_password')
    return render(request,'select_password.html',{"subjects":subjects,"islogin":user})

def profile(request,username):
    user=islogin(request)
    if user==False or request.session["username"]!=username:
        id=Account.objects.get(username=username)
        return render(request,'profile_view.html',{'username':Account.objects.get(username=username),"user_problems":Problem.objects.filter(user_added=id),"user_solutions":Solution.objects.filter(user_solved=id),"subjects":subjects,"islogin":user})
    user_problems=Problem.objects.filter(user_added=user)
    user_solutions=Solution.objects.filter(user_solved=user)
    if request.method=='POST':
        if 'fullname' in request.POST:
            user.fullname=request.POST["fullname"]
            user.save()
            return render(request,'profile.html',{"user_problems":user_problems,"user_solutions":user_solutions,"default":"profile","subjects":subjects,"islogin":user})
        if 'delete' in request.POST:
            user.profile_photo='profile_photos/default_pp.png'
            user.save()
            return render(request,'profile.html',{"user_problems":user_problems,"user_solutions":user_solutions,"default":"profile","subjects":subjects,"islogin":user})
        if 'photo' in request.FILES:
            user.profile_photo=request.FILES.get("photo")
            user.save()
            return render(request,'profile.html',{"user_problems":user_problems,"user_solutions":user_solutions,"default":"profile","subjects":subjects,"islogin":user})
        if 'username' in request.POST:
            if request.POST['username']==request.session['username']:
                return render(request,'profile.html',{"user_problems":user_problems,"user_solutions":user_solutions,"default":"profile","subjects":subjects,"islogin":user})
            try:
                Account.objects.get(username=request.POST["username"])
                return render(request,'profile.html',{"error":6,"default":"profile","subjects":subjects,"islogin":user})
            except:
                if len(request.POST["username"])<4 or len(request.POST["username"])>20:
                    return render(request,'profile.html',{"error":7,"default":"profile","subjects":subjects,"islogin":user})
                a=0
                for i in request.POST["username"]:
                    if i not in standard_symbols:
                        a=1
                        break
                if a:
                    return render(request,'profile.html',{"error":8,"default":"profile","subjects":subjects,"islogin":user})
                a=1
                for i in request.POST["username"]:
                    if i in standard_symbols[:52]:
                        a=0
                        break
                if a:
                    return render(request,'profile.html',{"error":9,"default":"profile","subjects":subjects,"islogin":user})
                user.username=request.POST["username"]
                user.save()                
                request.session["username"]=request.POST["username"]
                return redirect(f'/profile/{user.username}')
        if 'email' in request.POST:
            if request.POST['email']==Account.objects.get(username=request.session['username']).email:
                return render(request,'profile.html',{"user_problems":user_problems,"user_solutions":user_solutions,"default":"profile","subjects":subjects,"islogin":user})
            try:
                Account.objects.get(email=request.POST["email"].lower())
                return render(request,'profile.html',{"error":10,"default":"profile","subjects":subjects,"islogin":user})
            except:
                if len(request.POST["email"].lower().split('@'))!=2 or len(request.POST["email"].lower().split('@')[0])==0 or len(request.POST["email"].lower().split('@')[1].split('.'))!=2 or len(request.POST["email"].lower().split('@')[1].split('.')[0])==0 or len(request.POST["email"].lower().split('@')[1].split('.')[1])==0 or len(request.POST["email"].lower())>50:
                    return render(request,'profile.html',{"error":11,"default":"profile","subjects":subjects,"islogin":user})
                create_restore_request(request.session["username"],request.POST["email"].lower())
                return redirect(f'/verification/{request.session["username"]}/change_email')
        if 'password' in request.POST:
            if Account.objects.get(username=request.session["username"]).password==request.POST["previous_password"]:
                if request.POST["password"]!=request.POST["password_repeat"]:
                    return render(request,'profile.html',{"error":2,"user_problems":user_problems,"user_solutions":user_solutions,"default":"password","subjects":subjects,"islogin":user})
                if len(request.POST["password"])<8 or len(request.POST["password"])>50:
                    return render(request,'profile.html',{"error":3,"user_problems":user_problems,"user_solutions":user_solutions,"default":"password","subjects":subjects,"islogin":user})
                a=0
                for i in request.POST["password"]:
                    if i not in standard_symbols:
                        a=1
                        break
                if a:
                    return render(request,'profile.html',{"error":4,"user_problems":user_problems,"user_solutions":user_solutions,"default":"password","subjects":subjects,"islogin":user})
                a=1
                for i in request.POST["password"]:
                    if i in standard_symbols[:26]:
                        a=0
                        break
                if not a:
                    a=1
                    for i in request.POST["password"]:
                        if i in standard_symbols[26:52]:
                            a=0
                            break
                if not a:
                    a=1
                    for i in request.POST["password"]:
                        if i in standard_symbols[52:62]:
                            a=0
                            break
                if a:
                    return render(request,'profile.html',{"error":5,"user_problems":user_problems,"user_solutions":user_solutions,"default":"password","subjects":subjects,"islogin":user})
                user.password=request.POST["password"]
                user.save()
                return render(request,'profile.html',{"success":True,"user_problems":user_problems,"user_solutions":user_solutions,"default":"password","subjects":subjects,"islogin":user})
            return render(request,'profile.html',{"error":1,"user_problems":user_problems,"user_solutions":user_solutions,"default":"password","subjects":subjects,"islogin":user})
    return render(request,'profile.html',{"user_problems":user_problems,"user_solutions":user_solutions,"default":"profile","subjects":subjects,"islogin":user})

def profile_view(request,username):
    user=islogin(request)
    if user and request.session["username"]==username:
        return redirect("/profile")
    id=Account.objects.get(username=username)
    return render(request,'profile_view.html',{'username':Account.objects.get(username=username),"user_problems":Problem.objects.filter(user_added=id),"user_solutions":Solution.objects.filter(user_solved=id),"subjects":subjects,"islogin":user})

def admin_page(request):
    user=islogin(request)
    if user==False or user.admin_tag==False:
        return redirect("/")
    return redirect("/admin/bc91b7c47993de857e161b3984d195672153b07b2243b7a5838cc189cb677aa3")

def ai(request):
    user=islogin(request)
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        text=openai.ChatCompletion.create(model='gpt-3.5-turbo',messages=[{'role':'user','content':data['ai_data']+"with one sentence."}])["choices"][0]["message"]["content"]
        return JsonResponse({'result':text})
    return render(request,'ai.html',{"subjects":subjects,"islogin":user})