"""
URL configuration for EmployeeManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema
from User import views
from frontend import views as fe
from django.conf.urls.static import static
from django.conf import settings
# from User import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(views.CustomGraphQLView.as_view(graphiql=True, schema=schema))),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    #frontend Api
    path("",fe.Home,name='home'),
    path("d",fe.Dashboard,name='dashboard'),
    path("r",fe.consume_registration,name='registration'),
    path('l',fe.consume_login,name='login')


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
