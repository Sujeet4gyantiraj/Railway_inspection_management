from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.generic import View
from myadmin.models import *
from myadmin.views import*
from django.contrib import auth
from datetime import datetime
import datetime
from myadmin import models 
from inspects import models as m1
# from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth.models import User,auth
from collections import defaultdict 
import json
import requests
import mimetypes
from tkinter import * 
from django.db.models import Max 
from tkinter import messagebox 
from django.db.models import Q
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db.models.functions import Substr
from django.db.models import Subquery,Sum,Count
import re,uuid,copy
from copy import deepcopy
from django.db.models import Sum,Subquery
from django.utils import formats
from django.utils.dateformat import DateFormat
from decimal import *
from django.db import connection
cursor = connection.cursor()
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mass_mail
import math
import shutil
nav=defaultdict()
subnav=defaultdict()
usermaster=defaultdict()
rolelist = []
navmenu=[] 
user = get_user_model()
from datetime import datetime
# Create your views here.

def fetch_details(request):
    empno=request.GET.get('empno')
    print(empno)
    if(HRMS.objects.filter(empno=empno).exists()):
        # designation_id=m1.HRMS.objects.filter(empno=emp_id)[0].designation_id
        # designation=models.Designation_Master.objects.filter(designation_master_no=designation_id)[0].designation
        name=HRMS.objects.filter(empno=empno)[0].employee_first_name
        # empname=m1.HRMS.objects.filter(empno=emp_id)[0].empname
        # rly_id=m1.HRMS.objects.filter(empno=emp_id)[0].rly_id_id
        # div_id=m1.HRMS.objects.filter(empno=emp_id)[0].div_id_id
        # email_idd=m1.HRMS.objects.filter(empno=emp_id)[0].email
        # print(rly_id,'___________')
        # print(div_id,'___________')
        print(name,'first name')
        # desigg=models.Level_Desig.objects.filter(designation_code=designation)[0].designation
        # rly_code=models.railwayLocationMaster.objects.filter(rly_unit_code=rly_id)[0].location_code
        # if div_id!=None:
        #     div_code=models.railwayLocationMaster.objects.filter(rly_unit_code=div_id)[0].location_code
        # else:
        #     div_code=''
        context={
            'name':str(name),
            # 'empname':str(empname),
            # 'rly_code':str(rly_code),
            # 'div_code':str(div_code),
            # 'desigg':str(desigg),
            # 'email_idd':str(email_idd),
        }
        return JsonResponse(context)
    

def employeeList(request):
    # current_user = request.user
    emp=m1.empmast.objects.all() 
    employees=m1.empmast.objects.all().order_by('empname') 
    rail=railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    division=list(railwayLocationMaster.objects.filter(location_type='DIV').values('location_code').distinct('location_code'))
    
    # category = m1.empmast.objects.filter(decode_paycategory__isnull=False).values('decode_paycategory').distinct()
    department=departMast.objects.filter(delete_flag=False).values('department_name').order_by('department_name').distinct()
    designation=Level_Desig.objects.values('designation').order_by('designation').distinct()
    
    context={
        'emp':emp,
        'department':department,
        'employees':employees,
        'sub':0,
        # 'category':category,
        'rail':rail,
        'user':usermaster,
        'division':division,
        'designation':designation,
        
     }
    return render(request, 'employeeList.html',context)


def viewEmployee_Det(request):
    
    if request.method == "GET":
        empno = request.GET.get('empno') 

        emp = m1.empmast.objects.filter(empno=empno)[0]
        print(empno,'empno')
        desig=[]
        if emp.pc7_level is not None:
            desig=list(Level_Desig.objects.filter(pc7_levelmin__lte=emp.pc7_level,pc7_levelmax__gte=emp.pc7_level).values('designation').order_by('designation').distinct())
            parentdesignation=list(Level_Desig.objects.filter(pc7_levelmin__gte =emp.pc7_level).values('designation').order_by('designation').distinct())
        print(desig)
        if emp.rl_type=='PRODUCTION UNIT' or emp.rl_type=='OFFICE' or emp.rl_type=='HEAD QUATER':
            div="null"
        else:
            div=emp.currentunitdivision
            
        if emp.subdepartment=='COMMON':
            dept="null"
        else:
            dept=emp.subdepartment
        context={ 
        'desigall':desig, 
        'parentdesignation':parentdesignation,
        'empno':emp.empno,
        'empname':emp.empname,
        'birthdate':emp.birthdate,
        'dateapp':emp.appointmentdate,
        'railway':emp.currentzone,
        'superdate':emp.superannuation_date,
        # 'division':emp.currentunitdivision,
        'division':div,
        'department':emp.dept_desc,
        'sub_depart':dept,
        'railwaytype':emp.rl_type,
        'stationdes':emp.station_des,
        # 'office_or':emp.office_orderno,
        'gender':emp.gender,
        # 'emp_inctype':emp.emp_inctype,
        # 'marital_status':emp.marital_status,
        'email':emp.email,
        'contactno':emp.contactno,
        'subdept':emp.subdepartment,
        'rltype':emp.rl_type,
        # 'ticket_no':emp.ticket_no,
        # 'idcard_no':emp.idcard_no,
        # 'emp_inctype':emp.emp_inctype,
        # 'inc_category':emp.inc_category,
        'desig':emp.desig_longdesc,
        
        # 'status':emp.emp_status,
        'dept':emp.dept_desc,
        # 'category':emp.decode_paycategory,
        # 'payband':emp.payband,
        # 'scalecode':emp.scalecode,
        'paylevel':emp.pc7_level,
        # 'gradepay':emp.payrate,
        # 'date_of_joining':emp.date_of_joining,
        # 'date_of_promotion':emp.date_of_promotion,
        'station_dest':emp.station_des,
        # 'wau':emp.wau,
        'billunit':emp.billunit,
        'service':emp.service_status,
        # 'emptype':emp.emptype,
        # 'medicalcode':emp.medicalcode,
        # 'tradecode':emp.tradecode,
        'role':emp.role,
        # 'shop_section':emp.shop_section,

        
    
        }  
    
    
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)

def  get_emp_detNew(request):
    if request.method == "GET" and request.is_ajax():
        empno = request.GET.get('empno') 
        obj = m1.empmast.objects.filter(empno=empno).all() 
        rno=len(obj)
        if rno==0:            
           context={            
            'rno':rno ,
           }  
        else:          
           context={  
            'rno':rno ,          
            'empno':obj[0].empno,
            'empname':obj[0].empname,
            'birthdate':obj[0].birthdate,
            'dateapp':obj[0].appointmentdate,
            'office_orderno':obj[0].office_orderno,
            'sex':obj[0].sex,
            
            'marital_status':obj[0].marital_status,
            'email':obj[0].email,
            'contactno':obj[0].contactno,
            
            'desig':obj[0].desig_longdesc,
            'status':obj[0].emp_status,
            'dept':obj[0].dept_desc,
            # 'category':obj[0].decode_paycategory,
            'payband':obj[0].payband,
            'scalecode':obj[0].scalecode,
            'paylevel':obj[0].pc7_level,
            'gradepay':obj[0].payrate,
            'joining_date':obj[0].date_of_joining,
            'date_of_promotion':obj[0].date_of_promotion,
            'station_dest':obj[0].station_des,
            'wau':obj[0].wau,
            'billunit':obj[0].billunit,
            'service':obj[0].service_status,
            'emptype':obj[0].emptype,
            'ticket_no':obj[0].ticket_no,
            'idcard_no':obj[0].idcard_no,
            'emp_inctype':obj[0].emp_inctype,
            'inc_category':obj[0].inc_category,
            
       
           }  
       
       
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


# def assign_role(request):
    
#     if request.method=='GET' or request.is_ajax():
#         print('hiiiii')
#         empno1 = request.GET.get('empno1')
#         print(empno1,'-------')
#         emprole = request.GET.get('emprole')
#         print(emprole,'----ttttt---')
#         department = request.GET.get('department')
#         print(department,'----uuuuuutt---')
#         designation = request.GET.get('designation')
#         print(designation,'---5555555t---')
#         parentdesig = request.GET.get('parentdesig')
#         print(parentdesig,'===================--------=========')
      
