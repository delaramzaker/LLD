"""
URL configuration for LLD project.

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
from LLDapp.views import hello_world, upload_file, answer_question, combined_view, PWS_world, news, about, contact, question_answer, get_answer
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('upload/', upload_file, name='upload_file'), 
    path('combined/', combined_view, name='combined_view'),
    path('PWS/', PWS_world, name='PWS_world'),
    path('news/', news, name='news'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('question_answer/', question_answer, name='question_answer'),
    path('get_answer/', get_answer, name='get_answer'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

