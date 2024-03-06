from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import CreateView,TemplateView,DetailView,UpdateView,ListView,View
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages

from jobseeker.forms import RegisterJobSeekerForm,ProfileCreateModelForm
from myapp.models import StudentProfile,Job,Application,Category
# Create your views here.


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'Failed to Sign')
            return redirect('signin')
        
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,never_cache]


class SignUpView(CreateView):
    template_name='jobseeker/register.html'
    form_class=RegisterJobSeekerForm
    success_url=reverse_lazy('signin')

@method_decorator(decs,name='dispatch')
class StudentIndexView(ListView):
    template_name='jobseeker/index.html'
    context_object_name='all_jobs'
    model=Job
    
    def get_queryset(self):
        my_applications=Application.objects.filter(student=self.request.user).values_list('job',flat=True)
        qs=Job.objects.filter(status=True).order_by('-created_date')
        qs=qs.exclude(id__in=my_applications)
        #localhost/seeker/index/?category=front-end
        if 'category' in self.request.GET:
            category_value=self.request.GET.get('category')
            qs=qs.filter(category__name=category_value)
        return qs
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        qs=Category.objects.all()
        context['categories']=qs
        return context
@method_decorator(decs,name='dispatch')
class ProfileCreateView(CreateView):
    template_name='jobseeker/add_profile.html'
    form_class=ProfileCreateModelForm
    success_url=reverse_lazy('seeker_index')

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
@method_decorator(decs,name='dispatch')    
class ProfileDetailView(DetailView):
    template_name='jobseeker/profile_detail.html'
    context_object_name='data'
    model=StudentProfile

@method_decorator(decs,name='dispatch')
class ProfileEditView(UpdateView):
    template_name='jobseeker/edit_profile.html'
    form_class=ProfileCreateModelForm
    model=StudentProfile
    success_url=reverse_lazy('seeker_index')

# class JobListView(ListView):
#     template_name='jobseeker/job_list.html'
#     context_object_name='jobs'
#     model=Job
@method_decorator(decs,name='dispatch')
class JobDetailView(DetailView):
    template_name='jobseeker/job_detail.html'
    model=Job
    context_object_name='job'

@method_decorator(decs,name='dispatch')
class ApplyJobView(View):

    # get method not used here

    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        job_object=Job.objects.get(id=id)
        student_user=request.user
        Application.objects.create(job=job_object,student=student_user)
        messages.success(request,'You have applied successfully!')
        return redirect('seeker_index')
        
@method_decorator(decs,name='dispatch')
class ApplicationListView(ListView):
    template_name='jobseeker/applications.html'
    model=Application
    context_object_name='application'

    def get_queryset(self):
        qs=Application.objects.filter(student=self.request.user)
        return qs
  
    
@method_decorator(decs,name='dispatch')
class JobSaveView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        job_object=Job.objects.get(id=id)
        action=request.POST.get('action')
        if action=='save':
            request.user.profile.saved_jobs.add(job_object)
            messages.success(request,'Added to favorite')
        elif action=='unsave':
            request.user.profile.saved_jobs.remove(job_object)
            messages.success(request,'Removed from favorite')
        
        return redirect('seeker_index')
    
@method_decorator(decs,name='dispatch')
class SavedJobView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.profile.saved_jobs.all()
        return render(request,'jobseeker/saved_jobs.html',{'data':qs})
    
    
