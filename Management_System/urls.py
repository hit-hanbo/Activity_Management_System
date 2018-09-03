from django.contrib import admin
from django.urls import path
from Management.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('manager/input/', single_import),
    path('manager/new_activity', manager_add_activity),

    path('user/register/', volunteer_register),
    path('user/query/', volunteer_query),
]