#         s_section = request.GET.get('s_section')
#         print(s_section,'___________________________')
#         s_section = json.loads(s_section)
#         sop =''
#         for o in s_section:
#             sop=sop+o+", "

#         print(sop,'---------', designation)
       
        
#         parent=Level_Desig.objects.filter(designation=parentdesig).values('designation_code')
#         print(parent)
#         employeeUpdate=empmast.objects.filter(empno=empno1).first()
#         var1=Level_Desig.objects.filter(designation=designation).first()
#         print(employeeUpdate,'----number')
#         var1.parent_desig_code=parent[0]['designation_code']
#         var1.save()
#         employeeUpdate.role=emprole
#         print(employeeUpdate.role)
#         empl=empmast.objects.filter(empno=empno1).first()
#         print(empl)
#         sno=empmastnew.objects.all().last().sno
        
#         empmastnew.objects.create(sno=sno+1,emp_id=empl,shop_section=sop)
#         employeeUpdate.parent=emprole 
#         employeeUpdate.dept_desc=department
       
#         employeeUpdate.desig_longdesc=designation
        
#         employeeUpdate.save()
       
#         messages.success(request, 'Successfully Activate!')
        
        
#     return JsonResponse({'saved':'save'})


def assign_role(request):
    
    if request.method=='GET' or request.is_ajax():
        print('hiiiii')
        
        empno1 = request.GET.get('empno1')
        print(empno1,'-------')
        rly = request.GET.get('rly')
        print(rly,'-------')
        div = request.GET.get('div')
        print(div,'-------')
       
        department = request.GET.get('department')
        print(department,'----uuuuuutt---')
        designation = request.GET.get('designation')
        print(designation,'---5555555t---')
        parentdesig = request.GET.get('parentdesig')
        print(parentdesig,'===================--------=========')
      
        # s_section = request.GET.get('s_section')
        # print(s_section,'___________________________')
        # s_section = json.loads(s_section)
        # sop =''
        # for o in s_section:
        #     sop=sop+o+", "

        # print(sop,'---------', designation)
        rly_id=""
        div_id=""
        if railwayLocationMaster.objects.filter(location_code=rly,location_type='ZR').exists():
            rly_id=railwayLocationMaster.objects.filter(location_code=rly,location_type='ZR')[0].rly_unit_code
        if railwayLocationMaster.objects.filter(location_code=div,parent_location_code=rly).exists():
            div_id=railwayLocationMaster.objects.filter(location_code=div,parent_location_code=rly)[0].rly_unit_code
        parent=Level_Desig.objects.filter(designation=parentdesig).values('designation_code')
        print(parent)
        employeeUpdate=m1.empmast.objects.filter(empno=empno1).first()
        var1=Level_Desig.objects.filter(designation=designation).first()
        print(employeeUpdate,'----number')
        var1.parent_desig_code=parent[0]['designation_code']
        var1.save()
       
        employeeUpdate.rly_unit_code_id=rly_id
        employeeUpdate.division_id=div_id
        
        # empl=m1.empmast.objects.filter(empno=empno1).first()
        # if m1.empmastnew.objects.all().exists():
        #     print('----000000')

        #     sno=m1.empmastnew.objects.all().last().sno
        # else:
        #     sno=0
        
        # empmastnew.objects.create(sno=sno+1,emp_id=empl,shop_section=sop)
        
        employeeUpdate.dept_desc=department
       
        employeeUpdate.desig_longdesc=designation
        
        employeeUpdate.save()
       
        messages.success(request, 'Successfully Activate!')
        
        
    return JsonResponse({'saved':'save'})

def getDesigbyDepartment(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
         
        obj=list(Level_Desig.objects.filter(department=department).values('designation').order_by('designation').distinct('designation'))
        print(obj,'____________________________________')
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)

def division_by_rly(request):
    if request.method == "GET" and request.is_ajax():
        rly=request.GET.get('rly')
        print(rly,'_________________________aaaaaa________________')
          
        division=list(railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=rly).order_by('location_code').values('location_code').distinct('location_code'))
        l=[]
        for i in division:
            l.append(i['location_code'])
        print(l)    
        context={
            'division':l,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)


def officer_bydiv(request):
    if request.method == "GET" and request.is_ajax():
        div_1 = request.GET.get('div_1')
         
        div_id=railwayLocationMaster.objects.filter(location_code=div_1)[0].rly_unit_code
        obj=list(m1.empmast.objects.filter(division_id=div_id).values('empname').order_by('empname'))
        context={
            'obj':obj,
        }
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


 

def getsection_byshop1(request):
    if request.method == "GET" and request.is_ajax():
        shop = request.GET.get('shop')
        print(shop)  
         
        shop_id=Shop_section.objects.filter(shop_code=shop).values('section_code')
        
       
        l=[]
        for i in shop_id:
            l.append(i['section_code'])
        print(l)    
        context={
            'shop_id':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)
 


def getrole_bydesig(request):
    if request.method == "GET" and request.is_ajax():
        designation = request.GET.get('designation')
        print(designation)  
         
        desig_id=Level_Desig.objects.filter(designation=designation)[0].designation_code
        print(desig_id)
        role=list(roless.objects.filter(designation_code=desig_id).values('role').distinct('role'))
        print(role)
        l=[]
        for i in role:
            l.append(i['role'])
        print(l)    
        context={
            'role':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)



