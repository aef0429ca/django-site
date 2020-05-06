from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

# app_name = 'xmltools'
urlpatterns = [
    path('', views.home, name='home'),
    path('xml_upload.html', views.xml_upload, name='xml_upload'),
    path('xml_fetch.html', views.xml_fetch, name='xml_fetch'),
    path('xml_format_test/<int:pk>', views.xml_format_test, name='xml_format_test'),
    path('xml_analyze/<int:pk>', views.xml_analyze, name='xml_analyze'),
    path('xml_profile/<int:pk>', views.xml_profile, name='xml_profile'),
    path('xml_tags.html', TemplateView.as_view(template_name='xmltools/xml_tags.html'), name='xml_tags'),
]