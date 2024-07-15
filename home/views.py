from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from androidchecklist.models import *
from collections import Counter
from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.decoratorspytho import login_required
import requests
import json
from django.http import HttpResponse,JsonResponse
from datetime import datetime, timedelta
import csv
# from .models import *
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
from django.db import connection


def index(request):

  context = {
    'segment'  : 'index',
    #'products' : Product.objects.all()
  }
  return render(request, "pages/index.html", context)

def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/dynamic-tables.html", context)

#-------------STAFF TIME SHEET DEF-----------------------------------#
def stafftimsheet(request):
    staffnames = staff_Parameter.objects.values('StaffName','StaffCode','assignedSchools')
    q = request.GET.get('q')
    thirty_days_ago = datetime.now() - timedelta(days=31)
    
    if q:
        q = q[:100]
        q = escape(q)
    # else:
    #     q= 45001
    dataentry = DataEntry.objects.filter(dateofvisit__gte=thirty_days_ago)
    
    if q:
        # dataentry = dataentry.filter(Q(bemiscode__icontains=q) | Q(schoolname__icontains=q)).order_by('-dateofvisit')
        dataentry = dataentry.filter(Q(StaffName=q)).order_by('-dateofvisit')

    # Use a Subquery to fetch the staff name from the staff_Parameter model
    staff_name_subquery = staff_Parameter.objects.filter(StaffCode=OuterRef('StaffName')).values('StaffName','assignedSchools')[:1]

    # staff_name_subquery = staff_Parameter.objects.filter(StaffCode=OuterRef('StaffName')).values('StaffName','assignedSchools')[:1]
    
    # Annotate the dataentry queryset with the staff name
    dataentry = dataentry.annotate(staff_name=Subquery(staff_name_subquery))
    
    record_count = dataentry.count()
    context = {
        'dataentry': dataentry,
        'record_count': record_count,
        'staffnames' : staffnames,
    }
    # return render(request, 'androidchecklist/schools.html', context)
    return render(request, 'pages/testschool.html', context)
    # return render(request, 'pages/dashboard.html')

# -----------------------------------------------------

