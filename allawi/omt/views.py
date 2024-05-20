from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.utils import timezone
from django.core.mail import EmailMessage
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.db.models import Sum


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('review_cvs')
            elif Employee.objects.filter(name=user).exists():
                employee = Employee.objects.get(name=user)
                employee.login()
                return redirect('home_employee')
            elif Customer.objects.filter(name=user).exists():
                return redirect('home_customer')
            else:
                error_message = "Invalid user role."
                return render(request, 'login.html', {'error_message': error_message})
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        age = request.POST['age']
        nationality = request.POST['nationality']
        worth = request.POST['worth']
        if username == '' or email == '' or password == '' or confirm_password == '' or age == 0 or nationality == '' or worth ==0:
            error_message_fill = "Fill out all the fields..."
            return render(request, 'register.html', {'error_message_fill': error_message_fill})
        else:
            if User.objects.filter(username=username).exists():
                error_message_user = "Username is already taken..."
                return render(request, 'register.html', {'error_message_user': error_message_user})
            else:
                if len(password)<8:
                    error_message_len = "Password should be longer than 8 characters..."
                    return render(request, 'register.html', {'error_message_len': error_message_len})
                else:
                    if password != confirm_password:
                        error_message_pass = "Make sure passwords match..."
                        return render(request, 'register.html', {'error_message_pass': error_message_pass})
                    else:
                        u = User.objects.create_user(username=username, email=email, password=password)
                        Customer.objects.create(name=u, age=age, email= email,  nationality=nationality, worth=worth)
                        # Perform registration logic here
                        return redirect('login')
    else:
        return render(request, 'register.html')


@login_required(login_url='login')
def home_employee(request):
    # Perform home page logic here

    return render(request, 'homeEmployee.html')

@login_required(login_url='login')
def home_customer(request):
    customer = Customer.objects.get(name=request.user)
    return render(request, 'homeCustomer.html', {'customer':customer})
@login_required(login_url='login')
def home_customer_wallet(request):
    customer = Customer.objects.get(name=request.user)

    if Wallet.objects.filter(user=customer).exists():
        balance = Wallet.objects.get(user=customer)
        return render(request, 'homeCustomerWallet.html', {'customer': customer, 'balance': balance})
    else:
        new = True
        return render(request, 'homeCustomerWallet.html', {'customer': customer, 'new': new})
@login_required(login_url='login')
def home_customer_wallet_new(request):
    customer = Customer.objects.get(name=request.user)
    if request.method=='POST':
        balance = request.POST['balance']
        if balance=='' or balance==0:
            error_message = "● You cannot create an empty wallet..."
            return render(request, 'homeCustomerWalletNew.html', {'error_message':error_message, 'customer':customer})
        else:
            Wallet.objects.create(user=customer, balance=balance)
            return render(request, 'homeCustomer.html', {'customer': customer})
    else:
        return render(request, 'homeCustomerWalletNew.html', {'customer': customer})




def base_view(request):
    return render(request, 'base.html')

print("Outside")

def apply(request):
    print("Hey")
    if request.method == 'POST':
        print("Hello")
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        experience = request.POST.get('experience')
        education = request.POST.get('education')
        profile = request.POST.get('profile')
        if name == '' or email == '' or password == '' or confirm_password == '' or age == 0 or age == '' or experience == 0 or experience == '' or education == '' or profile == '':
            error_message_fill = "Fill out all the fields..."
            return render(request, 'apply.html', {'error_message_fill': error_message_fill})
        else:
            if User.objects.filter(username=name).exists():
                error_message_user = "Username is already taken..."
                return render(request, 'apply.html', {'error_message_user': error_message_user})
            else:
                if len(password) < 8:
                    error_message_len = "Password should be longer than 8 characters..."
                    return render(request, 'apply.html', {'error_message_len': error_message_len})
                else:
                    if password != confirm_password:
                        error_message_pass = "Make sure passwords match..."
                        return render(request, 'apply.html', {'error_message_pass': error_message_pass})
                    else:
                        EmployeeCV.objects.create(name=name, email=email, experience=experience, age=age, password=password, education=education, profile=profile)
                        return redirect('success')
    else:
        print("Now Way")
        return render(request, 'apply.html')

