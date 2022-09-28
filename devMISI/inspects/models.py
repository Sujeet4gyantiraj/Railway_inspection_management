from django.db import models
from asyncio.windows_events import NULL
from inspects import managers
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone
from .choices import INSPECTION_TYPE

# Create your models here.



class error_Table(models.Model):
    log_no=models.BigAutoField(primary_key=True)
    fun_name=models.CharField(max_length=255,null=True,blank=True)
    user_id=models.CharField(max_length=40,null=True,blank=True)
    err_details=models.TextField(null=True,blank=True)
    err_date=models.DateField(auto_now_add=True)

    class meta:
        db_table="error_Table"


class MyUser(AbstractBaseUser):

    username = models.CharField(
        max_length=50, blank=True, null=True,  unique=True)
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50, blank=True,null=True)
    email = models.EmailField(verbose_name='email address', null=True)
    user_role = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_update = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = managers.MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile_no', ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name



class Insp_multi_location(models.Model):
    location_no=models.BigAutoField(primary_key=True)
    inspection_no=models.ForeignKey('Inspection_details',on_delete=models.CASCADE, null=True) #on_delete=models.CASCADE
    item=models.CharField(max_length=50,null=False)
    type=models.CharField(max_length=5, null=True)
    d_flag=models.IntegerField(default=0)

