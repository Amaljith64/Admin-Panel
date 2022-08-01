
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('register',views.register,name='register'),
    path('registeruser',views.registeruser,name='registeruser'),
    path('registeradmin',views.registeradmin,name='registeradmin'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('myadmin',views.admin,name="myadmin"),
    path('update/<int:id>',views.update,name="updatedata"),
    path('delete/<int:id>',views.delete,name="deletedata"),
    

    
]

# <a href="update/{{data.id}}"><button><i class="material-icons" data-toggle="tooltip" title="Edit">&#xE254;</i></button></a> 