@login_required(login_url='login')
def transfer_view(request):
    customer = Customer.objects.get(name=request.user)
    print(customer)
    if request.method == 'POST':
        account = request.POST['account']
        money = request.POST['transfer-money']
        wallet = Wallet.objects.get(user=customer)

        if account == '' or money == 0 or money == '':
            error_message = "Please enter both fields..."
            return render(request, 'homeCustomerTransfer.html', {'customer': customer, 'error_message': error_message})
        else:
            print(money)
            print(wallet.balance)
            if int(money) > wallet.balance:
                error_message = "You don't have enough money in your wallet..."
                return render(request, 'homeCustomerTransfer.html', {'customer': customer, 'error_message': error_message})
            else:
                if User.objects.filter(email=account).exists():
                    toUser = Customer.objects.get(email=account)
                    if Wallet.objects.filter(user = toUser).exists():
                        masari = Wallet.objects.get(user = toUser)
                        masari.balance = masari.balance+int(money)
                        masari.save()
                        wallet.balance = wallet.balance - int(money)
                        wallet.save()
                        Transaction.objects.create(sender=customer.email, receiver=toUser.email, amount=money)
                        success_message = "Money transferred successfully!"
                        return render(request, 'homeCustomerTransfer.html',
                                      {'customer': customer, 'success_message': success_message})
                    else:
                        error_message = "Account has no wallet..."
                        return render(request, 'homeCustomerTransfer.html',
                                      {'customer': customer, 'error_message': error_message})
                else:
                    error_message = "The account under this email does not exist..."
                    return render(request, 'homeCustomerTransfer.html', {'customer': customer, 'error_message': error_message})
    else:
        if Wallet.objects.filter(user=customer).exists():
            new = False
            return render(request, 'homeCustomerTransfer.html', {'customer': customer, 'new': new})
        else:
            new = True
            return render(request, 'homeCustomerTransfer.html', {'customer': customer, 'new': new})

@login_required(login_url='login')
def deposit_view(request):
    customer = Customer.objects.get(name=request.user)
    if request.method=='POST':
        amount = request.POST['deposit']
        if amount=='' or amount==0:
            error_message = "Please enter a valid amount..."
            return render(request, 'homeCustomerDeposit.html', {'customer': customer, 'error_message':error_message})
        else:
            wallet = Wallet.objects.get(user=customer)
            wallet.balance = wallet.balance + int(amount)
            wallet.save()
            success_message = "Money added successfully!"
            return render(request, 'homeCustomerDeposit.html', {'customer' : customer, 'success_message': success_message})
    else:
        if Wallet.objects.filter(user=customer).exists():
            new = False
            return render(request, 'homeCustomerDeposit.html', {'customer': customer, 'new': new})
        else:
            new = True
            return render(request, 'homeCustomerDeposit.html', {'customer': customer, 'new': new})
@login_required(login_url='login')
def withdraw_view(request):
    customer = Customer.objects.get(name=request.user)
    if request.method == 'POST':
        amount = request.POST['withdraw']
        if amount == '' or amount == 0:
            error_message = "Please enter a valid amount..."
            return render(request, 'homeCustomerWithdraw.html', {'customer': customer, 'error_message': error_message})
        else:
            wallet = Wallet.objects.get(user=customer)
            if wallet.balance < int(amount):
                error_message = "You do not have enough funds..."
                return render(request, 'homeCustomerWithdraw.html', {'customer': customer, 'error_message': error_message})
            else:
                if int(amount)<0:
                    error_message = "You can't withdraw a negative amount..."
                    return render(request, 'homeCustomerWithdraw.html',
                                  {'customer': customer, 'error_message': error_message})
                else:
                    wallet.balance = wallet.balance - int(amount)
                    wallet.save()
                    success_message = "Money withdrawn successfully!"
                    return render(request, 'homeCustomerWithdraw.html',
                            {'customer': customer, 'success_message': success_message})
    else:
        if Wallet.objects.filter(user=customer).exists():
            new = False
            return render(request, 'homeCustomerWithdraw.html', {'customer': customer, 'new': new})
        else:
            new = True
            return render(request, 'homeCustomerWithdraw.html', {'customer': customer, 'new': new})


def success(request):
    return render(request, 'success.html')

@login_required
def cv_sent(request, cv_id):
    cv = get_object_or_404(EmployeeCV, id=cv_id)
    return render(request, 'cv_sent.html', {'cv': cv})






@login_required
def chatPage(request):
    return render(request, 'chatPage.html')


# @login_required
# def logout(request):
#     if request.user.is_superuser:
#         # Perform logout logic for superuser
#         pass
#     elif Employee.objects.filter(name=request.user).exists():
#         employee = Employee.objects.get(name=request.user)
#         elapsed_time = employee.logout()  # Update working_hours and get elapsed time
#         # Perform logout logic for employee
#         return render(request, 'logout.html', {'elapsed_time': elapsed_time})
#     elif Customer.objects.filter(name=request.user).exists():
#         # Perform logout logic for customer
#         pass
#     else:
#         # Handle other user roles
#         pass
#     return redirect('login')
@login_required
def cv_details(request, cv_id):
    if not request.user.is_superuser:
        return redirect('employee_home')

    employeecvs = EmployeeCV.objects.get(id=cv_id)
    return render(request, 'cv_details.html', {'employeecvs': employeecvs})
@login_required
def review_cvs(request):
    if not request.user.is_superuser:
        return redirect('employee_home')

    cvs = EmployeeCV.objects.filter(is_accepted=False)
    return render(request, 'review_cvs.html', {'cvs': cvs})

