
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,CreateView,ListView,UpdateView,DetailView
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from hr.forms import LoginForm,CategoryModalForm,JobModalForm,JobChangeForm
from myapp.models import Category,Job,Application
from jobseeker.views import decs,signin_required
# Create your views here.


def admin_permission_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_superuser:
            messages.error(request,'Admin Permission required!')
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
    return wrapper
super_rule=[admin_permission_required,signin_required,never_cache]

class SignInView(FormView):
    # def get(self,request,*args,**kwargs):
    #     form=LoginForm()
    #     return render(request,'signin.html',{'form':form})
    template_name='signin.html'
    form_class=LoginForm

    def post(self, request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get('username')
            pass_word=form.cleaned_data.get('password')
            user_obj=authenticate(request,username=user_name,password=pass_word)
            if user_obj:
                login(request,user_obj)
                messages.success(request,'Logged in')
                if request.user.is_superuser:
                    return redirect('index')
                else:
                    return redirect('seeker_index')
                
    
        messages.error(request,'Failed to Login, Invalid creditional')
        return render(request,'signin.html',{'form':form})

@method_decorator(super_rule,name='dispatch')
class DashboardView(TemplateView):
    #only to render a template, no forms or anything else
    template_name='index.html'

@method_decorator(decs,name='dispatch')
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('signin')
    
@method_decorator(super_rule,name='dispatch')
class CategoryCreateOrListView(CreateView,ListView):
    template_name='category.html'
    form_class=CategoryModalForm
    success_url=reverse_lazy('category')
    context_object_name='all_category'
    model=Category
    

# class CategoryView(View):
#     def get(self,request,*args,**kwargs):
#         form=CategoryModalForm()
#         all_category=Category.objects.all()
#         return render(request,'category.html',{'form':form,'all_category':all_category})

    
#     def post(self,request,*args,**kwargs):
#         form=CategoryModalForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,'This cateogary has been added')
#             return redirect('category')
#         else:
#             messages.error(request,'Failed')
#             return render(request,'category.html',{'form':form})
@method_decorator(super_rule,name='dispatch')        
class CategoryDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Category.objects.filter(id=id).delete()
        messages.success(request,'This category has been deleted!')
        return redirect('category')   
    
@method_decorator(super_rule,name='dispatch')
class JobsCreateView(CreateView):
    template_name='add_jobs.html'
    form_class=JobModalForm
    success_url=reverse_lazy('all_jobs')

@method_decorator(super_rule,name='dispatch')
class JobsListView(ListView):
    template_name='all_jobs.html'
    context_object_name='all_jobs'
    model=Job

    def get(self,request,*args,**kwargs):
        qs=Job.objects.all()

        if 'status' in request.GET:
            value=request.GET.get('status')
            qs=qs.filter(status=value)
        return render(request,self.template_name,{'all_jobs':qs})

    # def get_queryset(self):                    #overriding
    #     return Job.objects.filter(status=True)

    # def get(self,request,*args,**kwargs):                #overriding
    #     qs=Job.objects.filter(status=True)                     
    #     return render(request,'all_jobs.html',{'all_jobs':qs})


@method_decorator(super_rule,name='dispatch')
class JobsDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Job.objects.get(id=id).delete()
        messages.success(request,'This Job has been deleted')
        return redirect('all_jobs')
@method_decorator(super_rule,name='dispatch')    
class JobsUpdateView(UpdateView):
    form_class=JobChangeForm
    template_name='edit_job.html'
    model=Job
    success_url=reverse_lazy('all_jobs')

@method_decorator(super_rule,name='dispatch')
class JobApplicationView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        job_object=Job.objects.get(id=id)
        application=Application.objects.filter(job=job_object)
        return render(request,'applications.html',{'application':application})
@method_decorator(super_rule,name='dispatch')   
class ApplicationDetailView(DetailView):
    template_name='application_detail.html'
    context_object_name='data'
    model=Application

@method_decorator(super_rule,name='dispatch')
class AllApplicationListView(ListView):
    template_name='all_applications.html'
    context_object_name='all_applications'
    model=Application

@method_decorator(super_rule,name='dispatch')
class ApplicationUpdateView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        application_object=Application.objects.get(id=id)
        status=request.POST.get('status')
        application_object.status=status
        application_object.save()
        messages.success(request,'Status have been updated')
        # return redirect('index')
        if application_object.status=='shortlisted':
            send_mail(
            "Application updated",
            "Status for your application has changed",
            "from@example.com",
            [application_object.student.email],
            fail_silently=False,
        )
        return redirect('application_detail',id)