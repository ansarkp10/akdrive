from django import forms
from django.contrib.auth.models import User
from .models import File, Folder
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        
        # Remove default help texts
        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None
        
        # Custom placeholders
        self.fields["username"].widget.attrs["placeholder"] = "Enter username"


from django import forms
from .models import File, Folder

class FileUploadForm(forms.ModelForm):
    folder = forms.ModelChoiceField(queryset=Folder.objects.none(), required=False)

    class Meta:
        model = File
        fields = ['file', 'folder']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['folder'].queryset = Folder.objects.filter(owner=user)