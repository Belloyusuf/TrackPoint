import sweetify
from django.shortcuts import render
from django.shortcuts import render, redirect
from . forms import  UserRegistration, ProfileEditForm, UserProfileEditForm
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from . models import CustomUser
from sweetify.views import SweetifySuccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login as auth_login
# from .utils import send_welcome_email  # Import the email function






# users login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '')

        if not username:
            return JsonResponse({'success': False, 'message': 'Username is required.'}, status=400)

        if not password:
            return JsonResponse({'success': False, 'message': 'Password is required.'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return JsonResponse({'success': True, 'message': 'Login Successful...', 'next_url': next_url})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials.'}, status=401)
    else:
        next_url = request.GET.get('next', '')
        return render(request, 'registration/login.html', {'next': next_url})
    





@login_required(login_url="/accounts/login/")
def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            sweetify.toast(request, 'Account created successfully', icon='success', timer=3000, persistent=False)
            return redirect('school_setup:dashboard')
        else:
            error_messages = form.errors.get('__all__', [])
            return render(request, 'accounts/register.html', {'form': form, 'error_messages': error_messages})
    else:
        form = UserRegistration()

    return render(request, 'accounts/register.html', {'form': form})




# Update users profile 
@login_required(login_url="/accounts/login/")
def edit_profile(request):
    """ Users profile edit view ."""
    if request.method == 'POST':
        profile_form = UserProfileEditForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )
        if profile_form.is_valid():
            profile_form.save()
            sweetify.toast(request, 'Success!', text='Your profile has been updated successfully', icon="success", timer=3000)
            return redirect('school_setup:dashboard')
    else:
        profile_form = UserProfileEditForm(instance=request.user)
        
    return render(request, 'accounts/edit.html', {'profile_form': profile_form})




# Update users
class UpdateAdmin(LoginRequiredMixin, SweetifySuccessMixin, UpdateView):
    """ For Updating users in admin page """
    login_url = '/accounts/login/' # redirect user to the login page 
    model = CustomUser
    form_class = ProfileEditForm
    template_name = "accounts/update_admin.html"
    success_url = reverse_lazy("school_setup:dashboard")
    success_message = "Updated successfully"





# Delete users
class DeleteAdmin(LoginRequiredMixin, SweetifySuccessMixin, DeleteView):
    """ users can be deleted but there history as staff was saved """
    model = CustomUser
    template_name = "freezers/dashboard.html"
    success_url = reverse_lazy("school_setup:dashboard")
    success_message = "Updated successfully"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {
            'user_id': self.object.pk
        }
        return JsonResponse(data)











