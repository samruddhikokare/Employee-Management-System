from django.shortcuts import render, HttpResponse
from .models import Employee,Role,Department
from datetime import datetime
from django.db.models import Q
def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps':emps
    }
    print(context)
    return render(request, 'view_all_emp.html',context)

def add_emp(request):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            dept_id = request.POST.get('Department')
            role_id = request.POST.get('Role')
            salary = request.POST.get('Salary')
            hire_date = request.POST.get('Hire_Date')
            phone = request.POST.get('Phone')

            # check required fields
            if not all([first_name, last_name, dept_id, role_id, salary, phone]):
                return HttpResponse("All fields are required")

            # create employee
            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                salary=int(salary),
                dept_id=dept_id,   # foreign key
                role_id=role_id,         # foreign key
                phone=phone,
                hire_date=datetime.now() # or parse hire_date if needed
            )
            new_emp.save()
            return HttpResponse("Employee added successfully")

        except Exception as e:
            return HttpResponse(f"An exception occurred: {e}")

    elif request.method == 'GET':
        context = {
            'departments': Department.objects.all(),
            'roles': Role.objects.all()
        }
        return render(request, "add_emp.html", context)
    else:
        return HttpResponse("Invalid request method")



def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse(f"Employee {emp_to_be_removed.first_name} removed successfully")
        except Employee.DoesNotExist:
            return HttpResponse("Please enter a valid emp_id")

    emps = Employee.objects.all()
    return render(request, 'remove_emp.html', {'emps': emps})



def filter_emp(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        dept = request.POST.get('dept', '')
        role = request.POST.get('role', '')

        emps = Employee.objects.all()

        if name:
            emps = emps.filter(first_name__icontains=name) | emps.filter(last_name__icontains=name)
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)

        context = {"emps": emps}
        return render(request, "view_all_emp.html", context)

    # For GET request, just return empty filter form
    return render(request, "filter_emp.html")




