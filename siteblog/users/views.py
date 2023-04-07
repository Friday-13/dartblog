from django.contrib import messages
from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


from .forms import *
from .models import User, Profile
from .tokens import account_activation_token

def user_logout(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(request.POST.get('next', '/'))


def user_login(request: HttpRequest):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form, 'title': 'Login'})


def user_register(request: HttpRequest):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            return redirect('home')
    else:
        form = UserRegisterForm()
    # print(form.email.widget.attrs)
    return render(request, 'users/register.html', {'form': form, 'title': 'Register', 'formtitle': 'Register form'})


def user_profile_edit(request: HttpRequest):
    if request.method == 'POST':
        user_form = EditUserForm(data=request.POST, instance=request.user)
        profile_form = EditProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Settings have been saved!') 
            return redirect('home')
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', 
                  {'user_form': user_form, 'profile_form': profile_form,
                   'title': 'Edit'})

def activate_email(request, user, to_email):
    mail_subject = 'Activate your account'
    message = render_to_string('users/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    print(email.from_email)
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

class ChangePassword(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('home')
    success_message = f'Password has been saved'

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('home')

class PasswordReset(SuccessMessageMixin, PasswordResetView):
    success_url = reverse_lazy('home')
    success_message = f'Please, check your email. We sent your a letter with next step description'

    form_class = UserPasswordResetForm
    template_name = 'users/password_reset.html' 
    extra_context = {'formtitle': 'Reset password'}

class PasswordResetConfirm(SuccessMessageMixin, PasswordResetConfirmView): 
    success_url = reverse_lazy('login')
    success_message = f'Password reset successfully! Now you can login'
    
    form_class = UserPasswordResetConfirmForm
    template_name = 'users/password_reset.html'
    extra_context = {'formtitle': 'Create new password'}
    