class Inspection_details(models.Model):
    inspection_no=models.BigAutoField(primary_key=True)
    inspection_note_no=models.CharField(max_length=40, blank=True, null=True)
    inspection_officer=models.ForeignKey('myadmin.Level_Desig',on_delete=models.CASCADE, null=True) #on_delete=models.CASCADE
    inspection_title=models.CharField(max_length=200, blank=False, null=True)
    # zone=models.CharField(max_length=10, blank=False, null=False)
    # division=models.CharField(max_length=10, blank=False, null=False)
    # dept=models.CharField(max_length=20, blank=False, null=True)
    # location=models.CharField(max_length=20, blank=False, null=False)
    # inspected_on=models.DateField(auto_now=False, null=False)
    target_date=models.DateField(null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    report_path=models.CharField(max_length=50, blank=False, null=True)
    status_flag=models.IntegerField(default=0)
    send_to=models.CharField(max_length=100, blank=False, null=True)
    modified_by=models.CharField(max_length=100, blank=False, null=True)
    # ForeignKey('empmast',on_delete=models.CASCADE, null=True,related_name='modified_by')
    created_by=models.CharField(max_length=100, blank=False, null=True)
    # ForeignKey('empmast',on_delete=models.CASCADE, null=True,related_name='created_by')
    item_type=models.CharField(max_length=10, blank=False, null=True)
    status = models.CharField(max_length=10, blank=False, null=True)
    insp_last=models.IntegerField(blank=False, null=True)
    start_date=models.DateField(auto_now=False, null=True)
    # end_date=models.DateField(auto_now=False, null=True)
    inspected_on=models.DateField(auto_now=False, null=True)

class Item_details(models.Model):
    item_no=models.BigAutoField(primary_key=True)   
    item_title=models.CharField(max_length=100, blank=False, null=True)
    inspection_no=models.ForeignKey('Inspection_details', on_delete=models.CASCADE, null=True)
    status=models.CharField(max_length=10, blank=False, null=True)
    status_flag=models.IntegerField(default=0)
    observation=models.CharField(max_length=500, blank=False, null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    modified_by=models.CharField(max_length=15, blank=False, null=True)
    created_by=models.CharField(max_length=15, blank=False, null=True)
    target_date=models.DateField(null=True)
    item_subtitle=models.CharField(max_length=500, blank=False, null=True)
    type=models.CharField(max_length=3, blank=False, null=True)
    item_link=models.CharField(max_length=20, blank=False, null=True)
    des_id=models.CharField(max_length=8, blank=False, null=True)
    priority=models.IntegerField(default=0)



class Insp_mail_details(models.Model):
    mail_no=models.BigAutoField(primary_key=True)   
    inspection_no=models.ForeignKey('Inspection_details', on_delete=models.CASCADE, null=True)
    subject=models.CharField(max_length=100, blank=False, null=True)
    body=models.CharField(max_length=500, blank=False, null=True)
    send_to = models.CharField(max_length=2000, blank=False, null=True)
    send_desig = models.CharField(max_length=100, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True)
    area = models.CharField(max_length=10, blank=False, null=True)


class MsgInsp(models.Model):
    msg_no=models.BigAutoField(primary_key=True)
    msg_to=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    msg_sent=models.CharField(max_length=500, blank=False, null=True)
    msg_reply=models.CharField(max_length=500, blank=False, null=True)
    msg_by=models.CharField(max_length=15, blank=False, null=True)

class Marked_Officers(models.Model):
    marked_no=models.BigAutoField(primary_key=True)
    marked_to=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    marked_emp=models.CharField(max_length=100, blank=False, null=True)
    # ForeignKey('empmast', on_delete=models.CASCADE, null=True)
    item_no=models.ForeignKey('Item_details', on_delete=models.CASCADE, null=True)
    compliance=models.CharField(max_length=50, blank=False, null=True)
    compliance_recieved_on=models.DateTimeField(auto_now=False, null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    modified_by=models.CharField(max_length=15, blank=False, null=True)
    created_by=models.CharField(max_length=15, blank=False, null=True)
    #new amisha
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    status_flag=models.IntegerField(null=True)
    reply_on=models.DateField(null=True)
    #gunjan
    revert=models.CharField(max_length=50,blank=False, null=True)
    reverted_on=models.DateField(null=True)
    status=models.CharField(max_length=1,blank=False, null=True)
    viewed_on=models.DateField(auto_now=False,null=True)


class Marked_Officers_forward(models.Model):
    marked_no_forward=models.BigAutoField(primary_key=True)
    marked_to_forward=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    marked_no=models.ForeignKey('Marked_Officers', on_delete=models.CASCADE, null=True)
    compliance_forward=models.CharField(max_length=50, null=True)
    compliance_recieved_on_forward=models.DateTimeField(auto_now=False, null=True)
    modified_on_forward=models.DateTimeField(auto_now=False, null=True)
    created_on_forward=models.DateTimeField(auto_now=False, null=True)
    modified_by_forward=models.CharField(max_length=10, blank=False, null=True)
    created_by_forward=models.CharField(max_length=10, blank=False, null=True)
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    #gunjan
    status_flag=models.IntegerField(null=True)
    reply_on=models.DateField(null=True)
    viewed_on=models.DateField(auto_now=False,null=True)

class Officers_Remark(models.Model):
    remark_no=models.BigAutoField(primary_key=True)
    marked_no=models.ForeignKey('Marked_Officers', on_delete=models.CASCADE, null=True)
    remark = models.CharField(max_length=200, blank=False, null=True)
    reply_received=models.CharField(max_length=50, blank=False, null=True)
    rejected_on=models.DateTimeField(auto_now=False, null=True)
    reply_on=models.DateTimeField(auto_now=False, null=True)
    status = models.CharField(max_length=10, blank=False, null=True)
    status_flag = models.IntegerField(default=0)
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    #gunjan
    marked_no_forward=models.ForeignKey('Marked_Officers_forward', on_delete=models.CASCADE, null=True)
    marked_desig_id=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)

class Corrigendum_Report(models.Model):
    report_no=models.BigAutoField(primary_key=True)
    marked_no=models.ForeignKey('Marked_Officers', on_delete=models.CASCADE, null=True)
    remark = models.CharField(max_length=200, blank=False, null=True)
    created_on=models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=10, blank=False, null=True)


class roles(models.Model):
    role = models.CharField(primary_key=True, max_length=50)
    parent = models.CharField(max_length=50, blank=True, null=True)
    # department_id=models.ForeignKey('department_master', on_delete=models.CASCADE, null=True)
    rly_unit=models.CharField(max_length=50, blank=True, null=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True,null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    delete_flag=models.BooleanField(default=False)
    department_code=models.ForeignKey('myadmin.departMast', on_delete=models.CASCADE, null=True)
    designation_code= models.CharField( max_length=20, blank=True, null=True)
    role_code = models.CharField( max_length=5, blank=True, null=True)
    shop_code=models.CharField(null = True,max_length =50)
    class Meta:
        
        db_table = 'dlw_roles'


class empmast(models.Model):
    hrms_id=models.ForeignKey('myadmin.hrms', on_delete=models.CASCADE, null=True)
    empno=models.CharField(max_length=20,primary_key=True)
    empname=models.CharField(max_length=50,null=True)
    empmname=models.CharField(max_length=50,null=True)
    emplname=models.CharField(max_length=50,null=True)
    birthdate=models.DateField(null=True)
    appointmentdate=models.DateField(null=True) 
    superannuation_date=models.DateField(null=True)
    gender=models.CharField(max_length=10,null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    contactno = models.CharField(max_length=10, blank=True, null=True)
    railwaygroup = models.CharField(max_length=50, blank=True, null=True)
    pc7_level=models.CharField(max_length=10,null=True)
    billunit=models.CharField(max_length=50,null=True)
    service_status=models.CharField(max_length=50,null=True)
    desig_longdesc=models.CharField(max_length=50,null=True)
    desig_id=models.CharField(max_length=50,null=True)
    station_des=models.CharField(max_length=100,null=True)
    dept_desc=models.CharField(max_length=50,null=True)
    subdepartment = models.CharField(max_length=50, blank=True, null=True)    
    currentzone = models.CharField(max_length=50, blank=True, null=True)
    currentunitdivision = models.CharField(max_length=100, blank=True, null=True)
    rl_type = models.CharField(max_length=50, blank=True, null=True)
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=500, blank=True, null=True)    
    rly_id=models.ForeignKey('myadmin.railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='empmast_rly_id')
    profile_modified_by = models.CharField( max_length=20, blank=True, null=True)
    profile_modified_on=models.DateField(null=True,blank=True)    




class user_request(models.Model):
    rly_id=models.ForeignKey('myadmin.railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='empmast_rly_id1')
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    empno=models.BigIntegerField(max_length=12, null=True)
    requestDate=models.DateField(null=True)
    remarks=models.CharField(max_length=200, null=True)
    request_type=models.CharField(max_length=50, null=True)
    status=models.CharField(max_length=20, null=True)




class Inspection_Checklist(models.Model):
    checklist_id=models.AutoField(primary_key=True)  
    checklist_title=models.CharField(max_length=100, blank=False, null=False)
    inspection_type=models.CharField(max_length=15, choices=INSPECTION_TYPE, default = '1' )
    status=models.CharField(max_length=10, blank=False, null=False)
    delete_flag=models.BooleanField(default=False)
    created_by=models.CharField(max_length=12, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    last_modified_by=models.CharField(max_length=12, blank=False, null=True)
    last_modified_on=models.DateTimeField(auto_now_add=True, null=True)
    


class Inspection_Activity(models.Model):
    activity_id=models.AutoField(primary_key=True)  
    checklist_id=models.ForeignKey('Inspection_Checklist', on_delete=models.CASCADE)
    activities=models.CharField(max_length=200, blank=False, null=False)
    delete_flag=models.BooleanField(default=False)
    created_by=models.CharField(max_length=12, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True, null=True)
    last_modified_by=models.CharField(max_length=12, blank=False, null=True)
    last_modified_on=models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.checklist_id

class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_title = models.CharField(max_length=50,null=True)
    description = models.CharField(max_length=250,null=True,blank=True)
    status=models.CharField(max_length=10, default=0,blank=False, null=False)
    delete_flag=models.BooleanField(default=False)
    created_by=models.CharField(max_length=12, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    last_modified_by=models.CharField(max_length=12, blank=False, null=True)
    last_modified_on=models.DateTimeField(auto_now_add=True, null=True)
 
    
class Event_activty(models.Model):
    activity_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey('Events',on_delete=models.CASCADE,null=True)
    Railways_act = models.CharField(max_length=30,null=True)
    Division_act = models.CharField(max_length=30,null=True)
    location3_act = models.CharField(max_length=30,null=True)
    date_to_act = models.DateField(null=True)
    status=models.CharField(max_length=10,default=0, blank=False, null=True)
    delete_flag=models.BooleanField(default=False)
    created_by=models.CharField(max_length=12, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    last_modified_by=models.CharField(max_length=12, blank=False, null=True)
    last_modified_on=models.DateTimeField(auto_now_add=True, null=True)
 

class custom_menu(models.Model):
    m_id=models.IntegerField(null=True)
    menu=models.CharField(max_length=50,null=True)
    url=models.CharField(max_length=100,null=True)
    perent_id=models.IntegerField(null=True)
    role=models.CharField(max_length=200,null=True)
    icons=models.CharField(max_length=100,null=True)    

    