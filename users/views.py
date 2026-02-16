from django.shortcuts import get_object_or_404, redirect, render
from .models import CustomUser, TipGuide, TGimages
from .forms import CustomUserCreationForm, NewUserForm, SignInForm, CustomUserChangeForm, ForgotPassForm
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
import random
import string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from Shop.models import ShopDetails
from AuditTrail.models import AuditLog
# sign in view


def index(request):
    
    shop_details = ShopDetails.objects.first()
    signInForm = SignInForm()
    signUpForm = CustomUserCreationForm()
    page_name = "index"
    message = ""

    if request.method == "POST":
        signInForm = SignInForm(request.POST)

        # if valid
        if signInForm.is_valid():
            user = authenticate(
                username=signInForm.cleaned_data['username'],
                password=signInForm.cleaned_data['password'],
            )

            # if credentials are valid
            if user is not None:
                login(request, user)



                if user.is_verified:
                    log = AuditLog.objects.create(
                    audit_name=user.username, audit_action="Logged in", audit_module="Login")
                    log.save()

                    if user.role == "customer":
                        return redirect('index')
                    else:
                        return redirect('dashboard')
                else:
                    logout(request)
                    print("Error")

                    message = "Verify email first"
                    

            else:
                print("Error")

                message = "Incorrect username or password."

        else:
            signInForm = SignInForm()
            message = "Invalid values"

    return render(request, 'index.html', context={'form': signInForm, 'err': message, 'form2': signUpForm, 'page_name': page_name, 'shop_details': shop_details})


# logout
@login_required
def logout_view(request):

    logout(request)

    return redirect('index')


# For user registration / sign up
def sign_up(request):
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    token = ''.join(random.choice(allowed_chars) for _ in range(32))

    # render user creation form on the template
    signUpForm = CustomUserCreationForm()

    # give password field design bypass
    signUpForm.fields['password1'].widget.attrs.update({
        'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
        'placeholder': " ",
        'minlength': "8"
    })
    signUpForm.fields['password2'].widget.attrs.update({
        'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
        'placeholder': " ",
        'minlength': "8"
    })

    # if the user creation form has been sent
    if request.method == "POST":
        signUpForm = CustomUserCreationForm(request.POST)

        if signUpForm.is_valid():
            signUpForm.role = "customer"
            email = signUpForm.cleaned_data['email']
            username = signUpForm.cleaned_data['username']
            # random token for email verification
            newuser = signUpForm.save(commit=False)

            newuser.token = token

            newuser.save()

            # send email
            send_mail(
                "Account Activation for LZ Fishing Grounds",
                "Click this button to activate and verify your account.",
                "LZ.Fishing.Grounds@gmail.com",
                [str(email)],
                fail_silently=False,
                html_message=f"<h3 style='margin:20px 0;'> Verify account now </h3><a href='https://lz-fishing-grounds-sys.onrender.com/users/verify/{username}/{token}/' style='background:royalblue; text-transform:uppercase; border-radius: 3px; box-shadow: 0 1px 1px grey; color: white; padding:5px; text-decoration: none;' > Verify Account </a>",
            )
            return redirect('email_sent')

        else:

            print(signUpForm.errors)
            signUpForm.fields['password1'].widget.attrs.update({
                'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
                'placeholder': " ",
                'minlength': "8"
            })
            signUpForm.fields['password2'].widget.attrs.update({
                'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
                'placeholder': " ",
                'minlength': "8"
            })

    context = {
        'form': signUpForm
    }

    return render(request, 'users/signup.html', context)


# successfull sign up and email verification page
def email_sent_page(request):

    return render(request, 'users/email_sent.html')

# successfull sign up and email verification page
def email_sent_forgot(request):

    return render(request, 'users/email_sent_forgot.html')

# successfull sign up and email verification page
def verify_email(request, token, username):
    success = False
    
    users = CustomUser.objects.filter(username=username)
    
    for user in users:
        if user.token == token and not user.is_verified:
            success = True
            user.is_verified = True
            user.save()
    
    context = {
        'success': success,
    }
    
    return render(request, 'users/email_verification.html', context)

# successfull sign up and email verification page
def reset_password(request, uid, token):
    
    success = False
    err = ""
    
    user = CustomUser.objects.get(id=uid)
    form = SetPasswordForm(user)
    
    if user.token == token:
        success = True
        

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        
        if form.is_valid():
            
            curr_user = form.save()
            update_session_auth_hash(request, curr_user)
            user.token == "asdasdasdasd"
            user.save()
            
            messages.add_message(request, messages.SUCCESS, "Password has been reset.")
            return redirect('index')
    
    context = {
        'success': success,
        'form': form,
        'err': err
    }
    
    return render(request, 'users/reset_password.html', context)


