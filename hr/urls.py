from django.urls import path

from hr import views

urlpatterns = [
    path('signin/',views.SignInView.as_view(),name='signin'),
    path('index/',views.DashboardView.as_view(),name='index'),
    path('signout/',views.SignOutView.as_view(),name='signout'),
    path('category/',views.CategoryCreateOrListView.as_view(),name='category'),
    path('category/remove/<int:pk>',views.CategoryDeleteView.as_view(),name='category-delete'),
    path('job/add',views.JobsCreateView.as_view(),name='add_job'),
    path('job/all',views.JobsListView.as_view(),name='all_jobs'),
    path('job/remove/<int:pk>',views.JobsDeleteView.as_view(),name='remove_job'),
    path('job/change/<int:pk>',views.JobsUpdateView.as_view(),name='change_job'),
    path('job/<int:pk>/application',views.JobApplicationView.as_view(),name='applications'),
    path('job/application/all',views.AllApplicationListView.as_view(),name='all_applications'),
    path('job/application/<int:pk>/detail',views.ApplicationDetailView.as_view(),name='application_detail'),
    path('job/application/<int:pk>/status/change',views.ApplicationUpdateView.as_view(),name='application_status_edit'),
    

]