def get_parentdesig(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
        paylevel1 = request.GET.get('paylevel1')
        print(paylevel1)  
        
        desig_id=Level_Desig.objects.filter(department=department,pc7_level__gte=paylevel1).values('designation')
        print(desig_id,'------')
        #parent=models.Level_Desig.objects.filter(designation=desig_id).values('designation')
        l=[]
        for i in desig_id:
            l.append(i['designation'])
        print(l)    
        context={
            'desig_id':l,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status=400)


def getshopcode_bydept(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
         
        dept_id=departMast.objects.filter(department_name=department)[0].department_code
        print(dept_id)
        shop_code=list(shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
        
        l=[]
        for i in shop_code:
            l.append(i['shop_code'])
        print(l)    
        context={
            'shop_code':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


def empregistNew(request): 
    current_user = request.user
    emp=m1.empmast.objects.filter(pk=current_user.username)  
    
    empst=m1.empmast.objects.all().distinct('emp_status','dept_desc').distinct('emp_status') 
    depart=m1.empmast.objects.all().values('dept_desc').distinct('dept_desc').order_by('dept_desc')
    railway=railwayLocationMaster.objects.all().values('location_code').distinct('location_code').order_by('location_code') 
    # shop=shop_section.objects.all().order_by('section_code') 
    employees=m1.empmast.objects.all().order_by('empname')
    # shoplist=list(shop_section.objects.filter().values('shop_code','shop_id').order_by('shop_code').distinct()) 
    # category = m1.empmast.objects.filter(decode_paycategory__isnull=False).values('decode_paycategory').distinct()
    context={
        'emp':emp,
        'employees':employees,
        'sub':0,
        # 'category':category,
        'lenm' :2,
       
        'railway':railway,         
        'empst':empst,
        
        'user':usermaster,
        'depart':depart,
    }
    if request.method=="POST":
        Submit=request.POST.get('Submit')
        empno=request.POST.get('empno')
        print(empno)
        empname=request.POST.get('empname')
        id_card=request.POST.get('id_card')
        ticket=request.POST.get('ticket')
        emp_inctype=request.POST.get('emp_inctype')
        inc_category=request.POST.get('inc_category')
        sex=request.POST.get('empsex')
        marital_status=request.POST.get('empmarital')            
        email=request.POST.get('empemail')            
        contactno=request.POST.get('empphone')
        shopno=request.POST.get('shop_sec')  
        sub_shop_sec=request.POST.get('sub_shop_sec')
        emp_inctype=request.POST.get('emptype') 
        empdesignation=request.POST.get('empdesignation') 
        emptdepartment=request.POST.get('emptdepartment') 
        empstatus=request.POST.get('empstatus') 
        office_orderno=request.POST.get('office_orderno') 
        birthdate=request.POST.get('dobdate')
        yj=birthdate[6:10]
        mj=birthdate[3:5]
        dj=birthdate[0:2]
        birthdate=yj+'-'+mj+'-'+dj
        dateapp=request.POST.get('dateapp')
        yj=dateapp[6:10]
        mj=dateapp[3:5]
        dj=dateapp[0:2]
        dateapp=yj+'-'+mj+'-'+dj
        gradepay=request.POST.get('gradepay') 
        paylevel=request.POST.get('paylevel')
        payband=request.POST.get('payband') 
        scalecode=request.POST.get('scalecode')
        category=request.POST.get('category')
        medicalcode=request.POST.get('medicalcode') 
        tradecode=request.POST.get('tradecode')
        joining_date=request.POST.get('joining_date')
        yj=joining_date[6:10]
        mj=joining_date[3:5]
        dj=joining_date[0:2]
        joining_date=yj+'-'+mj+'-'+dj
        date_of_promotion=request.POST.get('date_of_promotion')
        yj=date_of_promotion[6:10]
        mj=date_of_promotion[3:5]
        dj=date_of_promotion[0:2]
        date_of_promotion=yj+'-'+mj+'-'+dj
        station_dest=request.POST.get('station_dest') 
        wau=request.POST.get('wau')
        billunit=request.POST.get('billunit') 
        service=request.POST.get('service')
        emptype=request.POST.get('emptype')
        # try:
        #     if(dateapp != None):
        #         dateapp=datetime.datetime.strftime(dateapp, "%Y-%m-%d")
            
        #     if(birthdate != None):
        #         birthdate=datetime.datetime.strftime(birthdate, "%Y-%m-%d")

        #     if(joining_date != None):
        #         joining_date=datetime.datetime.strftime(joining_date, "%Y-%m-%d")
            
        #     if(date_of_promotion != None):
        #         date_of_promotion=datetime.datetime.strftime(date_of_promotion, "%Y-%m-%d")
        # except:
        #     messages.success(request,'Please enter valid date !')
        print('Submit',Submit)
        import datetime
        cuser=request.user
        now = datetime.datetime.now()
        
        

        # p=str(now).split(' ')
        
        # s=p[0].split('-')
        # day2 = s[0]
        # month2 = s[1]
        # year2 = s[2]
        
        # date1 = year2+"-"+month2+"-"+day2
        # print(date1)
        # time=str(p[1]).replace(':','')
        
        # if(cuser != None):
        #     uniquid= str(cuser)+""+date1+""+time[:6]
        password="dlw@123"
        if Submit=='Submit':
            if user.objects.filter(username=empno).exists():
                messages.info(request, "User Already exists!")
            else:
                
        
                # m1.empmast.objects.create(decode_paycategory=category, empno=empno, empname=empname, birthdate=birthdate,
                # appointmentdate=dateapp,sex=sex,marital_status=marital_status,email=email,contactno=contactno,emp_inctype=emp_inctype,
                # inc_category=inc_category,desig_longdesc=empdesignation,emp_status=empstatus,dept_desc=emptdepartment,
                # office_orderno=office_orderno, date_of_joining=joining_date, date_of_promotion=date_of_promotion, pc7_level=paylevel,
                # payrate=gradepay,payband=payband, scalecode=scalecode,wau=wau, station_des=station_dest,billunit=billunit,
                # service_status=service, emptype=emptype,idcard_no=id_card,ticket_no=ticket, 
                # medicalcode=medicalcode,tradecode=tradecode)
                m1.empmast.objects.create(empno=empno, empname=empname, birthdate=birthdate,
                appointmentdate=dateapp,sex=sex,marital_status=marital_status,email=email,contactno=contactno,emp_inctype=emp_inctype,
                inc_category=inc_category,desig_longdesc=empdesignation,emp_status=empstatus,dept_desc=emptdepartment,
                office_orderno=office_orderno, date_of_joining=joining_date, date_of_promotion=date_of_promotion, pc7_level=paylevel,
                payrate=gradepay,payband=payband, scalecode=scalecode,wau=wau, station_des=station_dest,billunit=billunit,
                service_status=service, emptype=emptype,idcard_no=id_card,ticket_no=ticket, 
                medicalcode=medicalcode,tradecode=tradecode)
                ID=user.objects.filter().order_by('-id')[0].id
                newuser = user.objects.create_user(id=ID+1,username=empno, password=password,email=email, first_name=empname)
                newuser.is_staff= True
                # newuser.is_superuser=True
                newuser.save()
                
                messages.success(request,'Record has successfully inserted !')
        else:
            # m1.empmast.objects.filter(empno=empno).update(decode_paycategory=category, emp_status=empstatus, sex=sex,marital_status=marital_status,email=email,contactno=contactno,emp_inctype=emp_inctype,inc_category=inc_category,  date_of_joining=joining_date, date_of_promotion=date_of_promotion,  empname=empname, birthdate=birthdate,appointmentdate=dateapp, desig_longdesc=empdesignation,dept_desc=emptdepartment,office_orderno=office_orderno, pc7_level=paylevel, payrate=gradepay,payband=payband, scalecode=scalecode,wau=wau,  station_des=station_dest,billunit=billunit, service_status=service, emptype=emptype,idcard_no=id_card,ticket_no=ticket,medicalcode=medicalcode,tradecode=tradecode)
            m1.empmast.objects.filter(empno=empno).update(emp_status=empstatus, sex=sex,marital_status=marital_status,email=email,contactno=contactno,emp_inctype=emp_inctype,inc_category=inc_category,  date_of_joining=joining_date, date_of_promotion=date_of_promotion,  empname=empname, birthdate=birthdate,appointmentdate=dateapp, desig_longdesc=empdesignation,dept_desc=emptdepartment,office_orderno=office_orderno, pc7_level=paylevel, payrate=gradepay,payband=payband, scalecode=scalecode,wau=wau,  station_des=station_dest,billunit=billunit, service_status=service, emptype=emptype,idcard_no=id_card,ticket_no=ticket,medicalcode=medicalcode,tradecode=tradecode)

            messages.error(request,'Record has successfully updated ')

         
    return render(request, 'empRegistrationnew.html',context)


def open_empregistNew(request, empno):
    emplist=m1.empmast.objects.get(empno=empno)
    railway=railwayLocationMaster.objects.filter(location_code='ZR').values('location_code')
    context={
        'emplist':emplist,
        'empno':empno,
        'railway':railway,
    }
    return render(request, 'empRegistrationNew.html',context)


def add_designation(request):
    unit=departMast.objects.filter(delete_flag=False).values('department_name').order_by('department_name').distinct('department_name')
    cat=category.objects.all().values('category').order_by('category').distinct('category')
    submitvalue = request.POST.get('submit')
    post=Post_master.objects.filter(delete_flag=True).values('post_desc').order_by('post_desc').distinct('post_desc')
    rltype=railwayLocationMaster.objects.all().values('location_type_desc').order_by('location_type_desc').distinct('location_type_desc')
    emp=m1.empmast.objects.all()
    print(emp,'_____________________________________________________')
    # designation=request.GET.get()
    post=Post_master.objects.values()
    context={
        'unit':unit,
        'post':post,
        'cat':cat,
        'post':post,
        'rltype':rltype,
        # 'railway':railway,
        # 'division':division,
    }
    # savedesig=request.POST.get('savedesig')
    #         if(savedesig=="savedesig"):
    #             Level_Desig.objects.create(designation_code=,designation=,department=,parent_desig_code=,rly_unit_id=,pc7_levelmax=,department_code_id=,pc7_levelmin=,d_level=,contactnumber=,official_email_ID=)
    
    return render(request,'add_designation.html', context)

def railwaytype(request):
    if request.method == "GET":
        railwaytype=request.GET.get('rltype')
        if(railwaytype=='OFFICE' or railwaytype=='HEAD QUATER' or railwaytype=='PRODUCTION UNIT' or railwaytype=='INSTITUTE'):
            railway=list(railwayLocationMaster.objects.filter(Q(location_type_desc='OFFICE')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='INSTITUTE')).values('location_code').distinct('location_code'))
        elif(railwaytype=='DIVISION' or railwaytype=='WORKSHOP' or railwaytype=='STORE' or railwaytype=='CONSTRUCTION'):
            railwa=railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('parent_location_code').distinct('parent_location_code')
            railway=[]
            for i in railwa:
                railway.append({'location_code': i['parent_location_code']})
            # railway_val=request.GET.get('rly')
            # print(railway_val)
            # division=list(railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').distinct('location_code'))
            # division=list(railwayLocationMaster.objects.filter(parent_location_code=railway_val).values('location_code').distinct('location_code'))
        else:
            railway=[]
        context={
            'railway':railway,
            # 'division':division,
        }
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)

def divbyrly(request):
    if request.method == "GET":
        rly=request.GET.get('rly')
        division=list(railwayLocationMaster.objects.filter(parent_location_code=rly).values('location_code').distinct('location_code'))
        context={
            'division':division,
        }
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)

def cal_desig(request):
    if request.method == "GET":
        post=request.GET.get('post')
        desig=list(Level_Desig.objects.values())
        return JsonResponse(desig, safe = False)
    return JsonResponse({"success":False}, status=400)

def getsection_byshop(request):
     if request.method == "GET" and request.is_ajax():
        shop = request.GET.get('shop')
        print(shop)  
         
        shop=list(Shop_section.objects.filter(shop_code=shop).values('section_desc').distinct('section_code'))
        print(shop)
    
        l=[]
        for i in shop:
            l.append(i['section_desc'])
        print(l)    
        context={
            'shop':l,
        } 
        return JsonResponse(context, safe = False)
     return JsonResponse({"success":False}, status=400)

  

def getshop_bydept(request):
    if request.method == "GET" and request.is_ajax():
        dept = request.GET.get('dept')
        print(dept)  
         
        dept_id=departMast.objects.filter(department_name=dept)[0].department_code
        print(dept_id)
        shop=list(Shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
        print(shop)
        l=[]
        for i in shop:
            l.append(i['shop_code'])
        print(l)    
        context={
            'shop':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


def post_bydept(request):
    if request.method == "GET" and request.is_ajax():
        dept1 = request.GET.get('dept1')
        print(dept1)
        dept_id=departMast.objects.filter(department_name=dept1)[0].department_code
        print(dept_id)
        post=list(Post_master.objects.filter(department_code_id=dept_id).values('post_desc').distinct('post_desc'))
        print(post)
        context={
            'post':post,
        }
       
        
       
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


def getpost_bydept(request):
    if request.method == "GET" and request.is_ajax():
        dept = request.GET.get('dept')
        print(dept)  
         
        dept_id=departMast.objects.filter(department_name=dept)[0].department_code
        print(dept_id)
        post=list(Post_master.objects.filter(department_code_id=dept_id).values('post_desc').distinct('post_desc'))
        print(post)
        l=[]
        for i in post:
            l.append(i['post_desc'])
        print(l)    
        context={
            'post':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)



def add_post(request):
    if request.method == 'POST' or request.is_ajax():
        # current_user = request.user
        # emp=empmast.objects.get(pk=current_user.username)
        emp=m1.empmast.objects.all()   
        
        # dept1 = request.POST.get('dept1')
        # post_name = request.POST.get('post_name')
        postname=request.POST.get('postname')
        postcode=request.POST.get('postcode')
        print(postname)
        print(postcode)
        # dept_id=departMast.objects.filter(department_name=dept1)[0].department_code
        # print(dept_id)
        if Post_master.objects.all().exists():

            id=Post_master.objects.all().last().post_id
            print(id,'___________________________________')
        else:
            id=0
            print(id,'___________________________________')
      
        Post_master.objects.create(post_id=id+1,post_code=postcode,post_desc=postname)
        messages.success(request,'Data saved successfully')
        
            
    return JsonResponse({'saved':'save'})

# def save_designation(request):
#     if request.method == 'POST' or request.is_ajax():
#         # current_user = request.user
#         # emp=models.empmast.objects.get(pk=current_user.username) 
#         emp=empmast.objects.all()
#         wau = request.POST.get('wau')
#         print(wau)
#         dept = request.POST.get('dept')
#         print(dept,'--------')

#         design = request.POST.get('design')
#         print(design,'___------')

#         level = request.POST.get('level')
#         level_=int(level)
        
#         c = ('%02d' % level_)
#         level1=c
        
#         print(level1,'uuuuvar1-----')


#         dept_id=departMast.objects.filter(department_name=dept)[0].department_code
#         print(dept_id,'-----------------------')

#         section=request.POST.get('section')
#         print(section,'---------------------------------------------')

#         shop=request.POST.get('shop')
#         print(shop,'_____hhhhh')
#         deptpost=request.POST.get('deptpost')
#         print(deptpost,'[[[[[[[[')


#         post=int(Post_master.objects.filter(department_code_id=dept_id)[0].post_id)
#         a = ('%02d' % post)
#         level2=a
        
#         print(level2,'-------level2-----')

#         print(post,'___________________________')
        
#         section_id=list(Shop_section.objects.filter(department_code_id=dept_id,shop_code=shop,section_code=section).values('section_id'))
#         print(section_id,'gggggggggggggttttttttttggggg')

        
       
#         sec_id=str(section_id[0]['section_id'])+level1+level2
#         print(sec_id)
#         if Level_Desig.objects.all().exists():

#             id=Level_Desig.objects.all().last().id
#             print(id,'___________________________________')
#         else:
#             id=0
#             print(id,'___________________________________')
        
#         if Level_Desig.objects.filter(designation=design).exists():
#             messages.error(request, 'Designation already present')
#         else:

#             Level_Desig.objects.create(id=id+1,department=dept,designation=design,pc7_level=level1,department_code_id=dept_id,designation_code=sec_id)
#             messages.success(request, 'Data Saved')
        
        

      
        
        
            
#     return JsonResponse({'saved':'save'})

def save_designation(request):
    if request.method == 'POST' or request.is_ajax():
        # current_user = request.user
        # emp=models.empmast.objects.get(pk=current_user.username) 
        emp=m1.empmast.objects.all()
        wau = request.POST.get('wau')
        print(wau)
        dept = request.POST.get('dept')
        print(dept,'--------')

        design = request.POST.get('design')
        print(design,'___------')

        level = request.POST.get('level')
        level_=int(level)
        
        c = ('%02d' % level_)
        level1=c
        
        print(level1,'uuuuvar1-----')


        dept_id=departMast.objects.filter(department_name=dept)[0].department_code
        print(dept_id,'-----------------------')

        # section=request.POST.get('section')

        # shop=request.POST.get('shop')
        # print(shop,'_____hhhhh')
        # # deptpost=request.POST.get('deptpost')
        # print(deptpost,'[[[[[[[[')


        # post=int(Post_master.objects.filter(department_code_id=dept_id)[0].post_id)
        # a = ('%02d' % post)
        # level2=a
        
        # print(level2,'-------level2-----')

        # print(post,'___________________________')
        # print('111111111111111')

        # section=Shop_section.objects.filter(section_desc=section)[0].section_code
        # print(section,'9999')
        # print(dept_id)
        # print(shop)
        # section_id=list(Shop_section.objects.filter(department_code_id=dept_id,shop_code=shop,section_code=section).values('section_id'))
        # print(section_id,'gggggggggggggttttttttttggggg')

        # section=Shop_section.objects.filter(shop_code=shop).values('section_code')

       
        # sec_id=str(section_id[0]['section_id'])+level1
        # print(sec_id)
        if Level_Desig.objects.all().exists():

            id=Level_Desig.objects.all().last().designation_code
            print(id,'___________________________________')
        else:
            id=0
            print(id,'___________________________________')
        
        if Level_Desig.objects.filter(designation=design).exists():
            messages.error(request, 'Designation already present')
        else:

            Level_Desig.objects.create(designation_code=id+1,department=dept,designation=design,pc7_level=level1,department_code_id=dept_id)
            messages.success(request, 'Data Saved')
        
        

      
        
        
            
    return JsonResponse({'saved':'save'})



def div_by_rly(request):

    if request.method == "GET" or request.is_ajax():
        rly=request.GET.get('rly')
        print(rly,'_________++++++++++++++++++++++________________')
          
        division=list(railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=rly).order_by('location_code').values('location_code').distinct('location_code'))
        l=[]
        for i in division:
            l.append(i['location_code'])
        print(l)    
        context={
            'division':l,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)



def shop_data(request):
    print('111111111111111111111111111111111111111')
    print(request.method)
    if request.method == 'POST' or request.is_ajax():
        print('1')
        dept = request.POST.get('dept')
        shop = request.POST.get('shop')
        print(',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',dept)
        print(shop)
        dept_id=departMast.objects.filter(department_name=dept)[0].department_code
        print(dept_id)
        count=1
        shopcode=Shop_section.objects.filter(department_code_id=dept_id).distinct('shop_id')
        # shopcode=list(shop_section.objects.filter(department_code_id=dept_id).distinct('shop_code')).last()
        print(shopcode)
        shopcode=shopcode.count()
        shopcode+=1
        print(shopcode,"+++++++++")
        c = ('%02d' % shopcode)
        shopcode1=c

        # for i in shopcode:
        #     c = ('%02d' % shopcode)
        #     shopcode1=c
        #     count+1
        #     print(shopcode1)
       
        print(shopcode1)
        
        shop_id=str(120)+str(dept_id)+str(shopcode1)
        print(shop_id)
        section_id=shop_id+'00'
        print(section_id)
        section_code=int(section_id[5:9])
        
        
        print(section_code,'--------------__________--------------------')
        Shop_section.objects.create(department_code_id=dept_id,shop_code=shop,shop_id=shop_id,section_id=section_id,section_code=section_code)
        messages.success(request,'Data saved successfully')
        
            
    return JsonResponse({'saved':'save'})


def section_data(request):
    if request.method == 'POST' or request.is_ajax():
        
        dept1 = request.POST.get('dept1')
        print(dept1)
        sectiondept = request.POST.get('sectiondept')
        print(sectiondept)
        sec = request.POST.get('sec')
        print(sec)
        dept_id=departMast.objects.filter(department_name=dept1)[0].department_code
        print(dept_id)
        if Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).exists():
            shopcode=Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).last().section_id
        print(shopcode,'shopcode------')
        if Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).exists():
            shopcode_id=Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).last().shop_id
        print(shopcode_id,'shopcode_id------')

        if Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).exists():

            section_code=Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).last().section_code
        print(section_code,'section_code------')
        
        shop_id=int(shopcode)+1
        sec_code=int(section_code)+1
        if Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).exists():

            Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).create(section_id=shop_id,section_desc=sec,shop_code=sectiondept,department_code_id=dept_id,shop_id=shopcode_id,section_code=sec_code)
            messages.success(request,'Data saved successfully')
        
            
    return JsonResponse({'saved':'save'})


