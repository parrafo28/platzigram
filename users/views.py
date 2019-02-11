from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.db.utils import IntegrityError

from django.contrib.auth.models import User
from users.models import Profile

from users.forms import ProfileForm

def login_view(request):
    if(request.method=='POST'):
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if(user):
            login(request,user)
            return redirect('feed')
        else:
            return render(request,'users/login.html',{'error':'invalid username or password'})
    return render(request,'users/login.html')

def signup_view(request):
    if(request.method=='POST'):
        if(request.POST['password']!=request.POST['password_confirmation']):
            return render(request,'users/signup.html',{'error':'password confirmation does not match'})
        try:
            user=User.objects.create_user(username=request.POST['username'],password=request.POST['password'])
        except IntegrityError:
            return render(request,'users/signup.html',{'error':'username already in use'})

        user.firstname=request.POST['first_name']
        user.lastname=request.POST['last_name']
        user.email=request.POST['email']
        user.save()
        
        profile=Profile(user=user)
        profile.save()
    return render(request,'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def update_profile(request):
    profile=request.user.profile
    if(request.method=='POST'):
        form=ProfileForm(request.POST,request.FILES)
        if(form.is_valid()):
            data=form.cleaned_data

            profile.website=data['website']
            profile.phone_number=data['phone_number']
            profile.biography=data['biography']
            profile.picture=data['picture']
            profile.save()

            return redirect('update_profile')
    else:
        form=ProfileForm()
    return render(request,'users/update_profile.html',context={
        'profile':profile,
        'user':request.user,
        'form':form
    })