from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from newtask import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('appointment_confirmation/<int:appointment_id>/', views.appointment_confirmation, name='appointment_confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
