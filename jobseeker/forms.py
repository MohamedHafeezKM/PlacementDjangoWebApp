from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from myapp.models import StudentProfile


class RegisterJobSeekerForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2','first_name']


class ProfileCreateModelForm(forms.ModelForm):
    class Meta:
        model=StudentProfile
        exclude=('user','saved_jobs')

        widgets={
            'gender':forms.Select(attrs={'class':'form-select'})
        }

# class ChangeJobSeekerForm(UserChangeForm):
#     class Meta:
#         model=User
#         fields=['username','email','first_name']