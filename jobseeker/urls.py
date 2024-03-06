from django.urls import path

from jobseeker import views

urlpatterns=[
    path('register/',views.SignUpView.as_view(),name='signup'),
    path('index/',views.StudentIndexView.as_view(),name='seeker_index'),
    path('profile/add/',views.ProfileCreateView.as_view(),name='add_profile'),
    path('profile/detail/<int:pk>/',views.ProfileDetailView.as_view(),name='detail_profile'),
    path('profile/change/<int:pk>/',views.ProfileEditView.as_view(),name='edit_profile'),
    path('job/<int:pk>/',views.JobDetailView.as_view(),name='job_detail'),
    path('job/<int:pk>/apply/',views.ApplyJobView.as_view(),name='apply_job'),
    path('applications/',views.ApplicationListView.as_view(),name='applications'),
    path('job/<int:pk>/save',views.JobSaveView.as_view(),name='job_save'),
    path('job/saved/all',views.SavedJobView.as_view(),name='all_saved_job'),
    
]