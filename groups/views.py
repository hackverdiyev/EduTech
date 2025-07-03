from django.shortcuts import render,redirect
from problems.models import *
from groups.models import *
from base.models import *
from base.views import subjects

def islogin(request):
    if 'username' in request.session:
        return Account.objects.get(username=request.session['username'])
    return False

def groups_main(request):
    user=islogin(request)
    if user==False:
        return redirect('/login')
    if request.method=='POST':
        if 'enter' in request.POST:
            return redirect(f'/groups/{request.POST["enter"]}')
        if 'join' in request.POST:
            user.requests=user.requests.replace(f'%{request.POST["join"]}%','%')
            user.groups+=f'{request.POST["join"]}%'
            user.save()
            g=Group.objects.get(id=request.POST["join"])
            g.requests=g.requests.replace(f'%{user.id}%','%')
            g.participants+=f'{user.id}%'
            g.save()
            return redirect(f'/groups/{request.POST["join"]}')
        if 'deny' in request.POST:
            user.requests=user.requests.replace(f'%{request.POST["deny"]}%','%')
            user.save()
            g=Group.objects.get(id=request.POST["deny"])
            g.requests=g.requests.replace(f'%{user.id}%','%')
            g.save()
            return redirect(f'/groups')
        if 'leave' in request.POST:
            if Group.objects.get(id=request.POST["leave"]).creator==user:
                return redirect(f'/')
            user.groups=user.requests.replace(f'%{request.POST["leave"]}%','%')
            user.save()
            g=Group.objects.get(id=request.POST["leave"])
            g.admins=g.admins.replace(f'%{user.id}%','%')
            g.participants=g.participants.replace(f'%{user.id}%','%')
            g.save()
            return redirect(f'/groups')
    requests=list(map(lambda i:Group.objects.get(id=int(i)),user.requests.split('%')[1:-1]))
    groups=list(map(lambda i:Group.objects.get(id=int(i)),user.groups.split('%')[1:-1]))
    groups.reverse()
    return render(request,'groups_main.html',{"requests":requests,"groups":groups,"subjects":subjects,"islogin":user})

