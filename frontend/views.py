from django.shortcuts import render

# Create your views here.

def consume_registration(request):
    context={}
    return render(request,'registration.html',context)
   


def consume_login(request):
    context={}
    return render(request,'login.html',context)


def Dashboard(request):
    return render(request,'dashboard.html')


def Home(request):
    return render(request,'home.html')


def Employee_creation(request):
    return render(request,'creatingEmployee.html')

def Updating_employee(request,id):
    context={'employee_id':id}
    return render(request,'updatingEmployee.html',context)

def role_Data(request):
    return render(request,'role.html')

def update_Role(request,id):
    print('id--',id)
    return render(request,'updateRole.html',{'employee_id': id})

def Attendance_data(request):
    return render(request,'attendance.html')