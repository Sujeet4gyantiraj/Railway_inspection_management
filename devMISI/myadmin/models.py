
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from rest_framework.authtoken.models import Token
from django.conf import settings

from django import dispatch

# Create your models here.

class railwayLocationMaster(models.Model):
    rly_unit_code = models.AutoField(primary_key=True)
    location_code = models.CharField(max_length=10,null=True)
    location_type = models.CharField(max_length=5,null=True)
    location_description = models.CharField(max_length=100)
    parent_location_code = models.CharField(max_length=10)  
    last_update = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=30,null=True)
    station_code= models.CharField(max_length=5,null=True)
    rstype= models.CharField(max_length=15,null=True)
    location_type_desc= models.CharField(max_length=20,null=True)

class departMast(models.Model):
    
    department_code = models.CharField(primary_key=True, max_length =10)
    department_name=models.CharField(null = True,max_length =50, blank=True,unique=True)
    rly_unit_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    delete_flag=models.NullBooleanField(default=False,null=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)


class Post_master(models.Model):
    post_id = models.AutoField(primary_key=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    post_desc= models.CharField(max_length=50, blank=True, null=True)
    rly_unit_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    delete_flag=models.BooleanField(default=False)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)






class Level_Desig(models.Model):
    designation_code=models.AutoField(primary_key=True)  
    # cat_id=models.IntegerField(null=True)    
    designation=models.CharField(max_length=100,null=True)  
    department=models.CharField(max_length=50,null=True)   
    effectdate=models.DateTimeField(auto_now=True, null=True)
    # un_officer_id=models.IntegerField(null=True)
    # level=models.CharField(max_length=2,null=True)
    # designation_code = models.CharField(max_length=15,null=True)
    parent_desig_code= models.CharField(max_length=15,null=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    rly_unit=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    pc7_levelmin = models.IntegerField(null=True, blank=True)
    pc7_levelmax = models.IntegerField(null=True, blank=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    desig_user = models.ForeignKey('inspects.MyUser', on_delete=models.CASCADE, null=True)
    status= models.CharField( max_length=2, blank=True, null=True)
    empno=models.ForeignKey('inspects.empmast', on_delete=models.CASCADE, blank=True, null=True)
    d_level=models.CharField( max_length=4, blank=True, null=True)
    contactnumber=models.CharField(max_length=10, blank=True, null=True)
    official_email_ID=models.CharField(max_length=50, blank=True, null=True, unique=True)






class category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField( max_length=4, blank=True, null=True) 


class roless(models.Model):
    role = models.CharField(primary_key=True, max_length=50)
    parent = models.CharField(max_length=50, blank=True, null=True)
    # department_id=models.ForeignKey('department_master', on_delete=models.CASCADE, null=True)
    rly_unit=models.CharField(max_length=50, blank=True, null=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True,null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    delete_flag=models.NullBooleanField(default=False,null=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    designation_code= models.CharField( max_length=20, blank=True, null=True)
    role_code = models.CharField( max_length=5, blank=True, null=True)
    shop_code=models.CharField(null = True,max_length =50)



class Shop_section(models.Model):
    
    section_code = models.CharField( max_length =10)
    section_id = models.CharField(primary_key=True,max_length =10)
    section_desc = models.CharField(null = True,max_length =150)
    shop_code = models.CharField(null = True,max_length =50)
    shop_id = models.CharField(null = True,max_length =50)
    flag = models.CharField(null = True,max_length =1)
    rly_unit_code=models.CharField(max_length =3,null=True,blank=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True,null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True,blank=True)

#     class Meta:
        
#         db_table = 'myadmin_shop_section'


class custom_menu(models.Model):
    m_id=models.IntegerField(null=True)
    menu=models.CharField(max_length=50,null=True)
    url=models.CharField(max_length=100,null=True)
    perent_id=models.IntegerField(null=True)
    role=models.CharField(max_length=200,null=True)


class empmastnew(models.Model):
    sno = models.IntegerField(primary_key=True)
    emp_id=models.CharField(max_length=100,null=True)
    # models.ForeignKey('inspects.empmast', on_delete=models.CASCADE)
    shop_section = models.CharField(null = True,max_length =50)


class locationMaster(models.Model):
    pincode = models.IntegerField(primary_key=True)
    district = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    city  = models.CharField(max_length=50, default="NA")


    class Meta:
        db_table = 'locationMaster'


class AdminMaster(models.Model):
    code = models.BigAutoField(primary_key=True)
    address = models.CharField(max_length=100)
    pincode = models.ForeignKey(locationMaster, on_delete=models.CASCADE)
    admin = models.CharField(max_length=30)
    admin_mobile = models.BigIntegerField(unique=True)
    admin_phone = models.CharField(max_length=12,null=True)
    admin_email = models.EmailField(unique=True)
    rly = models.ForeignKey(railwayLocationMaster, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    created_on=models.DateTimeField(auto_now_add=True,null=True)


    def _str_(self):
        return self.admin_email

    class Meta:
        db_table = 'AdminMaster'


class HRMS(models.Model):
    ipas_employee_id=models.CharField(max_length=15,null=False)    
    hrms_employee_id=models.CharField(primary_key=True,max_length=6,null=False)
    employee_first_name=models.CharField(max_length=150,null=True)
    employee_middle_name=models.CharField(max_length=150,null=True)
    employee_last_name=models.CharField(max_length=150,null=True)
    date_of_birth=models.DateField(null=True)
    appointment_date=models.DateField(null=True)
    superannuation_date=models.DateField(null=True)    
    gender=models.CharField(max_length=1,null=True)
    community_sr=models.CharField(max_length=3,null=True)
    service_status=models.CharField(max_length=50,null=True)
    billunit=models.CharField(max_length=7,null=True)
    railway_group=models.CharField(max_length=1,null=True)
    current_zone=models.CharField(max_length=10,null=True)
    current_unit_division=models.CharField(max_length=80,null=True)
    rltype=models.CharField(max_length=20,null=True)
    current_place=models.CharField(max_length=100,null=True)
    department=models.CharField(max_length=50,null=True)
    sub_department=models.CharField(max_length=50,null=True)
    designation=models.CharField(max_length=300,null=True) 
    paylevel=models.CharField(max_length=4,null=True)
    official_mobile_no=models.CharField(max_length=10,null=True)
    official_email_id=models.CharField(max_length=50,null=True)
    txn_timestamp=models.DateTimeField(null=True)


class station_master(models.Model):
    stnshortcode=models.CharField(primary_key=True,editable=False,unique=True,max_length=6)
    rly_id_id=models.ForeignKey('railwayLocationMaster',on_delete=models.CASCADE,blank=True, null=True)
    lastmodified_by= models.CharField( max_length=20, blank=True, null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    station_name=models.CharField(max_length=50)
    created_on=models.DateTimeField(auto_now=True)
    lastmodified_on=models.DateTimeField(auto_now=True)
    delete_flag=models.BooleanField(default=False)


class stationcat_master(models.Model):
    stnid=models.AutoField(primary_key=True,editable=False,unique=True)
    stn_category=models.CharField(max_length=50)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(auto_now=True)
    lastmodified_on=models.DateTimeField(auto_now=True)
    delete_flag=models.BooleanField(default=False)


class runningroom_master(models.Model):
    rrid=models.AutoField(primary_key=True)
    rr_name=models.CharField(max_length=50)
    rr_code=models.CharField(max_length=10, unique=True)
    stnshortcode=models.ForeignKey('station_master', on_delete=models.CASCADE, blank=True, null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(auto_now=True)
    lastmodified_on=models.DateTimeField(auto_now=True)
    delete_flag=models.BooleanField(default=False)


class traincat_master(models.Model):
    tcatid=models.AutoField(primary_key=True,editable=False,unique=True)
    tn_category=models.CharField(max_length=50)
    code=models.CharField(max_length=6, unique=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(auto_now=True)
    lastmodified_on=models.DateTimeField(auto_now=True)
    delete_flag=models.BooleanField(default=False)


class train_master(models.Model):
    tnid=models.AutoField(primary_key=True, editable=False, unique=True)
    train_no=models.CharField(max_length=6,unique=True)
    train_name=models.CharField(max_length=50)
    tn_category=models.CharField(max_length=20,blank=False,null=True)
    # ForeignKey('traincat_master',on_delete=models.CASCADE,null=False)
    stnsource_code=models.CharField(max_length=20,blank=False,null=True)
    # ForeignKey('station_master',on_delete=models.CASCADE,null=False)
    stndest_code=models.CharField(max_length=20,blank=False,null=True)
    # ForeignKey('station_master',on_delete=models.CASCADE,null=False)
    total_coach=models.IntegerField(max_length=2)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(auto_now=True)
    lastmodified_on=models.DateTimeField(auto_now=True)
    delete_flag=models.BooleanField(default=False)


class inspectiontype_master(models.Model):
    instypeid=models.AutoField(primary_key=True, editable=False, unique=True)
    name=models.CharField(max_length=50)
    shortcode=models.CharField(max_length=10,unique=True)
    entity=models.CharField(max_length=10)
    parent_id=models.CharField(max_length=10, unique=True)
    statuschecklist=models.IntegerField(max_length=1,blank=False,null=False)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(auto_now=True)
    lastmodified_on=models.DateTimeField(auto_now=True)
    delete_flag=models.BooleanField(default=False)

class section_master(models.Model):   
    secid = models.AutoField(primary_key=True,editable=False,unique=True)
    section_code=models.CharField(max_length=20,blank=False,null=True)
    secstart_code = models.CharField(max_length=20,blank=False,null=True)
    # ForeignKey('station_master',on_delete=models.CASCADE,null=True)
    secend_code = models.CharField(max_length=20,blank=False,null=True)
    # ForeignKey('station_master',on_delete=models.CASCADE,null=True)
    via=models.CharField(max_length=20,blank=False,null=True)
    # ForeignKey('station_master',on_delete=models.CASCADE,null=True)
    startkm = models.IntegerField(max_length=5)
    endkm = models.IntegerField(max_length=5)
    rly_id_id=models.ForeignKey('railwaylocationmaster',on_delete=models.CASCADE,null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(auto_now=True)
    lastmodified_on=models.DateTimeField(auto_now=True)
    delete_flag=models.BooleanField(default=False)



class Level_Desig_temp(models.Model):
    designation_code=models.AutoField(primary_key=True)  
    # cat_id=models.IntegerField(null=True)    
    designation=models.CharField(max_length=100,null=True)  
    department=models.CharField(max_length=50,null=True)   
    effectdate=models.DateTimeField(auto_now=True, null=True)
    # un_officer_id=models.IntegerField(null=True)
    # level=models.CharField(max_length=2,null=True)
    # designation_code = models.CharField(max_length=15,null=True)
    parent_desig_code= models.CharField(max_length=15,null=True)
    department_code=models.CharField(max_length=15,null=True)
    # ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    rly_unit=models.CharField(max_length=15,null=True)
    # ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    pc7_levelmin = models.IntegerField(null=True, blank=True)
    pc7_levelmax = models.IntegerField(null=True, blank=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    desig_user = models.CharField(max_length=15,null=True)
    # ForeignKey('inspects.MyUser', on_delete=models.CASCADE, null=True)
    status= models.CharField( max_length=2, blank=True, null=True)
    empno=models.CharField(max_length=15,null=True)
    # ForeignKey('inspects.empmast', on_delete=models.CASCADE, blank=True, null=True)
    d_level=models.CharField( max_length=4, blank=True, null=True)





class Level_Desig_temp1(models.Model):
    designation_code=models.AutoField(primary_key=True)  
    # cat_id=models.IntegerField(null=True)    
    designation=models.CharField(max_length=100,null=True)  
    department=models.CharField(max_length=50,null=True)   
    effectdate=models.DateTimeField(auto_now=True, null=True)
    # un_officer_id=models.IntegerField(null=True)
    # level=models.CharField(max_length=2,null=True)
    # designation_code = models.CharField(max_length=15,null=True)
    parent_desig_code= models.CharField(max_length=15,null=True)
    department_code=models.IntegerField(null=True)
    # ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    rly_unit=models.IntegerField(null=True)
    # ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    pc7_levelmin = models.IntegerField(null=True, blank=True)
    pc7_levelmax = models.IntegerField(null=True, blank=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    #desig_user = models.ForeignKey('inspects.MyUser', on_delete=models.CASCADE, null=True)
    desig_user=models.IntegerField(null=True)
    status= models.CharField( max_length=2, blank=True, null=True)
    #empno=models.ForeignKey('inspects.empmast', on_delete=models.CASCADE, blank=True, null=True)
    empno= models.CharField( max_length=50, blank=True, null=True)
    d_level=models.CharField( max_length=4, blank=True, null=True)
    contactnumber=models.CharField(max_length=10, blank=True, null=True)
    official_email_ID=models.CharField(max_length=50, blank=True, null=True, unique=True)

    
