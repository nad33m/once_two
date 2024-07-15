from django.urls import path
from django.contrib.auth import views as auth_views
from collections import Counter
from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.decoratorspytho import login_required
import requests
import json
from django.http import HttpResponse,JsonResponse
from datetime import datetime, timedelta
import csv
from .models import *
from django.db.models import Q, OuterRef, Subquery
from django.shortcuts import render
from django.utils.html import escape
from django.views import View
import re
from django.db.models import Sum,F
from django.utils.html import escape
from datetime import datetime, timedelta
from django.db.models import Count
from django.views.generic.list import ListView
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
  path(''       , views.charts,  name='index-page'),
  path('tables/', views.showrecords, name='tables'),
  path('timesheet/', views.stafftimsheet, name='timesheet-page'),
  path('login/', views.login, name='login-page'),
  path('settingss', login_required(views.tsettings, login_url='login'), name='settings-page'),
]
