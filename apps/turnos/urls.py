from django.urls import path
from apps.turnos import views
from apps.turnos.views import Medicos
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'turnos'
urlpatterns = [
    path('', views.index, name='index'),

    path('login/', LoginView.as_view(
        template_name="login.html"), name='login'),

    path('logout/', LogoutView.as_view(
        template_name="logout.html"), name='logout'),

    path('register/', views.register, name='register'),

    path('update/', views.update, name='update'),

    path('account/', views.account, name='account'),

    path('medicos/', Medicos.as_view(template_name="medicos.html"),
         name='medicos'),

    path('appointment/', views.appointment, name='appointment'),

    path('confirm/', views.confirm, name='confirm'),

    path('misturnos/', views.misturnos, name='misturnos'),

    path('edit/', views.edit, name='edit'),

    path('delete/', views.delete, name='delete'),

    path('confirm_edit/', views.confirm_edit, name='confirm_edit'),

]
