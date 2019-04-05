from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from PyPDF2 import PdfFileWriter, PdfFileReader
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
import uuid
from .forms import UserManagementForm ,UserAccountForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from mailer import Mailer
from mailer import Message
from pdfcon.models import PdfFile

class CreateAccount(View):
    def get(self,request):
        # form = UserAccountForm()
        try:
            first_name = request.GET['first_name']
            email = request.GET['email']
            last_name = request.GET['last_name'] 
            context = {'email' : email,'first_name':first_name,'last_name':last_name}
            return render(request,'registration.html',context)
        except Exception as err:
            messages.add_message(request, messages.INFO, 'User already exists')
            return render(request,'registration.html')

    def post(self,request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if not User.objects.filter(email=email).exists():
            if password and email is not None:
                if password == confirm_password:
                    user = User.objects.create(username=email ,first_name=first_name,last_name=last_name,email=email, password=password)
                    user.set_password(password)
                    user.save()
                else:
                    print('password and confirm password does not match')
            return HttpResponseRedirect('/login')
        return HttpResponseRedirect('/create/account')
        
class Email:
    def sendMail(title,body,frm,email):
        try:
            email = EmailMessage(title, body, frm,to=[email])
            email.send()
            return True
        except Exception as err:
            return False 

class ManageUser(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ManageUser, self).dispatch(request, *args, **kwargs)

    def get(self,request):
        form = UserManagementForm()
        return render(request,'manage_user.html',{'management':form})

    def post(self,request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name'] 
        email = request.POST['email']
        
        if first_name and last_name and email is not None:
            frm = 'aarti@thoughtwin.com'
            # body = "Hi"+ first_name + "Welcome to Mapitron.Please go to link"
            body = "Hi"+" "+ first_name +" "+" <a href=http://127.0.0.1:8000/create/account?email="+email+"&first_name="+first_name+"&last_name="+last_name+">Go to this link</a>"
            
            if Email.sendMail("Invitation",body,frm,email) is True:
                messages.add_message(request, messages.INFO, 'Mail Sent Successfully')
            else:
                messages.add_message(request, messages.INFO, 'Error while sending email')
        return HttpResponseRedirect('/manage/user')
            
class LoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard')
        else:
            return render(request,'login.html')
        
    def post(self,request):
        msg = ''
        response = {}
        username = request.POST['username']
        password = request.POST['password'] 
        if username and password is not None:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/dashboard')
            else:
                msg = "Incorrect username and password"
                response['msg']=msg
                print(response)
                return render(request,'login.html',{'res':response})
        else:
            msg = "Please fill the form"
            response['msg']=msg
            print(response)
        return render(request,'login.html',{'res':response})

class LogoutView(View):
    def get(self,request):
        if request.user.username:
            logout(request)
            return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('/login')
    
class DashboardView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request,'dashboard.html')
        else:
            return HttpResponseRedirect('/login')

    def post(self,request):
        # import pdb; pdb.set_trace()
        pdf_list = []
        inputpdf = PdfFileReader(open("/home/hp/projects/django/convertor/convert/pdfcon/file2.pdf", "rb"))
        for i in range(inputpdf.numPages):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            new_pdf = uuid.uuid4()
            with open(str(new_pdf)+".pdf", "wb") as outputStream:
                pdf = output.write(outputStream)
                pdf_list.extend(str(new_pdf)+".pdf")
        # print(pdf_list)
        store_pdf = PdfFile.objects.create(file=str(new_pdf)+".pdf")
        return HttpResponseRedirect('/dashboard')

class PdfList(View):
    def get(self,request):
        pdf = PdfFile.objects.all()
        return render(request,'pdf_list.html',{'pdf_list':pdf})
        
class ChangePassword(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request,'dashboard.html')
        else:
            return render(request,'change_password.html')

    def post(self,request):
        old_password = request.POST['old_password']
        email = request.POST['email']
        try:
            user  = User.objects.get(email=email)
            if old_password is not None:
                if authenticate(username=user,password=old_password) is not None:
                    new_password = request.POST['new_password']
                    confirm_password = request.POST['confirm_password']
                    if new_password == confirm_password:
                        user.set_password(new_password)
                        user.save()
                        messages.add_message(request, messages.INFO, 'Password changed Successfully')
                    else:
                        messages.add_message(request, messages.INFO, 'New password and confirm password does not match')
                else:
                    messages.add_message(request, messages.INFO, 'Authentication fail')
            return render(request,'change_password.html')
        except Exception as err:
            messages.add_message(request, messages.INFO, 'Wrong email id')
            return HttpResponseRedirect('/change/password')
    