def dept_data(request):
    if request.method == 'POST' or request.is_ajax():
        # current_user = request.user
        # emp=empmast.objects.get(pk=current_user.username).values('wau')
        # emp=models.empmast.objects.all()
        
        department = request.POST.get('department')
        # now = datetime.datetime.now()
        

        # p=str(now).split(' ')
        
        # s=p[0].split('-')
        # day2 = s[0]
        # month2 = s[1]
        # year2 = s[2]
        
        # date1 = year2+""+month2+""+day2
        
        # time=str(p[1]).replace(':','')
        obj=list(departMast.objects.filter(department_name=department).values('department_name').distinct())
        sc_1=int(departMast.objects.last().department_code)
        print(sc_1)
           
        print(obj,'obj')
        if len(obj)==0:
            print('a')
            departMast.objects.create(department_name=department, department_code=sc_1+1)
            messages.success(request,'Data saved successfully')
        else:
            messages.error(request,'Department Already Exists!')
            print('b')
            # railwayLocationMaster.objects.filter(location_code=location_code).update(location_type=location_type, location_description=desc, parent_location_code=ploco_code, location_type_desc=type_desc, rstype=rstype, station_code=st_code)
           
    return JsonResponse({'saved':'save'})

def shop_section(request):
    # current_user = request.user
    emp=m1.empmast.objects.all() 
    unit=departMast.objects.filter(delete_flag=False).values('department_name').order_by('department_name').distinct('department_name')
    list=[]
    cur= connection.cursor()
    cur.execute('''select department_name,shop_code,shop_id,section_code,section_id from myadmin_Shop_section a join myadmin_departMast b on
    a.department_code_id=b.department_code order by (b.department_name,a.shop_code,a.section_code) ''')
    d=cur.fetchall()
    print(d,'________________')
    for i in d:
        temp={}
        temp['department_name']=i[0]
        temp['shop_code']=i[1]
        temp['shop_id']=i[2]
        temp['section_code']=i[3]
        temp['section_id']=i[4]
        list.append(temp)
    print('list',list,'_____________________________')    
 
           
   
    context={
        'emp':emp,
        'list':list,
        # 'val':val,
        'unit':unit,
       
    }
    
    return render(request, 'shop_section.html',context)


