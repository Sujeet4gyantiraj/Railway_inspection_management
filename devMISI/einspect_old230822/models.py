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

# Create your models here.

class einsp_roster(models.Model):
    erosterid=models.AutoField(primary_key=True,editable=False,unique=True)
    fromdate=models.DateTimeField()
    todate=models.DateTimeField()
    status=models.BooleanField(null=False,blank=False)
    rly_id_id=models.ForeignKey('myadmin.railwaylocationmaster',on_delete=models.CASCADE, null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(auto_now=True)
    lastmodified_on=models.DateTimeField(auto_now=True)
    delete_flag=models.BooleanField(default=False)


class roster_detail(models.Model):
    rostdetailid=models.AutoField(primary_key=True,editable=False,unique=True)
    roster_id=models.CharField(max_length=30)
    # ForeignKey('einsp_roster',on_delete=models.CASCADE, null=True)
    inspection_officer_id=models.CharField(max_length=30)
    doi=models.DateTimeField(auto_now=True)
    inspectiontype_id=models.ForeignKey('myadmin.inspectiontype_master',on_delete=models.CASCADE, null=True)
    inspectionof=models.CharField(max_length=30)
    section=models.CharField(max_length=30)
    # ForeignKey('section_master',on_delete=models.CASCADE, null=True)
    startstn=models.CharField(max_length=30)
    # ForeignKey('station_master',on_delete=models.CASCADE,null=True)
    endstn=models.CharField(max_length=30)
    # ForeignKey('station_master',on_delete=models.CASCADE,null=True)
    status=models.IntegerField(max_length=1, blank=False,null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(auto_now=True)
    lastmodified_on=models.DateTimeField(auto_now=True)
    delete_flag=models.BooleanField(default=False)





class questionare_master(models.Model):
    qid=models.AutoField(primary_key=True)
    instypeid_id=models.CharField(max_length=30)
    # ForeignKey('inspectiontype_master', on_delete=models.CASCADE, null=False)
    activity=models.CharField(max_length=200)
    choicetype=models.CharField(max_length=15, null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(auto_now=True)
    lastmodified_on=models.DateTimeField(auto_now=True)
    delete_flag=models.BooleanField(default=False)







class einspection_item_detail(models.Model):
    eitemid=models.AutoField(primary_key=True,editable=False,unique=True)
    einspno=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('einspection_detail',on_delete=models.CASCADE,null=False)
    qid=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('questionaire_master',on_delete=models.CASCADE,null=False)
    status=models.IntegerField(max_length=1,null=False)
    einsdetailid=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('einspection_detail',on_delete=models.CASCADE,null=False)
    value=models.CharField(max_length=10)
    remarks=models.CharField(max_length=100)
    target_date=models.DateTimeField()
    qtype=models.CharField(max_length=10,null=False)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(auto_now=True)
    lastmodified_on=models.DateTimeField(auto_now=True)
    delete_flag=models.BooleanField(default=False)


class einspection_details(models.Model):
    einspno=models.AutoField(primary_key=True,editable=False,unique=True)
    instypeid=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('inspectiontype_master',on_delete=models.CASCADE,null=False)
    inspection_officer_id=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('empmast',on_delete=models.CASCADE,null=False)
    inspected_on=models.DateTimeField(auto_now=False,null=True)
    inspection_title=models.CharField(max_length=200,blank=False,null=True)
    designation=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('level_desig',on_delete=models.CASCADE,null=False)
    inspection_note_no=models.CharField(max_length=40,blank=True,null=True)
    status=models.IntegerField(max_length=1,blank=False,null=False)
    dept=models.CharField(max_length=20, blank=False, null=True)
    report_path=models.CharField(max_length=50, blank=False, null=True)
    rly_id_id=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('railwaylocationmaster',on_delete=models.CASCADE,null=False)
    startstn=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('station_master',on_delete=models.CASCADE,null=False)
    endstn=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('station_master',on_delete=models.CASCADE,null=False)
    entitydetails=models.CharField(max_length=30,blank=False,null=True)
    entityid=models.CharField(max_length=10,null=False)
    rostetrdetail_id=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('roster_details',on_delete=models.CASCADE,null=False)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(auto_now=False,null=True)
    lastmodified_on=models.DateTimeField(auto_now=False,null=True)
    delete_flag=models.BooleanField(default=False)


class einsp_marked(models.Model):
    id=models.AutoField(primary_key=True, editable=False, unique=True)
    eitemid=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('einspection_item_detail',on_delete=models.CASCADE,null=False)
    marked_to=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('level_desig',on_delete=models.CASCADE,null=False)
    marked_emp_id=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('empmast',on_delete=models.CASCADE,null=False)
    compliance=models.CharField(max_length=50, blank=False, null=True)
    compliance_recieved_on=models.DateTimeField(auto_now=False, null=True)
    status_flag=models.IntegerField(max_length=1, blank=False,null=True)
    revert=models.CharField(max_length=50,blank=False,null=True )
    reverted_on=models.DateTimeField(auto_now=False,null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(auto_now=True)
    lastmodified_on=models.DateTimeField(auto_now=True)
    delete_flag=models.BooleanField(default=False)