@login_required
def accept_cv(request, cv_id):
    if not request.user.is_superuser:
        return redirect('employee_home')

    cv = get_object_or_404(EmployeeCV, id=cv_id)
    cv.is_accepted = True
    cv.save()

    # Create the Employee object with the current date
    u = User.objects.create_user(username=cv.name, email=cv.email, password=cv.password)
    Employee.objects.create(name=u, age=cv.age,
                            experience_years=cv.experience,
                            date_employed=timezone.now())

    from_email = 'munierhaffar@gmail.com'
    # to = cv.email
    subject = 'CV Accepted'
    message = 'Dear {}, your CV has been accepted. Congratulations on the new opportunity!'.format(cv.name)
    email = EmailMessage(subject, message, from_email, to=[cv.email])
    email.send()

    # Delete the EmployeeCV object
    cv.delete()

    # Perform any additional logic or redirect as needed
    return redirect('review_cvs')

@login_required
def reject_cv(request, cv_id):
    if not request.user.is_superuser:
        return redirect('employee_home')

    cv = get_object_or_404(EmployeeCV, id=cv_id)

    from_email = 'munierhaffar@gmail.com'
    # to = cv.email
    subject = 'CV Rejected'
    message = 'Dear {}, we regret to inform you that your CV has been rejected.'.format(cv.name)
    email = EmailMessage(subject, message, from_email, to=[cv.email])
    email.send()


    cv.delete()

    # Perform any additional logic or redirect as needed
    return redirect('review_cvs')

@login_required
def employees_list(request):
    employees = Employee.objects.all()

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee_id = request.POST.get('employee_id')
            position = form.cleaned_data['position']
            salary = form.cleaned_data['salary']
            report = form.cleaned_data['report']

            employee = Employee.objects.get(id=employee_id)

            if employee.position != position:
                # Send promotion email with salary and report information
                subject = f"Congratulations, {employee.name}!"
                message = f"Congratulations on your promotion to {position}!\n\n" \
                          f"Your new salary is {salary}$.\n" \
                          f"Report: {report}"
            else:
                # Send salary and report email
                subject = f"Salary and Report"
                message = f"Your salary is {salary}$.\n" \
                          f"Report: {report}"

            # Save the updated values for the employee
            employee.position = position
            employee.salary = salary
            employee.report = report
            employee.save()

            # Send the email
            send_mail(subject, message, 'munierhaffar@gmail.com', [employee.name.email])

            return redirect('employees_list')

    else:
        form = EmployeeForm()

    context = {
        'employees': employees,
        'form': form,
        'POSITIONS': POSITIONS
    }

    return render(request, 'employees_list.html', context)


@login_required
def fire_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    # Send termination email to the employee
    subject = "Termination Notice"
    message = f"Dear {employee.name},\n\nWe regret to inform you that your employment with our company has been terminated.\n\nThank you for your services.\n\nSincerely,\nThe Management"
    send_mail(subject, message, 'munierhaffar@gmail.com', [employee.name.email])

    # Deactivate the associated User
    user = employee.name
    user.delete()
    # Remove the employee from the company
    employee.delete()

    return redirect('employees_list')

@login_required
def data_view(request):
    # Get the data for the pie chart (applied employees' experience distribution)
    labels = []
    data = []

    queryset = EmployeeCV.objects.order_by('experience')[:5]
    for employee in queryset:
        labels.append(employee.name)
        data.append(employee.experience)



    # Get the data for the line graph (number of applied employees, employees, and customers)
    label1 = ['Applied Employees', 'Employees', 'Customers']
    data1 = [EmployeeCV.objects.count(), Employee.objects.count(), Customer.objects.count()]

    # Get the data for the vertical bar chart (customer worth)
    customers = Customer.objects.all()
    label2 = [customer.name.username for customer in customers]
    data2 = []

    for customer in customers:
        try:
            wallet = Wallet.objects.get(user=customer)
            data2.append(wallet.balance)
        except Wallet.DoesNotExist:
            data2.append(0)


    context = {
        'labels': labels,
        'data': data,
        'label1': label1,
        'data1': data1,
        'label2': label2,
        'data2': data2
    }
    return render(request, 'data.html', context)

def transaction_list(request):
    if request.user.is_superuser:
        transactions = Transaction.objects.all().values('sender', 'receiver', 'amount', 'created_at', 'status')
    else:
        customer = request.user.customer
        transactions = Transaction.objects.filter(models.Q(sender=customer) | models.Q(receiver=customer)).values('sender', 'receiver', 'amount', 'created_at', 'status')

    total_fees = Transaction.objects.aggregate(total_fees=Sum('amount'))['total_fees']
    if total_fees is not None:
        total_fees = total_fees * Decimal('0.02')
    else:
        total_fees = Decimal('0.00')

    transaction_count = Transaction.objects.count()

    context = {
        'transactions': transactions,
        'total_fees': total_fees,
        'transaction_count': transaction_count
    }


    return render(request, 'transaction_list.html', context)

@require_POST
def approve_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    transaction.status = 'APPROVED'
    transaction.save()
    #Send approval message here (e.g., using a messaging library)
    return redirect('transaction_list')

@require_POST
def decline_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    transaction.status = 'REJECTED'
    transaction.save()
    #Send rejection message here (e.g., using a messaging library)
    return redirect('transaction_list')

def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'create_appointment.html', {'form': form})

def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'edit_appointment.html', {'form': form, 'appointment': appointment})

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.delete()
    return redirect('appointment_list')

def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointment_list.html', {'appointments': appointments})

