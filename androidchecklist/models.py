from django.db import models
from django.contrib.auth.models import User
from .models import *

# # Create your models here.
class staff_Parameter(models.Model):
    StaffName = models.CharField(max_length=120)
    Designation = models.CharField(max_length=800)
    Districts = models.CharField(max_length=80)
    StaffCode = models.CharField(max_length=180)
    assignedSchools = models.IntegerField(null=True, blank=True)  # New Field.

    class Meta:  
        verbose_name_plural = 'staff_Parameter'

    def __str__(self):
        return self.StaffName
    

class DataEntry(models.Model):
    dateofvisit = models.DateField()
    bemiscode = models.CharField(max_length=6)
    schoolname = models.CharField(max_length=200)
    district = models.CharField(max_length=50)
    StaffName = models.CharField(max_length=180)
    # StaffCode = models.ForeignKey(staff_Parameter, on_delete=models.CASCADE)
    region = models.CharField(max_length=50)
    schoolStatus = models.CharField(max_length=80)

    girls_reg_kachi = models.CharField(max_length=3,default=None)
    girls_reg_one = models.CharField(max_length=3,default=None)
    girls_reg_two = models.CharField(max_length=3,default=None)
    girls_reg_three = models.CharField(max_length=3,default=None)
    girls_reg_four = models.CharField(max_length=3,default=None)
    girls_reg_five = models.CharField(max_length=3,default=None)
    
    boys_reg_kachi = models.CharField(max_length=3,default=None)
    boys_reg_one = models.CharField(max_length=3,default=None)
    boys_reg_two = models.CharField(max_length=3,default=None)
    boys_reg_three = models.CharField(max_length=3,default=None)
    boys_reg_four = models.CharField(max_length=3,default=None)
    boys_reg_five = models.CharField(max_length=3,default=None)
    
    girls_kachi = models.CharField(max_length=3,default=None)
    girls_one = models.CharField(max_length=3,default=None)
    girls_two = models.CharField(max_length=3 ,default=None)
    girls_three = models.CharField(max_length=3,default=None)
    girls_four = models.CharField(max_length=3,default=None)
    girls_five = models.CharField(max_length=3,default=None)

    boys_kachi = models.CharField(max_length=3,default=None)
    boys_one = models.CharField(max_length=3,default=None)
    boys_two = models.CharField(max_length=3,default=None)
    boys_three = models.CharField(max_length=3,default=None)
    boys_four = models.CharField(max_length=3,default=None)
    boys_five = models.CharField(max_length=3,default=None)
    
    ptscms_enroll = models.CharField(max_length=3)
    ptsmc_designation = models.CharField(max_length=280)
    
    stationary_purchased = models.CharField(max_length=3,default=None)
    stationary_amount_pkr = models.CharField(max_length=3,default=None)
    student_performance = models.CharField(max_length=200,default=None)

    dateofpurchase = models.DateField()
    stu_att_register_available = models.CharField(max_length=3 ,default=None)
    stu_att_register_update =  models.CharField(max_length=3 ,default=None)
    teach_att_register_available = models.CharField(max_length=3 ,default=None) 
    teach_att_register_update = models.CharField(max_length=3 ,default=None)
    aw_register_available = models.CharField(max_length=3 ,default=None)
    aw_register_update = models.CharField(max_length=3 ,default=None) 
    cash_register_available = models.CharField(max_length=3,default=None)
    cash_register_update = models.CharField(max_length=3 ,default=None)
    stock_register_available = models.CharField(max_length=3 ,default=None)
    stock_register_update = models.CharField(max_length=3 ,default=None)
    log_register_available = models.CharField(max_length=3 ,default=None)
    log_register_update = models.CharField(max_length=3 ,default=None)
    meet_register_available = models.CharField(max_length=3 ,default=None)
    meet_register_update = models.CharField(max_length=3 ,default=None)

    descriptions = models.TextField(
                    max_length=10000,
                    default='',
                    blank=True,
                    db_column='descriptions',
                    db_collation='utf8_general_ci',
                )


    # Add more fields that match the structure of the JSON data
    unique_together = ('dateofvisit', 'bemiscode', 'schoolname')
    # unique_together = ('dateofvisit', 'bemiscode', 'schoolname', 'district')
    
    class Meta:  
        verbose_name_plural = 'DataEntry'
        

    def __str__(self):
        return f"checklist of {self.schoolname}"

