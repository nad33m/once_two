from django.contrib import admin
from django.urls import path,include
from . import views
from .views import *

urlpatterns = [
    
    path('', views.index, name='home-page'),
    path('insertrecords', views.insertrecords, name='insert-page'),
    path('deleterecords', views.deleterecords, name='delete-page'),
    path('showrecords', views.showrecords, name='record-page'),
    # path('autocomplete/', DataEntryAutocomplete.as_view(), name='dataentry_autocomplete'),
    # path('autocomplete-template/', views.dataentry_autocomplete, name='autocomplete_template'),
    # path('autocomplete/', DataEntryAutocomplete.as_view(), name='autocomplete'),
    path('charts/', views.charts, name='charts-page'),
    path('searchrecords', views.searchrecords, name='search-page'),
    path('generate_data/', views.generate_data, name='fake-data'),
    path('searchschools/', views.search_schools, name='search-schools'),
    path('searchschools_page/', views.search_schools_page, name='search-schools-page'),
    path('timesheet/', views.stafftimsheet, name='timesheet-page'),
    # path('searchschools/', search_schools),
    # path('search-schools/', autocomplete_schoolname, name='autocomplete_schoolname'),
    

]
    # path('school', views.indexx, name='school-page'),


