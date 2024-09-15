from django.shortcuts import render

# Create your views here.

def consume_registration(request):
    context={}
    return render(request,'registration.html',context)
   


def consume_login(request):
    context={}
    return render(request,'login2.html',context)


def Dashboard(request):
    return render(request,'dashboard.html')


def Home(request):
    return render(request,'home.html')

