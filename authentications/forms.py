from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate




# login form
class LoginForm(forms.Form):

    """ provide username or email and password to login """
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Email or username"}), max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        fields = ("username",)
        
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data

    def get_user(self):
        return self.user
        



        
# USER REGISTRATION FORM
class UserRegistration(UserCreationForm):

    """Create new user by providing required information"""
    username = forms.CharField(widget=forms.TextInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(widget=forms.EmailInput, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'image', 'email', 'phone', 'section', 'm_class', 
                  'is_admin', 'is_principal', 'is_admission', 'is_class_master', 'is_exam', 'is_account')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            self.add_error(None, ValidationError("Passwords do not match. Please enter matching passwords."))

        # Validate class master fields
        is_class_master = cleaned_data.get('is_class_master')
        section = cleaned_data.get('section')
        m_class = cleaned_data.get('m_class')

        if is_class_master:
            if not section or not m_class:
                self.add_error(None, ValidationError("Class master must have both a section and a class assigned."))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserRegistration, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'id': 'password1'})
        self.fields['password2'].widget.attrs.update({'id': 'password2'})
        


  

# User profile update form
class ProfileEditForm(forms.ModelForm):

    """ 
    users can update their informations
    the following fields can be editable 
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'image', 'email', 'phone','section','m_class', 
                    'is_admin', 'is_principal','is_admission', 'is_class_master',  'is_exam', 'is_account')




class UserProfileEditForm(forms.ModelForm):
    
    """ 
    following fields can be editable for users that are not admins 
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'image', 'email', 'phone')