# User management view
@login_required
def management(request):
    # users object
    users = CustomUser.objects.all().order_by('-id')

    if request.GET.get("search"):
        if request.GET.get("search") is not None:

            search = request.GET.get("search")
            users = CustomUser.objects.filter(Q(username__icontains=search) | Q(
                email__icontains=search) | Q(last_name__icontains=search)).order_by('-id')
    page = "user_management"

    # pagination
    paginator = Paginator(users, 5)  # shows 4 users per page

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    # variables rendered to the template
    context = {
        'page_name': page,
        'users': users,
        'page_obj': page_obj,
        'page_char': 'a' * page_obj.paginator.num_pages
    }

    return render(request, 'user_management/index.html', context)

# User management view_all

@login_required
def view_all(request):
    # users object
    users = CustomUser.objects.all().order_by('-id')

    page = "user_management"

    # variables rendered to the template
    context = {
        'page_name': page,
        'users': users,
    }

    return render(request, 'user_management/view_all.html', context)


# add user page
@login_required
def new_user_page(request):
    new_user_form = NewUserForm()

    if request.method == "POST":
        new_user_form = NewUserForm(request.POST)

        if new_user_form.is_valid():
            new = new_user_form.save(commit=False)
            new.is_verified = True
            new.save()
            
            log = AuditLog.objects.create(audit_name=request.user.username, audit_action="Added new user", audit_module="Users Management")
            log.save()
            messages.add_message(request, messages.SUCCESS, "New user has been registered successfully.")
            
            # return redirect('user_management')

        else:
            messages.add_message(request, messages.ERROR,
                                 "Error creating user.")

    new_user_form.fields['password1'].widget.attrs.update({
        'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
        'placeholder': " ",
        'minlength': "8"
    })
    new_user_form.fields['password2'].widget.attrs.update({
        'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
        'placeholder': " ",
        'minlength': "8"
    })

    context = {
        'form': new_user_form,
    }

    return render(request, 'user_management/new_user.html', context)


# update user page
@login_required
def update_user_page(request, id):
    # user = CustomUser.objects.get(id=id)

    obj = get_object_or_404(CustomUser, id=id)

    form = CustomUserChangeForm(request.POST or None, instance=obj)

    if request.method == "POST":

        if form.is_valid():

            form.save()
            log = AuditLog.objects.create(audit_name=request.user.username, audit_action="Updated a user", audit_module="Users Management")
            log.save()
            
            return redirect('user_management')

        else:

            print(form.errors)

    context = {
        'form': form
    }

    return render(request, 'user_management/update_user.html', context)


def forgot_pass(request):
    form = ForgotPassForm()
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    token = ''.join(random.choice(allowed_chars) for _ in range(32))
    
    
    if request.method == "POST":
        form = ForgotPassForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.filter(email=email)[:1]
            
            print(token)
            for i in user:
                i.token = token
                i.save()
                # send email
                
                send_mail(
                    "Account Activation for LZ Fishing Grounds",
                    "Click this button to activate and verify your account.",
                    "LZ.Fishing.Grounds@gmail.com",
                    [str(email)],
                    fail_silently=False,
                    html_message=f"<h3 style='margin:20px 0;'> Click the link to reset your password. </h3><a href='https://lz-fishing-grounds-sys.onrender.com/users/forgot_password/{i.id}/{token}/' style='background: teal; text-transform:uppercase; border-radius: 3px; box-shadow: 0 1px 1px grey; color: white; padding:5px; text-decoration: none;' > Reset Password </a>",
                )
                
                
                
                return redirect('email_sent_forgot')
                   
    context = {
        'form': form
    }
    return render(request, "users/forgot_password.html", context)



def reach_us(request):
    shop_details = ShopDetails.objects.get(id=1)
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        send_mail(
        f"{first_name} {last_name} is Reaching out to us.",
        "",
        f"{email}",
        [shop_details.email,],
        fail_silently=False,
        html_message=f"<h3 style='margin:20px 0;'> {message} </h3>",                
        )
    
    return redirect('index')




def tips_guides(request):
    
    tips_guides = TipGuide.objects.all()
    
    images = TGimages.objects.all()
    
    context = {
        'tips_guides': tips_guides,
        'images': images,
    }
    
    return render(request, 'tipsguide.html', context)

def profile(request):
    
    user = request.user
    
    context = {
        'user': user,
  
    }
    
    return render(request, 'profile.html', context)


def change_password(request):
    form = PasswordChangeForm(request.user)
    
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            curr_user = form.save()
            update_session_auth_hash(request, curr_user)
            messages.add_message(request, messages.SUCCESS, "Password has been changed!.")
            
            log = AuditLog.objects.create(audit_name=request.user.username, audit_action="Changed Password", audit_module="Profile")
            log.save()
            
            return redirect('logout')
    context = {
        'form': form
    }
    return render(request, "users/change_password.html", context)



def terms_conditions(request):
    
    
    return render(request, "users/terms.html")
    




