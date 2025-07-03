from django.shortcuts import render,redirect
from django.http import JsonResponse
from base.models import Account
from base.views import subjects
from problems.models import *
from PIL import Image
import pytesseract
import openai

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
openai.api_key="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"

def islogin(request):
    if 'username' in request.session:
        return Account.objects.get(username=request.session['username'])
    return False

def ranking(request):
    users=Account.objects.filter(point__gt=0).order_by('-point')
    return render(request,'ranking.html',{"users":users,"subjects":subjects,"islogin":islogin(request)})

def problems_main(request):
    return render(request,"problems_main.html",{"subjects":subjects,"islogin":islogin(request)})

def problems(request,subject):
    problems=Problem.objects.filter(problem_subject=subject)
    if request.method=='POST':
        filtered_problems=[]
        filter=request.POST['search'].strip()
        for i in problems:
            if filter.lower() in i.source_problem.lower():
                filtered_problems.append(i)
        return render(request,'problems.html',{"filter":filter,"problems":filtered_problems,"subjects":subjects,"islogin":islogin(request)})
    return render(request,'problems.html',{"problems":problems,"subjects":subjects,"islogin":islogin(request)})

def problem_view(request,subject,id):
    user=islogin(request)
    problem=Problem.objects.get(id=id)
    text=False
    if request.method=='POST':
        if 'report' in request.POST:
            checkbox_problem=False
            checkbox_solution=False
            checkbox_content=False
            checkbox_chat=False
            checkbox_other=False
            if 'report_problem' in request.POST:
                checkbox_problem=True
            if 'report_solution' in request.POST:
                checkbox_solution=True
            if 'report_content' in request.POST:
                checkbox_content=True
            if 'report_chat' in request.POST:
                checkbox_chat=True
            if 'report_other' in request.POST:
                checkbox_other=True
            if checkbox_other:
                ReportedProblem(problem_reported=problem,checkbox_problem=checkbox_problem,checkbox_solution=checkbox_solution,checkbox_content=checkbox_content,checkbox_chat=checkbox_chat,other=request.POST['report_other']).save()
            elif checkbox_other==False:
                ReportedProblem(problem_reported=problem,checkbox_problem=checkbox_problem,checkbox_solution=checkbox_solution,checkbox_content=checkbox_content,checkbox_chat=checkbox_chat,other="").save()
            return redirect(f'/problems/{subject}/{id}')
        if 'askai' in request.POST:
            text=problem.problem_context
            if len(text)==0:
                text=pytesseract.image_to_string(Image.open(problem.problem_context_img))
            text=openai.ChatCompletion.create(model='gpt-3.5-turbo',messages=[{'role':'user','content':text}])
            text=text["choices"][0]["message"]["content"]
        if 'chat' in request.POST:
            if user==False:
                return redirect('/login')
            if len(request.POST["message"].strip())>0:
                Chat(message=request.POST["message"].strip(),problem=problem,user_added=user).save()
                return redirect(f'/problems/{subject}/{id}')
    if problem.show_problem==False and (user==False or (user.admin_tag==False and user.teacher_tag==False and user.username!='Selcan')): #SELCAN
        return redirect(f'/problems/{problem.problem_subject}')
    messages=Chat.objects.filter(problem=problem).order_by('-date')
    solution=Solution.objects.filter(problem=problem)
    verify=False
    if len(solution)==0:
        solution=False
    elif problem.have_solution:
        solution=solution[0]
    elif user and (user.admin_tag or user.teacher_tag or user.username=='Selcan'): #SELCAN
        solution=solution[0]
        verify=True
    problem.problem_views+=1
    problem.save()
    return render(request,'problem_view.html',{"problem":problem,'solution':solution,'verify':verify,'messages':messages,'ai':text,"subjects":subjects,"islogin":user})

def add_problem(request):
    user=islogin(request)
    if user==False:
        return redirect('/login')
    if request.method=='POST':
        problem_subject=request.POST["problem_subject"]
        show_problem=False
        if request.FILES.get("photo")==None and len(request.POST["text_of_problem"].strip())==0:
            return redirect('/add')
        if user.admin_tag or user.teacher_tag or user.clever_tag:
            user.point+=1
            if user.point>=50:
                user.clever_tag=1
            user.save()
            show_problem=True
        p=Problem(source_problem=request.POST['source_problem'],problem_subject=problem_subject,problem_context_img=request.FILES.get("photo"),problem_context=request.POST["text_of_problem"],show_problem=show_problem,user_added=user)
        p.save()
        if 'with_solution' in request.POST:
            return redirect(f'/add/{p.id}')
        return redirect(f'/problems/{problem_subject}')
    return render(request,'add.html',{'type':'problem',"subjects":subjects,"islogin":user})

def add_solution(request,problem_id):
    user=islogin(request)
    if user==False:
        return redirect('/login')
    problem=Problem.objects.get(id=problem_id)
    if problem.have_solution:
        return redirect(f'/problems/all/{problem_id}')
    if request.method=='POST':
        if request.FILES.get("sol_video")==None and request.FILES.get("sol_imgs")==None and len(request.POST["text_of_solution"].strip())==0:
            return redirect(f'/add/{problem_id}')
        Solution(problem=problem,solution_path_video=request.FILES.get("sol_video"),solution_path_img=request.FILES.get("sol_imgs"),solution_cont=request.POST["text_of_solution"],user_solved=user).save()
        if (user.admin_tag or user.teacher_tag or user.clever_tag) and len(Solution.objects.filter(problem=problem))==1:
            user.point+=3
            if user.point>=50:
                user.clever_tag=1
            user.save()
            problem.have_solution=True
            problem.save()
        return redirect(f'/problems/all/{problem.id}')
    return render(request,'add.html',{'type':'solution',"subjects":subjects,"islogin":user})

