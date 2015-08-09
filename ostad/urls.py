"""ostad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'ostad.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^loginpage$', 'ostad.views.home_login'),
    url(r'^login$', 'ostad.views.login_user'),
    url(r'^logout$', 'ostad.views.logout_user'),
    url(r'^sections$', 'sections.views.show_classes'),
    url(r'^sections/(?P<class_id>\d+)$', 'sections.views.list_sections'),
    url(r'^sections/add/(?P<class_id>\d+)$', 'sections.views.add_section'),
    url(r'^sections/save/(?P<class_id>\d+)$', 'sections.views.save_section'),
    url(r'^sections/delete$', 'sections.views.remove_sections'),
    url(r'^sections/delete/(?P<class_id>\d+)$', 'sections.views.remove_sections'),

    url(r'^sections/signup/(?P<class_id>\d+)/(?P<section_id>\d+)$', 'sections.views.add_student'),
    url(r'^students/save/(?P<class_id>\d+)$', 'sections.views.save_student'),
    url(r'^students/delete$', 'sections.views.remove_students'),
    url(r'^students/delete/(?P<class_id>\d+)/(?P<student_id>\d+)$', 'sections.views.remove_students'),

    url(r'^classes/save', 'sections.views.save_class'),
    url(r'^classes/delete', 'sections.views.remove_classes'),

    #url(r'^$', 'sections.views.custom_signup_form'),
    #url(r'^customform/save$', 'sections.views.custom_form_save')

    url(r'^captcha/', include('captcha.urls')),

    # TODO: remove after testing
    url(r'^populate', 'ostad.views.generate_mock_data'),

]