def shop_bydept(request):
    if request.method == "GET" and request.is_ajax():
        dept = request.GET.get('dept')
        print("===================",dept)
        dept_id=departMast.objects.filter(department_name=dept)[0].department_code
        print("========id===========",dept_id)
        shop_code=list(Shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
        print(shop_code)
        context={
            'shop_code':shop_code,
        }
       
        
       
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)

def section_bydept(request):
    if request.method == "GET" and request.is_ajax():
        dept = request.GET.get('dept')
        sectiondept = request.GET.get('sectiondept')
        print(sectiondept)
        dept_id=departMast.objects.filter(department_name=dept)[0].department_code
        print(dept_id)
        section_desc=list(Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).values('section_desc').distinct('section_desc'))
        print(section_desc)
        context={
            'section_desc':section_desc,
        }
       
        
       
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


def RoleAdd(request):
    # cuser=request.user
    # usermaster=empmast.objects.filter(empno=cuser).first()
    # current_user = request.user
    # emp=empmast.objects.filter(pk=current_user.username).values('wau')
  
    list=[]
    
    val = roless.objects.all().filter(delete_flag=False).values('role','parent','department_code_id').order_by('role').distinct() 
    for i in val:
        temp={}
        temp['role']=i['role']
        temp['parent']=i['parent']
        if departMast.objects.filter(department_code=i['department_code_id']).exists():
            temp['department_name']=departMast.objects.filter(department_code=i['department_code_id'])[0].department_name 
        else:
            temp['department_name']='None'     
        list.append(temp)
    role = roless.objects.all().filter(delete_flag=False).values('role').order_by('role').distinct()
    empdep = departMast.objects.all().values('department_name').order_by('department_name').distinct()
    # shop = shop_section.objects.values('shop_code').order_by('shop_code').distinct()
    # users = []
    if request.method=="POST":
        rolename = request.POST.get('roldel')
        print(rolename)
        if rolename:
          
            custom_menu.objects.all().filter(role=rolename).delete()
            roless.objects.all().filter(role=rolename).update(delete_flag=True)
            userremove = m1.empmast.objects.all().values('empno').filter(role=rolename)
            for i in range(len(userremove)):
                # users.append(userremove[i]['empno'])
                m1.empmast.objects.filter(empno=userremove[i]['empno']).update(role=None,parent=None)
            # User.objects.filter(username__in=users).delete()
            messages.success(request, 'Successfully Deleted!')
        else:
            messages.error(request,"Error")
    context = {
       
        'roles' : role,
        'val':val,
        'empdep':empdep,
        # 'shop':shop,
        'list':list,
        # 'wau':emp[0]['wau'],
    }
    return render(request,'RoleAdd.html',context)


def ajaxDeleteRoleUser(request):
    if request.method == 'POST' or request.is_ajax():

        rolename= request.POST.get('roledel')
        if rolename:
            perlist = custom_menu.objects.filter(role=rolename).values('url').distinct()   
            custom_menu.objects.all().filter(role=rolename).delete()
            roless.objects.all().filter(role=rolename).update(delete_flag=True)
            userremove = m1.empmast.objects.all().values('empno').filter(role=rolename)
            for i in range(len(userremove)):
               
                m1.empmast.objects.filter(empno=userremove[i]['empno']).update(role=None,parent=None)
            
       
    return JsonResponse({'deleted':'delete'})





