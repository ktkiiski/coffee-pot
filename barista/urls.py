"""barista URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from coffeestatus.views import CoffeeStatusView
from coffeestatus.views import coffee_image_redirect
from recognition.views import labelize_pictures
from recognition.views import labelize_picture_left_sides
from recognition.views import labelize_picture_right_sides
from webcam.views import dump_labeled_pics

urlpatterns = [
    url(r'^$', CoffeeStatusView.as_view()),
    url(r'^status/?$', CoffeeStatusView.as_view()),
    url(r'^img/?$', coffee_image_redirect),
    url(r'^labelizer/?$', labelize_pictures, name="labelizer"),
    url(r'^labelizer/left/?$', labelize_picture_left_sides, name="left_labelizer"),
    url(r'^labelizer/right/?$', labelize_picture_right_sides, name="right_labelizer"),
    url(r'^dump/?$', dump_labeled_pics, name="dump_labeled_pics"),
    url(r'^admin/', admin.site.urls),
]
# Serve static files in development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
