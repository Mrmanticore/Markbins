from django.contrib import admin
from django.urls import path
from .views import index,upload_image
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', index, name='home'),
    path('mobile/', views.mobile_view, name='mobile_view'),

    path('upload-image/', views.upload_image, name='upload_image'),
    path('capture-map/', views.capture_map, name='capture_map'),
    path('submit-tweet/', views.submit_tweet, name='submit_tweet'),
    path('submit_tweet/<str:unique_id>/', views.submit_tweet, name='submit_tweet'),
    path('guide.html', views.guide_view, name='guide'),
    path('blogs.html', views.blogs_view, name='blogs'),
    path('VideoTutorial.html', views.video_tutorial_view, name='video_tutorial'),
    path('about.html', views.about_view, name='about'),
    # path('contact.html', views.contact_view, name='contact'),
    path('markbins.html', views.markbins, name='markbins'),
    path('spotfill.html', views.spotfill, name='spotfill'),
    path('contact.html', views.contact_view, name='contact'),
    path('submit_contact_form/', views.submit_contact_form, name='submit_contact_form'),



]


urlpatterns += staticfiles_urlpatterns() 