def ajaxRoleGen(request):
    
    if request.method=='POST' or request.is_ajax():
        
        # emp=models.empmast.objects.get(pk=current_user.username)  
        emp=m1.empmast.objects.all() 
        rolename = request.POST.get('rolename')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        shop = request.POST.get('shop1')
        shop1 = json.loads(shop)
        sop =''
        for o in shop1:
            sop=sop+o+", "

        print(sop,'---------', designation)
        role=roless.objects.filter(role=rolename)
        desig_id=Level_Desig.objects.filter( designation= designation)[0].designation_code
        print(desig_id)
        dept_id=departMast.objects.filter(department_name=department)[0].department_code
        print(dept_id)
        if len(role)==0:
            roless.objects.create(role=rolename,parent=rolename,department_code_id=dept_id,modified_by=emp.empno, rly_unit=emp.wau,shop_code=sop, designation_code=desig_id)            
            messages.success(request,"succesfully added!")
        else:
            messages.error(request,"This role already exists")
    return JsonResponse({'saved':'save'})


def getDepartmentbyroles(request):
    if request.method == "GET" and request.is_ajax():
        emptdepartment = request.GET.get('emptdepartment')
               
        if emptdepartment !=None: 
            obj=list(departMast.objects.filter(department=emptdepartment).values('designation').order_by('designation').distinct())
            
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)


def getDesigbyDepartment(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
         
        obj=list(Level_Desig.objects.filter(department=department).values('designation').order_by('designation').distinct('designation'))
        print(obj,'____________________________________')
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)


