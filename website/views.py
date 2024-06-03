from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth import authenticate, login , logout 
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib import messages
from .forms import SignUpForm , AddRecordForm
from .models import Records

# Create your views here.


def home(request):
    Datas = Records.objects.all()
    if request.method == "POST":
        uName = request.POST.get('UserName')
        passd = request.POST.get('PASS')
        # return HttpResponse(uName+"  "+passd)
        
        user = authenticate(request, username=uName, password = passd)
        # return HttpResponse(user)
        if user is not None:
            login(request,user)
            messages.success(request,"You have login Successfully")
            return redirect('home')
        else:
            messages.success(request,'There some thing Error loging this with User Name and Password')
            return redirect('home')
    else:

        return render(request,'home.html',{'Records':Datas})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, ' You have been logout........')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username , password=password)
            login(request,user)
            messages.success(request, 'You have registred successfully') 
            return redirect('home')
    else:    
        form = SignUpForm()
        return render(request, 'register.html',{'form':form})
    return render(request, 'register.html',{'form':form})

def customer_record(request,pk):
    if request.user.is_authenticated:
       customer_data = Records.objects.get(id=pk)
       return render(request, 'record.html',{'customer_data':customer_data})
    else:
        messages.success(request, 'You have to login First') 
        return redirect('home')

def delete_record(request,pk):    
    if request.user.is_authenticated:
        delete_data = Records.objects.get(id=pk)
        delete_data.delete()
        messages.success(request,"You have Deleted successfully") 
        return redirect('home')
    else:
        messages.success(request, 'You have to login First') 
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request,"Record Added successfully" ) 
                return redirect('home')
        return render(request,'add_record.html',{'form':form})  
    else:
        messages.success(request, 'You have to login First') 
        return redirect('home')
    
def update_record(request,pk):
   
        if request.user.is_authenticated:
            current_record = Records.objects.get(id=pk)
            form = AddRecordForm(request.POST or None, instance=current_record)
            if form.is_valid():
                form.save()
                messages.success(request,"Record Updated successfully" )
                return redirect('home') 
            return render(request,'update.html',{'form':form})
        else:
            messages.success(request, 'You have to login First') 
            return redirect('home')
    