def charts(request):
    staff_names = staff_Parameter.objects.values('StaffName','StaffCode', 'assignedSchools','Districts')
    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')
    # Calculate the date 30 days ago from today
    all_records = DataEntry.objects.all()
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    if startDate and endDate:
        start_date = datetime.strptime(startDate, '%Y-%m-%d')
        end_date = datetime.strptime(endDate, '%Y-%m-%d')
        number_entries_today = end_date - timedelta(days=2)
        if start_date > end_date:
            return render(request, 'androidchecklist/charts.html')
    else:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        number_entries_today = end_date - timedelta(days=2)

    # dataentry = DataEntry.objects.filter(schoolStatus='open').count()
    # dataentry_staff = DataEntry.objects.filter(dateofvisit__gte=thirty_days_ago)
    dataentry_staff = DataEntry.objects.filter(dateofvisit__range=(start_date, end_date))
    # staff_visits = dataentry_staff.values('StaffName').annotate(visit_count=Count('bemiscode'))
    # staff_visits = dataentry_staff.values('StaffName').annotate(visit_count=Count('bemiscode'))
    
    # staff_visits = dataentry_staff.annotate(visit_count=Count('bemiscode')).values('StaffName').order_by('-visit_count')
    # Count the distinct school codes for each staff
    staff_visits = dataentry_staff.values('StaffName').annotate(visit_count=Count('bemiscode', distinct=True)).order_by('-visit_count')
    # -----------------------------------------------------------------------------------------
    data_entries = DataEntry.objects.filter(
        Q(StaffName__in=staff_names.values('StaffCode')),
        # dateofvisit__gte=thirty_days_ago
        dateofvisit__range=(start_date, end_date)
    )

    staff_counts = {}
    for staff in staff_names:
        staff_code = staff['StaffCode']
        assigned_schools = staff['assignedSchools']
        districts = staff['Districts']

        count = data_entries.filter(StaffName=staff_code).count()
        difference = assigned_schools - count   
        coverPercentAge = round((count/assigned_schools)*100)
        
        serialno = [1,2,3,4,5,6,7,8,9]

        staff_counts[staff['StaffName']] = {
            'count': count,
            'assigned': assigned_schools,
            'difference' : difference,
            'coverPercentAge' : coverPercentAge,
            'districts' :   districts,
            'serial' : serialno,
        }
    # ------------------------------------------------------------------------------------------
    number_entries_today_2 = DataEntry.objects.filter(dateofvisit__range=(number_entries_today, end_date)).count()
    dataentry = DataEntry.objects.filter(schoolStatus='open', dateofvisit__range=(start_date, end_date)).count()
    closed = DataEntry.objects.filter(schoolStatus='close', dateofvisit__range=(start_date, end_date)).count()
    region_ca = DataEntry.objects.filter(region='Central-A', dateofvisit__range=(start_date, end_date)).count()
    region_cb = DataEntry.objects.filter(region='Central-B', dateofvisit__range=(start_date, end_date)).count()
    region_na = DataEntry.objects.filter(region='North-A', dateofvisit__range=(start_date, end_date)).count()
    region_nb = DataEntry.objects.filter(region='North-B', dateofvisit__range=(start_date, end_date)).count()
    region_sea = DataEntry.objects.filter(region='South-East-A', dateofvisit__range=(start_date, end_date)).count()
    region_seb = DataEntry.objects.filter(region='South-East-B', dateofvisit__range=(start_date, end_date)).count()
    region_swa = DataEntry.objects.filter(region='South-West-A', dateofvisit__range=(start_date, end_date)).count()
    region_swb = DataEntry.objects.filter(region='South-West-B', dateofvisit__range=(start_date, end_date)).count()
    
    region_list = ['Central-A','Central-B','North-A','North-B','South-East-A','South-East-B','South-West-A', 'South-West-B' ]
    region_count = [region_ca,region_cb,region_na,region_nb,region_sea,region_seb,region_swa,region_swb]
    # closed = DataEntry.objects.filter(schoolStatus='close').count()
    region_zip = zip(region_list, region_count)
    total_entries = sum(region_count)
    dataentry = int(dataentry)
    closed = int(closed)
    thirty_days_percentage = round((total_entries/633)*100)

     # --------------------------------------------------------------
    with connection.cursor() as cursor:
        query = """
        SELECT MONTHNAME(dateofvisit) AS month, COUNT(*) AS visit_count
        FROM androidchecklist_dataentry
        WHERE YEAR(dateofvisit)=2024
        GROUP BY MONTHNAME(dateofvisit)
        ORDER BY STR_TO_DATE(CONCAT('01 ', MONTHNAME(dateofvisit), ' 2000'), '%d %M %Y');
        """
        cursor.execute(query)
        result_list = cursor.fetchall()
    # --------------------------------------------------------------


    # ==================
    context = {
        'staff_visits': staff_visits,
        'dataentry': dataentry,
        'closed': closed,
        'region_list' : region_list,
        'region_count' : region_count,
        'region_zip' : region_zip,
        'total_entries' : total_entries,
        'thirty_days_percentage' : thirty_days_percentage,
        'all_records' : all_records,
        'staff_counts': staff_counts,
        'end_date' : end_date,
        'start_date' : start_date,
        'number_entries_today_2' : number_entries_today_2, 
        'result_list' : result_list,   
        # 'total_girls_enrollment': total_girls_enrollment,
        # 'total_boys_enrollment': total_boys_enrollment,
        # 'grand_total_enrollment': grand_total_enrollment,
    }
    context1 ={
        'nadeem' : '',
    }
  
    # return render(request, 'pages/testschool.html', context)
    # return render(request, 'androidchecklist/charts.html', context)
    return render(request, 'pages/index.html', context)
#----------------------------------------------------------------------------

def showrecords(request):
    q = request.GET.get('q')
    thirty_days_ago = datetime.now() - timedelta(days=365)
    
    if q:
        q = q[:100]
        q = escape(q)
    else:
        q=45001
        
    dataentry = DataEntry.objects.filter(dateofvisit__gte=thirty_days_ago)
    
    if q:
        dataentry = dataentry.filter(Q(bemiscode__icontains=q) | Q(schoolname__icontains=q)).order_by('-dateofvisit')
    
    # Use a Subquery to fetch the staff name from the staff_Parameter model
    staff_name_subquery = staff_Parameter.objects.filter(StaffCode=OuterRef('StaffName')).values('StaffName')[:1]
    
    # Annotate the dataentry queryset with the staff name
    dataentry = dataentry.annotate(staff_name=Subquery(staff_name_subquery))
    
    record_count = dataentry.count()
    context = {
        'dataentry': dataentry,
        'record_count': record_count, 
    }
    
    return render(request, 'pages/dynamic-tables.html', context)

def login(request):
    return render(request, 'pages/login.html')
# SETTINGS ----------------------------------
def tsettings(request):
    return render(request, 'pages/settings.html',)