# class dsAssignedCS(models.Model):
#     Staff_Name = models.CharField(max_length=120)
#     Designation = models.CharField(max_length=800)
#     District = models.CharField(max_length=80)
#     Codes = models.CharField(max_length=180)
#     addignedSchools = 
#     class Meta:  
#         verbose_name_plural = 'staff_Parameter'

#     def __str__(self):
#         return self.StaffName

class DataEntry_backup(models.Model):
    dateofvisit = models.DateField()
    bemiscode = models.CharField(max_length=6)
    schoolname = models.CharField(max_length=200)
    district = models.CharField(max_length=50)
    StaffName = models.CharField(max_length=180)
    # StaffCode = models.ForeignKey(staff_Parameter, on_delete=models.CASCADE)
    region = models.CharField(max_length=50)
    schoolStatus = models.CharField(max_length=80)

    girls_reg_kachi = models.CharField(max_length=3,default=None)
    girls_reg_one = models.CharField(max_length=3,default=None)
    girls_reg_two = models.CharField(max_length=3,default=None)
    girls_reg_three = models.CharField(max_length=3,default=None)
    girls_reg_four = models.CharField(max_length=3,default=None)
    girls_reg_five = models.CharField(max_length=3,default=None)
    
    boys_reg_kachi = models.CharField(max_length=3,default=None)
    boys_reg_one = models.CharField(max_length=3,default=None)
    boys_reg_two = models.CharField(max_length=3,default=None)
    boys_reg_three = models.CharField(max_length=3,default=None)
    boys_reg_four = models.CharField(max_length=3,default=None)
    boys_reg_five = models.CharField(max_length=3,default=None)
    
    girls_kachi = models.CharField(max_length=3,default=None)
    girls_one = models.CharField(max_length=3,default=None)
    girls_two = models.CharField(max_length=3 ,default=None)
    girls_three = models.CharField(max_length=3,default=None)
    girls_four = models.CharField(max_length=3,default=None)
    girls_five = models.CharField(max_length=3,default=None)

    boys_kachi = models.CharField(max_length=3,default=None)
    boys_one = models.CharField(max_length=3,default=None)
    boys_two = models.CharField(max_length=3,default=None)
    boys_three = models.CharField(max_length=3,default=None)
    boys_four = models.CharField(max_length=3,default=None)
    boys_five = models.CharField(max_length=3,default=None)
    
    ptscms_enroll = models.CharField(max_length=3)
    ptsmc_designation = models.CharField(max_length=280)
    
    stationary_purchased = models.CharField(max_length=3,default=None)
    stationary_amount_pkr = models.CharField(max_length=8,default=None)
    student_performance = models.CharField(max_length=200,default=None)

    dateofpurchase = models.DateField()
    stu_att_register_available = models.CharField(max_length=3 ,default=None)
    stu_att_register_update =  models.CharField(max_length=3 ,default=None)
    teach_att_register_available = models.CharField(max_length=3 ,default=None) 
    teach_att_register_update = models.CharField(max_length=3 ,default=None)
    aw_register_available = models.CharField(max_length=3 ,default=None)
    aw_register_update = models.CharField(max_length=3 ,default=None) 
    cash_register_available = models.CharField(max_length=3,default=None)
    cash_register_update = models.CharField(max_length=3 ,default=None)
    stock_register_available = models.CharField(max_length=3 ,default=None)
    stock_register_update = models.CharField(max_length=3 ,default=None)
    log_register_available = models.CharField(max_length=3 ,default=None)
    log_register_update = models.CharField(max_length=3 ,default=None)
    meet_register_available = models.CharField(max_length=3 ,default=None)
    meet_register_update = models.CharField(max_length=3 ,default=None)

    descriptions = models.TextField(
                    max_length=10000,
                    default='',
                    blank=True,
                    db_column='descriptions',
                    db_collation='utf8_general_ci',
                )


    # Add more fields that match the structure of the JSON data
    unique_together = ('dateofvisit', 'bemiscode', 'schoolname')
    # unique_together = ('dateofvisit', 'bemiscode', 'schoolname', 'district')
    
    class Meta:  
        verbose_name_plural = 'DataEntry_backup'
        

    def __str__(self):
        return f"checklist of {self.schoolname}"
    


