from django.contrib import admin
from django.urls import path
from Management.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('query/', volunteer_query),
]
