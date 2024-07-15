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
from faker import Faker
fake = Faker()


def index(request): 
    return render(request, 'androidchecklist/main.html',)

# def deleterecords(request): 
#     DataEntry.objects.all().delete()
#     if DataEntry.objects.all().delete():
#         messages.success(request, 'All the Records deleted successfully.')
#         return redirect('home-page')
#     else:
#         return render(request, 'androidchecklist/delete.html',)
def deleterecords(request):
    try:
        deleted_count, _ = DataEntry.objects.all().delete()
        if deleted_count > 0:
            messages.success(request, 'All the records deleted successfully.')
        else:
            messages.info(request, 'No records to delete.')
    except Exception as e:
        # Handle exceptions if any during the deletion process
        messages.error(request, f'An error occurred: {str(e)}')

    return redirect('home-page')    

def insertrecords(request): 
# insert_into()
    insert_check = DataEntry.objects.count()
    
    if insert_check > 0:
        messages.warning(request, f'{insert_check} Records already imported! ')
        return redirect('home-page')
    else:
        url = "https://kc.humanitarianresponse.info/api/v1/data/1111365?format=json"
        response = requests.get(url)
        json_data = response.json()
        # print(json_data)
        for item in json_data:
            data_entry = DataEntry(
                dateofvisit = item['dateofvisit'],
                bemiscode=item['bemisCode'],
                schoolname=item['schoolname'],
                district = item['district'],
                StaffName = item['grp_staffname/staff_name'],
                region =item['grp_staffname/region'],
                schoolStatus= item['school_status'],
                # grp_completeForm/grp_enratt_1/girls_five_register

                # girls_reg_kachi= item['grp_completeForm/grp_enratt_ 1/girls_kachi_register'],
                girls_reg_kachi= item.get('grp_completeForm/grp_enratt_1/girls_kachi_register', 0),
                girls_reg_one =  item.get('grp_completeForm/grp_enratt_1/girls_one_register', 0),
                girls_reg_two =  item.get('grp_completeForm/grp_enratt_1/girls_two_register', 0),
                girls_reg_three= item.get('grp_completeForm/grp_enratt_1/girls_three_register', 0),
                girls_reg_four = item.get('grp_completeForm/grp_enratt_1/girls_four_register', 0),
                girls_reg_five = item.get('grp_completeForm/grp_enratt_1/girls_five_register', 0),

                boys_reg_kachi = item.get('grp_completeForm/grp_enratt_2/boys_kachi_register', 0),
                boys_reg_one =   item.get('grp_completeForm/grp_enratt_2/boys_one_register', 0),
                boys_reg_two =   item.get('grp_completeForm/grp_enratt_2/boys_two_register', 0),
                boys_reg_three=  item.get('grp_completeForm/grp_enratt_2/boys_three_register', 0),
                boys_reg_four =  item.get('grp_completeForm/grp_enratt_2/boys_four_register', 0),
                boys_reg_five =  item.get('grp_completeForm/grp_enratt_2/boys_five_register', 0),

                girls_kachi = item.get('grp_completeForm/grp_enratt_3/girls_kachi_present', 0),
                girls_one =   item.get('grp_completeForm/grp_enratt_3/girls_one_present', 0),
                girls_two =   item.get('grp_completeForm/grp_enratt_3/girls_two_present', 0),
                girls_three = item.get('grp_completeForm/grp_enratt_3/girls_three_present', 0),
                girls_four =  item.get('grp_completeForm/grp_enratt_3/girls_four_present', 0),
                girls_five =  item.get('grp_completeForm/grp_enratt_3/girls_five_present', 0),
                
                boys_kachi =  item.get('grp_completeForm/grp_enratt_4/boys_kachi_present', 0),
                boys_one =    item.get('grp_completeForm/grp_enratt_4/boys_one_present', 0),
                boys_two =    item.get('grp_completeForm/grp_enratt_4/boys_two_present', 0),
                boys_three =   item.get('grp_completeForm/grp_enratt_4/boys_three_present', 0),
                boys_four =   item.get('grp_completeForm/grp_enratt_4/boys_four_present', 0),
                boys_five =   item.get('grp_completeForm/grp_enratt_4/boys_five_present', 0),
                
                ptscms_enroll =  item.get('grp_completeForm/grp_ptsmc/ptsmcs_enroll', None),
                ptsmc_designation = item['grp_completeForm/grp_ptsmc/ptsmc_designation'] if 'grp_completeForm/grp_ptsmc/ptsmc_designation' in item else None,
                # ptsmc_designation = item['grp_completeForm/grp_ptsmc/ptsmc_designation'],
                
                stationary_purchased = item.get('grp_completeForm/grp_stationary/grp_stationary_sub/stationary_purchased', None),
                stationary_amount_pkr = item['grp_completeForm/grp_stationary/grp_stationary_sub/stationary_amount_pkr'] if 'grp_completeForm/grp_stationary/grp_stationary_sub/stationary_amount_pkr' in item else None,
                dateofpurchase = item['grp_completeForm/grp_stationary/grp_stationary_sub/dateofpurchase'] if 'grp_completeForm/grp_stationary/grp_stationary_sub/dateofpurchase' in item else None,
              
                student_performance = item.get('grp_completeForm/grp_misc/student_performance', None),
                
                stu_att_register_available = item.get('grp_completeForm/grp_schoolrecords/stu_att_register_available', None),
                stu_att_register_update = item['grp_completeForm/grp_schoolrecords/stu_att_register_update'] if 'grp_completeForm/grp_schoolrecords/stu_att_register_update' in item else None, 
                teach_att_register_available  = item.get('grp_completeForm/grp_schoolrecords/teach_att_register_available', None),
                teach_att_register_update = item['grp_completeForm/grp_schoolrecords/teach_att_register_update'] if 'grp_completeForm/grp_schoolrecords/teach_att_register_update' in item else None, 
                aw_register_available = item.get('grp_completeForm/grp_schoolrecords/aw_register_available', None),
                aw_register_update = item['grp_completeForm/grp_schoolrecords/aw_register_update'] if 'grp_completeForm/grp_schoolrecords/aw_register_update' in item else None, 
                cash_register_available = item.get('grp_completeForm/grp_schoolrecords/cash_register_available', None),
                cash_register_update = item['grp_completeForm/grp_schoolrecords/cash_register_update'] if 'grp_completeForm/grp_schoolrecords/cash_register_updatee' in item else 0,
                stock_register_available = item.get('grp_completeForm/grp_schoolrecords/stock_register_available', None),
                stock_register_update = item['grp_completeForm/grp_schoolrecords/stock_register_update'] if 'grp_completeForm/grp_schoolrecords/stock_register_update' in item else 0,
                log_register_available = item.get('grp_completeForm/grp_schoolrecords/log_register_available', None),
                log_register_update = item['grp_completeForm/grp_schoolrecords/log_register_update'] if 'grp_completeForm/grp_schoolrecords/log_register_update' in item else 0,
                meet_register_available = item.get('grp_completeForm/grp_schoolrecords/meet_register_available', None),
                meet_register_update = item['grp_completeForm/grp_schoolrecords/meet_register_update'] if 'grp_completeForm/grp_schoolrecords/meet_register_update' in item else 0,

                
                descriptions = item.get('grp_remarks/remarks',None)

            ## Map more fields from the JSON data to the model
            )
            # data_entry.save()
            data_entry.save()
        messages.success(request, 'All the records imported successfully.')
        # return render(request, 'androidchecklist/insert.html',)
    return redirect('home-page') 

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
    return render(request, 'androidchecklist/schools.html', context)
    
    # return render(request, 'pages/dashboard.html')

