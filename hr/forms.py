from django import forms
from myapp.models import Category,Job

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))

class CategoryModalForm(forms.ModelForm):

    class Meta:
        model=Category
        fields=['name']


class JobModalForm(forms.ModelForm):

    class Meta:
        model=Job
        exclude=('status',) #exclude 'status'  from Job Modal in this form and include all other fields
        

        widgets={
            # 'title':forms.TextInput(attrs={'class':'form-control'}),
            # 'description':forms.Textarea(attrs={'class':'form-control','rows':2}),
            # 'salary':forms.NumberInput(attrs={'class':'form-control'}),
            # 'experience':forms.NumberInput(attrs={'class':'form-control'}),
            'last_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            # 'vacancies':forms.NumberInput(attrs={'class':'form-control'}),
            # 'contact':forms.NumberInput(attrs={'class':'form-control'}),
            # 'qualification':forms.TextInput(attrs={'class':'form-control'}),
            # 'company':forms.TextInput(attrs={'class':'form-control'}),
            # 'poster':forms.FileInput(attrs={'class':'form-control','type':'file'}),
            'category':forms.Select(attrs={'class':'form-select'}),
            'job_type':forms.Select(attrs={'class':'form-select'}),
           
            
        }

class JobChangeForm(forms.ModelForm):

    class Meta:
        model=Job
        fields="__all__"
        widgets={
            'last_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'category':forms.Select(attrs={'class':'form-select'}),
            'status':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'created_date':forms.DateInput(attrs={'class':'form-control','type':'datetime'}),
            'job_type':forms.Select(attrs={'class':'form-select'}),
        }
        