def groups(request,id):
    user=islogin(request)
    if user==False:
        return redirect('/login')
    if f'%{id}%' in user.groups:
        group=Group.objects.get(id=id)
        contests=list(map(lambda i:Contest.objects.get(id=int(i)),group.contests.split('%')[1:-1]))
        admins=list(map(lambda i:Account.objects.get(id=int(i)),group.admins.split('%')[1:-1]))
        participants=list(map(lambda i:Account.objects.get(id=int(i)),group.participants.split('%')[1:-1]))
        requests=list(map(lambda i:Account.objects.get(id=int(i)),group.requests.split('%')[1:-1]))
        if user==group.creator:
            admin=True
        elif user in admins:
            admin=True
            admins.remove(user)
        else:
            admin=False
            participants.remove(user)
        if request.method=='POST':
            if 'delete_group' in request.POST:
                user.groups=user.groups.replace(f'%{group.id}%','%')
                user.save()
                for i in admins:
                    i.groups=i.groups.replace(f'%{group.id}%','%')
                    i.save()
                for i in participants:
                    i.groups=i.groups.replace(f'%{group.id}%','%')
                    i.save()
                for i in requests:
                    i.requests=i.requests.replace(f'%{group.id}%','%')
                    i.save()
                group.delete()
                return redirect('/groups')
            if 'change' in request.POST:
                group.name=request.POST['name']
                group.about=request.POST['about']
                group.subject=request.POST['subject']
                group.save()
                return render(request,'groups.html',{"group":group,"admin":admin,"contests":contests,"admins":admins,"participants":participants,"requests":requests,'default':4,'success':1,"subjects":subjects,"islogin":user})
            if 'user_request' in request.POST:
                x=Account.objects.filter(username=request.POST["user_request"])
                if len(x)==0:
                    return render(request,'groups.html',{"group":group,"admin":admin,"contests":contests,"admins":admins,"participants":participants,"requests":requests,'default':2,"error":1,"subjects":subjects,"islogin":user})
                x=x[0]
                if x==group.creator or f'%{x.id}%' in group.admins or f'%{x.id}%' in group.participants or f'%{x.id}%' in group.requests:
                    return render(request,'groups.html',{"group":group,"admin":admin,"contests":contests,"admins":admins,"participants":participants,"requests":requests,'default':2,"error":2,"subjects":subjects,"islogin":user})
                x.requests+=f'{group.id}%'
                x.save()
                group.requests+=f'{x.id}%'
                group.save()
                requests.append(x)
                return render(request,'groups.html',{"group":group,"admin":admin,"contests":contests,"admins":admins,"participants":participants,"requests":requests,'default':2,'success':2,"subjects":subjects,"islogin":user})
            if 'create_contest' in request.POST:
                problems_list=request.POST['problems'].split(',')
                problems='%'
                for i in problems_list:
                    if len(Problem.objects.filter(id=int(i.strip())))>0:
                        problems=f'{problems}{i.strip()}%'
                x=Contest(name=request.POST['name'],group=group,creator=user,problems=problems)
                x.save()
                group.contests+=f'{x.id}%'
                group.save()
                contests.append(x)
                return redirect(f'/groups/{group.id}/contests/{x.id}')
            if 'delete_request' in request.POST:
                group.requests=group.requests.replace(f'%{request.POST["delete_request"]}%','%')
                x=Account.objects.get(id=int(request.POST["delete_request"]))
                x.requests=x.requests.replace(f'%{group.id}%','%')
                x.save()
                group.save()
                requests.remove(x)
                return render(request,'groups.html',{"group":group,"admin":admin,"contests":contests,"admins":admins,"participants":participants,"requests":requests,'default':2,'success':3,"subjects":subjects,"islogin":user})
            if 'delete_participant' in request.POST:
                group.participants=group.participants.replace(f'%{request.POST["delete_participant"]}%','%')
                x=Account.objects.get(id=int(request.POST["delete_participant"]))
                x.groups=x.groups.replace(f'%{group.id}%','%')
                x.save()
                group.save()
                participants.remove(x)
                return render(request,'groups.html',{"group":group,"admin":admin,"contests":contests,"admins":admins,"participants":participants,"requests":requests,'default':2,'success':3,"subjects":subjects,"islogin":user})
            if 'delete_admin' in request.POST:
                group.admins=group.admins.replace(f'%{request.POST["delete_admin"]}%','%')
                x=Account.objects.get(id=int(request.POST["delete_admin"]))
                x.groups=x.groups.replace(f'%{group.id}%','%')
                x.save()
                group.save()
                admins.remove(x)
                return render(request,'groups.html',{"group":group,"admin":admin,"contests":contests,"admins":admins,"participants":participants,"requests":requests,'default':2,'success':3,"subjects":subjects,"islogin":user})
            if 'increase' in request.POST:
                x=Account.objects.get(id=int(request.POST["increase"]))
                group.participants=group.participants.replace(f'%{x.id}%','%')
                group.admins+=f'{x.id}%'
                group.save()
                participants.remove(x)
                admins.append(x)
                return render(request,'groups.html',{"group":group,"admin":admin,"contests":contests,"admins":admins,"participants":participants,"requests":requests,'default':2,'success':4,"subjects":subjects,"islogin":user})
            if 'decrease' in request.POST:
                x=Account.objects.get(id=int(request.POST["decrease"]))
                group.admins=group.admins.replace(f'%{x.id}%','%')
                group.participants+=f'{x.id}%'
                group.save()
                participants.append(x)
                admins.remove(x)
                return render(request,'groups.html',{"group":group,"admin":admin,"contests":contests,"admins":admins,"participants":participants,"requests":requests,'default':2,'success':5,"subjects":subjects,"islogin":user})
        return render(request,'groups.html',{"group":group,"admin":admin,"contests":contests,"admins":admins,"participants":participants,"requests":requests,'default':1,"subjects":subjects,"islogin":user})
    return redirect('/groups')

def contests(request,id,contest_id):
    user=islogin(request)
    if user==False:
        return redirect('/login')
    if f'%{id}%' in user.groups:
        contest=Contest.objects.get(id=contest_id)
        problems=list(map(lambda i:Problem.objects.get(id=int(i)),contest.problems.split('%')[1:-1]))
        if request.method=='POST':
            if len(request.POST["message"].strip())>0:
                Discussion(message=request.POST["message"].strip(),contest=contest,user_added=user).save()
                return redirect(f'/groups/{id}/contests/{contest_id}')
        messages=Discussion.objects.filter(contest=contest).order_by('-date')
        return render(request,'problems.html',{"contest":contest,"problems":problems,"messages":messages,"subjects":subjects,"islogin":islogin(request)})
    return redirect('/groups')

def create_group(request):
    user=islogin(request)
    if user==False:
        return redirect('/login')
    if request.method=='POST':
        g=Group(name=request.POST["name"],about=request.POST["about"],subject=request.POST["subject"],creator=user)
        g.save()
        user.groups+=f'{g.id}%'
        user.save()
        return redirect('/groups')
    return render(request,'create_group.html',{"subjects":subjects,"islogin":user})