def searchrecords(request):
    if request.htmx:
      q = request.GET.get('q')
    # q = request.GET.get('q')
      if q:
        thirty_days_ago = datetime.now() - timedelta(days=320)
        dataentry = DataEntry.objects.filter(dateofvisit__gte=thirty_days_ago)
        dataentry = dataentry.filter(Q(bemiscode__icontains=q) | Q(schoolname__icontains=q)).order_by('-dateofvisit')
        # Use a Subquery to fetch the staff name from the staff_Parameter model
        staff_name_subquery = staff_Parameter.objects.filter(StaffCode=OuterRef('StaffName')).values('StaffName')[:1]
        # Annotate the dataentry queryset with the staff name
        dataentry = dataentry.annotate(staff_name=Subquery(staff_name_subquery))
        print( dataentry)
        return render(
            request=request,
            template_name='search.html',
            context={
                'dataentry': dataentry,
            }
        )
    # context = {
    #     'dataentry': dataentry,
    # }
    return render(request, 'androidchecklist/schools.html')

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
        if start_date > end_date:
            return render(request, 'androidchecklist/charts.html')
    else:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
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

    # ==================
    context = {
        'staff_visits': staff_visits,
        'dataentry': dataentry,
        'closed': closed,
        'region_list' : region_list,
        'region_count' : region_count,
        'region_zip' : region_zip,
        'total_entries' : total_entries,
        'all_records' : all_records,
        'staff_counts': staff_counts,
        'end_date' : end_date,
        'start_date' : start_date,
            
        # 'total_girls_enrollment': total_girls_enrollment,
        # 'total_boys_enrollment': total_boys_enrollment,
        # 'grand_total_enrollment': grand_total_enrollment,
    }
    return render(request, 'androidchecklist/charts.html', context)


def generate_data(request):
    for i in range(1 , 100):
        fake_name_address.objects.create(name=fake.name(), address=fake.address())
    return JsonResponse({'status : 200'})

""" def search_schools(request):
    schools =   request.GET.get('address')
    payload = []
    if schools:
        school_obj =  fake_name_address.objects.filter(address__icontains=schools)

        for school in school_obj:
            payload.append(school.address)


    return JsonResponse({'status': 200, 'data': payload}) """

def search_schools_page(request):
    return render(request, 'androidchecklist/Untitled-1.html')
# ---------AUTO COMPLETE----------------------#
def search_schools(request):
    schools = request.GET.get('address')
    payload = []
   
    if schools:
        # school_objs = DataEntry.objects.filter(schoolname__icontains=schools).distinct()
        school_objs = DataEntry.objects.filter(schoolname__icontains=schools).values('schoolname').distinct()
        # school_objs = DataEntry.objects.filter(schoolname__icontains=schools).values('schoolname', 'bemiscode').distinct()

        # payload = [school.schoolname for school in school_objs]
        payload = [entry['schoolname'] for entry in school_objs]
        # payload = [{'schoolname': entry['schoolname'], 'bemiscode': entry['bemiscode']} for entry in school_objs]

    return JsonResponse(payload, safe=False)

#-------------STAFF TIME SHEET DEF-----------------------------------#
def stafftimsheet(request):
    staffnames = staff_Parameter.objects.values('StaffName','StaffCode')
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
    staff_name_subquery = staff_Parameter.objects.filter(StaffCode=OuterRef('StaffName')).values('StaffName')[:1]
    
    # Annotate the dataentry queryset with the staff name
    dataentry = dataentry.annotate(staff_name=Subquery(staff_name_subquery))
    
    record_count = dataentry.count()
    context = {
        'dataentry': dataentry,
        'record_count': record_count,
        'staffnames' : staffnames 
    }
    # return render(request, 'androidchecklist/schools.html', context)
    return render(request, 'pages/testschool.html', context)
    # return render(request, 'pages/dashboard.html')