def getshopcode_bydept(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
         
        dept_id=departMast.objects.filter(department_name=department)[0].department_code
        print(dept_id)
        shop_code=list(Shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
        
        l=[]
        for i in shop_code:
            l.append(i['shop_code'])
        print(l)    
        context={
            'shop_code':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)

def adminuserHome(request):
    return render(request,"adminuserHome.html")

def admin_logout(request):
    try:
        logout(request)
        return HttpResponseRedirect('/login')
    except Exception as e: 
       print(e)

def inspect_logout(request):
    try:
        logout(request)
        return HttpResponseRedirect('/login')
    except Exception as e: 
       print(e)
       
def admin_changePassword(request):
    print('jjjjj')
    try:
        if request.method == "POST":
            try:
                oldpass = request.POST.get('oldPassword').strip()
                newpass = request.POST.get('confirmNewPassword').strip()
                loguser = request.user.pk

                if len(str(newpass).strip()) < 8 or oldpass == None or newpass == None:
                    # make an error manually to go into except block
                    raise ValueError('Password must be 8 chars')

                loguser = user.objects.get(pk=loguser)
                if loguser.check_password(oldpass):
                    loguser.set_password(newpass)
                    loguser.save()
                    print('jjjjj')
                    messages.success(request, "Password Changed successfully.")
                    return HttpResponseRedirect('/login')
                    print('done')
                else:
                    messages.error(request, "Invalid Credentials.")

            except Exception as e: 
                print(e,'aaaaaaaaaaaaaaa')
                messages.error(request, "Something went wrong.")
                return HttpResponseRedirect('/inspect_changePassword')
        return render(request, "inspect_changePassword.html")
    except Exception as e: 
        print(e)
        # try:
        #     models.error_Table.objects.create(fun_name="rkvy_changePassword",user_id=request.user,err_details=str(e))
        # except:
        #     print("Internal Error!!!")
        # #messages.error(request, 'Error : '+str(e))
        # return render(request, "commanerrorpage.html", {})

from collections import namedtuple

def headquarterMaster(request):
        if request.method == "POST":
            hq_code = request.POST.get('headquarter_code')
            print(',,,,,,,,,,,',hq_code)
            print('999999999999')
            hq_address = request.POST.get('headquarter_address')
            hq_pincode = request.POST.get('pincode')
            pincodeObj = models.locationMaster.objects.get(pk=hq_pincode)
            hq_admin = request.POST.get('headquarter_admin')

            hq_admin_mob = request.POST.get('admin_mobile')
            # change25
            hq_admin_phn = str(request.POST.get('admin_phone'))
            hq_admin_email = request.POST.get('admin_email')
            hq_rly = request.POST.get('headquarter_rly')
            print(hq_rly,'///////////////')
            hq_status = request.POST.get('headquarter_status')

            if hq_code:
                # update
                try:
                    headquarter_rlyObj = models.railwayLocationMaster.objects.get(location_code=hq_rly)

                    val="admin "+headquarter_rlyObj.location_code
                    hqObj = models.AdminMaster.objects.get(pk=hq_code)
                    userObj = user.objects.filter(first_name=val)[0]
                    try:
                        # if hq_admin_mob != userObj.official_mobileNo:
                        #         userObj.official_mobileNo = hq_admin_mob
                        #         userObj.save()
                                hqObj.admin_mobile = hq_admin_mob
                                
                    
                            
                            

                    except Exception as e:
                        print(e)
                        messages.error(
                            request, "Can't Update mobile no, new mobile you entered already exists.")
                        return HttpResponseRedirect('/headquarterMaster')

                    try:
                        if userObj.email != hq_admin_email:

                                email_body = f'''
                                   Hello {hq_admin},
                                   Your email for RKVY has been updated from {userObj.email} to {hq_admin_email}.
                                   Sincerely,
                                   RKVY Team
                                '''

                                try:
                                    
                                    # send_mail("Login Credentials for RKVY", email_body, 'crisdlwproject@gmail.com',
                                    #           [f'{userObj.email}'], fail_silently=False)

                                    #saud faisal (28-08-2021) -----
                                    subject="Login Credentials for RKVY"
                                    To=userObj.email
                                    email_body1='<p>'+email_body+'</p>'
                                    # MailSend(subject,email_body1,To)
                                    #end here

                                    userObj.email = hq_admin_email
                                    userObj.save()
                                    hqObj.admin_email = hq_admin_email
                                except Exception as e:
                                    print(e)
                                    messages.error(request, "Email failed.")
                                    return HttpResponseRedirect('/headquarterMaster')

                           
                    except Exception as e:
                        print(e,'0000000')
                        messages.error(
                            request, "Can't Update email, new email you entered already exists.")
                        return HttpResponseRedirect('/headquarterMaster')

                    
                    hqObj.address = hq_address
                    hqObj.pincode = pincodeObj
                    hqObj.admin = hq_admin
                    print('1111111111')

                    if hq_admin_phn:
                        hqObj.admin_phone = hq_admin_phn
                    # change25
                    else:
                        hqObj.admin_phone= '' 
                    if hq_rly != "":
                        hqObj.rly = models.railwayLocationMaster.objects.get(location_code=hq_rly)
                    hqObj.status = hq_status
                    hqObj.save()

                    messages.success(request, "Successfully Updated the Headquarter")
                    return HttpResponseRedirect('/headquarterMaster')

                except Exception as e:
                    print(e)
                    messages.error(request, "Something went wrong.")
                    return HttpResponseRedirect('/headquarterMaster')

            else:
                # create new
                print('9')
                print(hq_rly)


                headquarter_rlyObj = models.railwayLocationMaster.objects.get(location_code=hq_rly)
                print(headquarter_rlyObj)
                import datetime

                hqObj = models.AdminMaster( address=hq_address,admin=hq_admin,admin_mobile=hq_admin_mob,admin_email=hq_admin_email,status=hq_status, rly=headquarter_rlyObj,pincode=pincodeObj,created_on=datetime.datetime.now())
                print('00000000')
                if hq_admin_phn:
                    hqObj.admin_phone = hq_admin_phn
                
                try:
                    hqObj.save()
                    print('99')
                    uname=models.AdminMaster.objects.filter(rly_id=headquarter_rlyObj.rly_unit_code).count()
                    cnt=('%03d' % uname)
                    val2=str(headquarter_rlyObj.rly_unit_code)+str(cnt)
                    val="admin "+headquarter_rlyObj.location_code

                    _password = "Misi@123"
                    # if user.objects.filter(email=hq_admin_email).exists():
                    #     obj=user.objects.get(email=hq_admin_email)
                    #     obj.is_admin=True
                    #     obj.first_name=val
                    #     obj.username=val2
                    #     obj.user_role="admin_rly"
                    #     obj.save()

                    # else:
                    user.objects.create_user(username=val2, is_active=True,password=_password,email=hq_admin_email, first_name=val,is_admin=True,user_role="admin_rly")
                    # userObj = models.AuthUser(email=hq_admin_email, password=_password,
                    #                               first_name=hqObj.pk, last_name=str(hq_admin)[:30],username="admin"+"_"+hq_rly)
                    # userObj.is_active = True
                    # userObj.save()
                    # email_context = {
                        
                    #     'login_id': userObj.email,
                    #     'password': _password,
                    # }
                    print('00/////////')
                    # email_template_name = "accounts/email_headquarter_credentials.txt"
                    # email_body = render_to_string(
                    #     email_template_name, email_context)
                    # try:
                    #     # send_mail("Login Credentials for RKVY", email_body, 'crisdlwproject@gmail.com',
                    #     #           [f'{userObj.email}'], fail_silently=False)
                        
                    # #saud faisal (28-08-2021) -----
                    #     subject="Login Credentials for RKVY"
                    #     To=userObj.email
                    #     email_body1='<p>'+email_body+'</p>'
                    #     MailSend(subject,email_body1,To)
                    #     #end here
                        
                    # except Exception as e:
                    #     print(e)
                    #     userObj.delete()
                    #     hqObj.delete()
                    #     messages.error(request, "Email failed.")
                    #     return HttpResponseRedirect('/rkvy_headquarterMaster')

                except Exception as e:
                    print(e,'999999999999999999999999999')
                    messages.error(
                        request, "Headquarter already exists with this email or mobile no.")
                    return HttpResponseRedirect('/headquarterMaster')

                messages.success(request, "HeadQuarter added succesfully.")
                return HttpResponseRedirect('/headquarterMaster')

        #changes 12-08 Ritika Garg
        # headquarter = list(
        #     models.rkvy_headquarterMaster.objects.all().order_by('headquarter_code'))

        cursor = connection.cursor()
        cursor.execute("""SELECT hq.code, hq.address, hq.admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.status, r.location_code, hq.pincode_id, r.location_type, l.district, l.state FROM "myadmin_railwaylocationmaster" r ,"AdminMaster" hq, "locationMaster" l  where r.location_type!='DIV' and status='Active' and  hq.rly_id=r.rly_unit_code and hq.pincode_id=l.pincode order by hq.code""")

        # cursor.execute("""SELECT hq.headquarter_code, hq.headquarter_address, hq.headquarter_admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.headquarter_status, r.location_code, hq.pincode_id, r.location_type, l.district, l.state FROM "myadmin_railwaylocationmaster" r ,"headquarterMaster" hq, "locationMaster" l  where hq.headquarter_rly_id=r.rly_unit_code and hq.pincode_id=l.pincode order by hq.headquarter_code""")
        data1=namedtuplefetchall(cursor)
        # cursor.execute("""SELECT hq.code, hq.address, hq.admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.status, r.location_code, hq.pincode_id, r.location_type, l.district, l.state FROM "myadmin_railwaylocationmaster" r ,"AdminMaster" hq, "locationMaster" l  where r.location_type!='DIV' and hq.rly_id=r.rly_unit_code and hq.pincode_id=l.pincode order by hq.code""")


        return render(request, "headquarter.html", {'headquarter': data1})
        return render(request, "headquarter.html")
def editHeadquarter(request):
    try:
        if request.method == "POST":
            _id = int(request.POST.get("id"))
            #print(_id)

            headquarterData = models.AdminMaster.objects.filter(pk=_id)
            #print(headquarterData)
            city =headquarterData[0].pincode.district
            state = headquarterData[0].pincode.state
            location = headquarterData[0].rly.location_description
            print(location)
            headquarterData = list(headquarterData.values())
            #print(headquarterData)
            headquarterData[0]['headquarter_city'] = city
            headquarterData[0]['headquarter_state'] = state
            headquarterData[0]['headquarter_rly'] = location
            print(headquarterData)
            return JsonResponse(
                {
                    "status": 1,
                    "headquarterData": headquarterData,
                }
            )
        bono=[]
        return JsonResponse(
            {
                "status": 0,
                "bono":bono
            }
        )
    except Exception as e: 
        print(e)


def deleteHeadQuarter (request):
    try:
        if request.method == "POST":
            _id = int(request.POST.get("id"))
            obj = (models.AdminMaster.objects.filter(
                code=_id))[0]
            #print(obj)
            obj.status="InActive"
            obj.save()

            obj = user.objects.filter(email=email).update(is_admin=False)

            return JsonResponse({
                "status": 1,
            }
            )
        return JsonResponse(
            {
                "status": 0,
            }
        )
    except Exception as e: 
        print(e)

def buildInstituteRly(request):
    print('0')
    try:
        if request.method == "POST":
            zonetype = request.POST.get("zonetype")
            print(zonetype)
            parentzone = request.POST.get("parentzone")

            location = []

            print(',1111111111111111',parentzone)

           
            if zonetype == "OT":
                location = list(models.railwayLocationMaster.objects.filter().values('location_code', 'location_description').exclude(location_type__in=['PU','ZR']).distinct())
                print('o')
            elif parentzone == "":
                location = list(models.railwayLocationMaster.objects.filter(
                    location_type=zonetype).values('location_code', 'location_description').distinct())
            else:
                location = list(models.railwayLocationMaster.objects.filter(
                    location_type=zonetype, parent_location_code=parentzone).values('location_code', 'location_description').distinct())

            return JsonResponse({'location': location, })
        return JsonResponse({"success": False}, status=400)
    except Exception as e: 
        print(e)
        try:
            models.error_Table.objects.create(fun_name="buildInstituteRly",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")

def getParentZones(request):
    print('0;;;;')


def fetchEmployee(request):
    desc = request.GET.get('desc')
    print(desc)
    employees = list(m1.empmast.objects.filter(
                    rly_id__location_code=desc).values('empno').distinct())
    print(employees)
    return JsonResponse({'employees': employees, })


def fetchStateCity(request):
    try:
        if request.method == "POST":
            print('11111111')
            pincode = request.POST.get('pincode')
            pincodedata = 'NULL'
            print(pincode)
            print('9999999999')
            if models.locationMaster.objects.filter(pincode=pincode).exists():
                pincodedata = list(models.locationMaster.objects.filter(
                    pincode=pincode).values('pincode', 'district', 'state'))[0]
            #print(pincodedata)
            return JsonResponse({'status': 200, 'pincodedata': pincodedata})
        return JsonResponse({'status': 500, })
    except Exception as e: 
        print(e)
        try:
            models.error_Table.objects.create(fun_name="rkvy_fetchStateCity",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")

def fetchData(request):
    empno = request.GET.get('empno')
    print(empno)
    details = list(m1.empmast.objects.filter(
                    empno=empno).values('contactno','email').distinct())
    print(details)
    return JsonResponse({'details': details, })

def namedtuplefetchall(cursor):
    try:
        "Return all rows from a cursor as a namedtuple"
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]
    except Exception as e: 
        try:
            models.error_Table.objects.create(fun_name="namedtuplefetchall",user_id=request.user,err_details=str(e))
        except:
            print(e)
            print("Internal Error!!!")

def DivisonMaster(request):
        if request.method == "POST":
            hq_code = request.POST.get('divison_code')
            print(',,,,,,,,,,,',hq_code)
            print('999999999999')
            hq_address = request.POST.get('divison_address')
            hq_pincode = request.POST.get('pincode')
            pincodeObj = models.locationMaster.objects.get(pk=hq_pincode)
            hq_admin = request.POST.get('divison_admin')

            hq_admin_mob = request.POST.get('admin_mobile')
            # change25
            hq_admin_phn = str(request.POST.get('admin_phone'))
            hq_admin_email = request.POST.get('admin_email')
            hq_rly = request.POST.get('divison_rly')
            print(hq_rly,'///////////////')
            hq_status = request.POST.get('divison_status')

            if hq_code:
                # update
                try:
                    headquarter_rlyObj = models.railwayLocationMaster.objects.get(location_code=hq_rly)
                    val="admin "+headquarter_rlyObj.location_code

                    print('99999')
                    print(hq_code)
                    hqObj = models.AdminMaster.objects.get(pk=hq_code)
                    userObj = user.objects.filter(first_name=val)[0]
                    # print(userObj.official_mobileNo)
                    print(hq_admin_mob)
                    try:
                        # if hq_admin_mob != userObj.official_mobileNo:
                        #     userObj.official_mobileNo = hq_admin_mob
                        #     userObj.save()
                            hqObj.admin_mobile = hq_admin_mob

                                
                        
                            
                            

                    except Exception as e:
                        print(e,'0088888888800000000000000')
                        messages.error(
                            request, "Can't Update mobile no, new mobile you entered already exists.")
                        return HttpResponseRedirect('/DivisonMaster')

                    try:
                        print('99999999999')
                        if userObj.email != hq_admin_email:

                                email_body = f'''
                                   Hello {hq_admin},
                                   Your email for RKVY has been updated from {userObj.email} to {hq_admin_email}.
                                   Sincerely,
                                   RKVY Team
                                '''

                                try:
                                    
                                    # send_mail("Login Credentials for RKVY", email_body, 'crisdlwproject@gmail.com',
                                    #           [f'{userObj.email}'], fail_silently=False)

                                    #saud faisal (28-08-2021) -----
                                    subject="Login Credentials for RKVY"
                                    To=userObj.email
                                    email_body1='<p>'+email_body+'</p>'
                                    # MailSend(subject,email_body1,To)
                                    #end here

                                    userObj.email = hq_admin_email
                                    userObj.save()
                                    hqObj.admin_email = hq_admin_email
                                except Exception as e:
                                    print(e)
                                    messages.error(request, "Email failed.")
                                    return HttpResponseRedirect('/DivisonMaster')

                            
                    except Exception as e:
                        print(e,'0000000')
                        messages.error(
                            request, "Can't Update email, new email you entered already exists.")
                        return HttpResponseRedirect('/DivisonMaster')

                    
                    hqObj.address = hq_address
                    hqObj.pincode = pincodeObj
                    hqObj.admin = hq_admin
                    if hq_admin_phn:
                        hqObj.admin_phone = hq_admin_phn
                    # change25
                    else:
                        hqObj.admin_phone= '' 
                    if hq_rly != "":
                        hqObj.rly = models.railwayLocationMaster.objects.get(location_code=hq_rly)
                    hqObj.headquarter_status = hq_status
                    hqObj.save()

                    messages.success(request, "Successfully Updated the Divison")
                    return HttpResponseRedirect('/DivisonMaster')

                except Exception as e:
                    print(e)
                    messages.error(request, "Something went wrong.")
                    return HttpResponseRedirect('/DivisonMaster')

            else:
                # create new
                print('9')
                print(hq_rly)


                headquarter_rlyObj = models.railwayLocationMaster.objects.get(location_code=hq_rly)
                print(headquarter_rlyObj)
                import datetime
                hqObj = models.AdminMaster( address=hq_address,admin=hq_admin,admin_mobile=hq_admin_mob,admin_email=hq_admin_email,status=hq_status,rly=headquarter_rlyObj,pincode=pincodeObj,created_on=datetime.datetime.now())
                print('00000000.')
                if hq_admin_phn:
                    hqObj.admin_phone = hq_admin_phn
                
                try:
                    hqObj.save()
                    print('99')
                    uname=models.AdminMaster.objects.filter(rly_id=headquarter_rlyObj.rly_unit_code).count()
                    cnt=('%03d' % uname)
                    val2=str(headquarter_rlyObj.rly_unit_code)+str(cnt)
                    print(val2)
                    val="admin "+headquarter_rlyObj.location_code

                    _password = "Misi@123"
                    if user.objects.filter(email=hq_admin_email):
                        obj=user.objects.get(email=hq_admin_email)
                        obj.is_admin=True
                        obj.username=headquarter_rlyObj.rly_unit_code
                        obj.first_name=val
                        obj.user_role="admin_div"
                        obj.save()
                    else:
                        user.objects.create_user(username=val2, is_active=True,password=_password,email=hq_admin_email, first_name=val,is_admin=True,user_role="admin_div")
                    # userObj = models.AuthUser(email=hq_admin_email, password=_password,
                    #                               first_name=hqObj.pk, last_name=str(hq_admin)[:30],username="admin"+"_"+hq_rly)
                    # userObj.is_active = True
                    # userObj.save()
                    # email_context = {
                        
                    #     'login_id': userObj.email,
                    #     'password': _password,
                    # }
                    # email_template_name = "accounts/email_headquarter_credentials.txt"
                    # email_body = render_to_string(
                    #     email_template_name, email_context)
                    # try:
                    #     # send_mail("Login Credentials for RKVY", email_body, 'crisdlwproject@gmail.com',
                    #     #           [f'{userObj.email}'], fail_silently=False)
                        
                    # #saud faisal (28-08-2021) -----
                    #     subject="Login Credentials for RKVY"
                    #     To=userObj.email
                    #     email_body1='<p>'+email_body+'</p>'
                    #     MailSend(subject,email_body1,To)
                    #     #end here
                        
                    # except Exception as e:
                    #     print(e)
                    #     userObj.delete()
                    #     hqObj.delete()
                    #     messages.error(request, "Email failed.")
                    #     return HttpResponseRedirect('/rkvy_headquarterMaster')

                except Exception as e:
                    print('lllll')


                    print(e,'999999999999999999999999999')
                    messages.error(
                        request, "Divison already exists with this email or mobile no.")
                    return HttpResponseRedirect('/DivisonMaster')

                messages.success(request, "Divison added succesfully.")
                return HttpResponseRedirect('/DivisonMaster')

        #changes 12-08 Ritika Garg
        # headquarter = list(
        #     models.rkvy_headquarterMaster.objects.all().order_by('headquarter_code'))

        cursor = connection.cursor()
        cursor.execute("""SELECT hq.code, hq.address, hq.admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.status, r.location_code, hq.pincode_id, r.location_type, l.district, l.state FROM "myadmin_railwaylocationmaster" r ,"AdminMaster" hq, "locationMaster" l  where r.location_type='DIV' and status='Active' and hq.rly_id=r.rly_unit_code and hq.pincode_id=l.pincode order by hq.code""")
        data1=namedtuplefetchall(cursor)
        id=request.user.username
        id=id[0:len(id)-3]
        code=models.railwayLocationMaster.objects.filter(rly_unit_code=id)[0].location_code
        desc=models.railwayLocationMaster.objects.filter(rly_unit_code=id)[0].location_description
        print(desc)
        print(data1)
        div=list(models.railwayLocationMaster.objects.filter(parent_location_code=code,location_type='DIV').values('location_code','rly_unit_code'))
        print(div)
        context={
        'headquarter': data1,
        'div':div,
        'desc':desc,

        }

        return render(request, "divison.html", context)

def editDivison(request):
    try:
        if request.method == "POST" and request.is_ajax():
            print('sssssssssssss')
            print(request.POST.get("id"))
            _id = int(request.POST.get("id"))
            print(_id)

            divisonData = models.AdminMaster.objects.filter(pk=_id)
            #print(headquarterData)
            city =divisonData[0].pincode.district
            state = divisonData[0].pincode.state
            location = divisonData[0].rly.location_description
            print(location)
            divisonData = list(divisonData.values())
            #print(headquarterData)
            divisonData[0]['divison_city'] = city
            divisonData[0]['divison_state'] = state
            divisonData[0]['divison_rly'] = location
            print(divisonData)
            return JsonResponse(
                {
                    "status": 1,
                    "divisonData": divisonData,
                }
            )
        return JsonResponse(
            {
                "status": 0,
            }
        )
    except Exception as e: 
        print(e)

def deleteDivison (request):
    try:
        if request.method == "POST" and request.is_ajax():
            print('1')
            _id = int(request.POST.get("id"))
            print(_id)
            obj = (models.AdminMaster.objects.filter(
                code=_id))[0]
            #print(obj)
            obj.status="InActive"
            obj.save()

            obj = m1.MyUser.objects.filter(email=email).update(is_admin=False)

            return JsonResponse({
                "status": 1,
            }
            )
        return JsonResponse(
            {
                "status": 0,
            }
        )
    except Exception as e: 
        print(e)

