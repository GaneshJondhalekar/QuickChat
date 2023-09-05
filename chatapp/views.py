from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

from .form import UserForm,ProfileUpdateForm
from django.contrib.auth.models import User
from .models import UserProfile,FriendRequest,ChatMessage
# Create your views here.
@login_required
def Index(request):
    user=request.user
    friends=user.profile.friends.all()
    context={'friends':friends}
    return render(request,'chats.html',context)

def Login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)
        user=authenticate(request,username=username,password=password)
        print(user)
        if user:
            login(request,user)
            return redirect('index')
        else:
            return render(request,'login.html',{'msg':'Username or Password is Invalid'})
    return render(request,'login.html')

def Register(request):
    form=UserForm()
    if request.method=="POST":
        #form=CustomUserCreationForm(request.POST)
        form=UserForm(request.POST)
        email=request.POST.get('email')
        if form.is_valid():
            user=form.save()
            user.username=form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
        return render(request,'signup.html',{'msg':form.errors})
    context={'form':form}
    return render(request,'signup.html',context=context)

def Logout(request):
    logout(request) 
    return redirect('login')

@login_required
def update_profile(request):
    user=request.user
    profile=UserProfile.objects.get(user=user)
    form=ProfileUpdateForm(instance=profile)
    context={'form':form}
    if request.method=='POST':
        form=ProfileUpdateForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            user.first_name=form.cleaned_data['first_name']
            user.last_name=form.cleaned_data['last_name']
            user.email=form.cleaned_data['email']
            user.save()
            form.save()
            return redirect('index')
        context['msg']=form.errors
        return render(request,'update_profile.html',context=context)
    
    return render(request,'update_profile.html',context=context)


@login_required
def suggestion(request):
    user=request.user
    profile=UserProfile.objects.get(user=user)
    friends=profile.friends.all()
    friend_ids = friends.values_list('id', flat=True)
    #show suggettions- show all users to login user excludes his friends,self and superuser
    suggested_profiles=User.objects.exclude(id__in=friend_ids).exclude(profile=profile).exclude(is_staff=True)
    #login user have made following friend requests to suggetions shown on page 
    f_requests=FriendRequest.objects.filter(receiver__in=suggested_profiles,sender=user)
    #login user have following requests
    friend_requests=FriendRequest.objects.filter(receiver=request.user)

    context={'suggestions':suggested_profiles,'f_requests':f_requests,'friend_requests':friend_requests}
    return render(request,'notifications.html',context)

@login_required
def send_friend_request(request,id):
    receiver=User.objects.get(pk=id)
    sender=request.user
    FriendRequest.objects.create(sender=sender,receiver=receiver,status='PENDING')
    return redirect('notifications')

@login_required
def cancel_request(request,id):
    receiver=User.objects.get(pk=id)
    sender=request.user
    FriendRequest.objects.filter(sender=sender,receiver=receiver).delete()
    return redirect('notifications')

@login_required
def accept_friend_request(request,id):
    sender=User.objects.get(pk=id)
    receiver=request.user
    sender.profile.friends.add(receiver)
    receiver.profile.friends.add(sender)
    FriendRequest.objects.get(sender=sender,receiver=receiver).delete()
    return redirect('notifications')

@login_required
def chat_window(request,user_id):
    sender=request.user
    receiver=User.objects.get(pk=user_id)
    received_messages=list(request.user.received_messages.filter(sender=receiver))
    sent_messages=list(request.user.sent_messages.filter(receiver=receiver))
    all_messages=received_messages+sent_messages
    all_messages.sort(key=lambda x:x.timestamp)

    return render(request,'chat_window.html', {"other_user_id": user_id,'all_messages':all_messages})

