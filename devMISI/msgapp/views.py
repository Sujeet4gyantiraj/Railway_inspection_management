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
from inspects import models as m1
from myadmin import models
import json
from django.db.models import Q
from django.db.models import Max
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mass_mail
import math
user = get_user_model()
from datetime import datetime
from inspects.utils import render_to_pdf
from msgapp import models as m
from xhtml2pdf import pisa
from django.template.loader import get_template
from myadmin import models

import random
from django.db.models import Subquery,Sum,Count

# Create your views here.
def messeging_form(request):
    empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    empnumber=None
    if empnox:
        empno = empnox[0].empno
        empnumber = empnox[0].empno_id
        print(empno)
    empdata = models.Level_Desig.objects.filter(empno__myuser_id=request.user).values('designation', 'empno__empname','empno__empmname','empno__emplname', 'empno')
    print(empdata)
    if empdata:
        desig_longdesc = empdata[0]['designation']
    else:
        desig_longdesc ='NA'
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code')
    list2=[]
    for i in list1:
            # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(parent_location_code='NR')& Q(location_type='DIV')).values('location_code')
    print(list3)
    list4=[]
    list5 =[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code']) 
    try:
        
        list5=list(models.Level_Desig.objects.all().values('designation','designation_code'))  
    except Exception as e:
        print("e==",e)  
    list6=models.departMast.objects.all().values('department_name')
    alldesig=models.Level_Desig.objects.values('designation').distinct().order_by('designation')
    print('6666666666666666666666666666666666')

    desg_no=[]
    abc=m1.Marked_Officers.objects.filter(item_no__inspection_no__in=m1.Inspection_details.objects.filter(created_by=empnumber).values('inspection_no'),marked_to__isnull=False).values('marked_to__designation').annotate(total=Count('marked_to__designation')).order_by()
    lst=sorted(abc, key = lambda i: i['total'],reverse=True)
    for i in range(len(lst)):
        exi=models.Level_Desig.objects.filter(designation=lst[i]['marked_to__designation']).values('empno')
        if exi.count():
            desg_no.append({'designation':lst[i]['marked_to__designation'],'empno':exi[0]['empno']})

    context={
            'Zone':list2 ,
            'division':list4,
            'marked_to':list5,
            'department':list6,
            'desig': desig_longdesc,
            'alldesig':alldesig,
            'desg_no':desg_no,
            
            }
    # try:
    print('ffffffffffffffffffffffffffff')
    if request.method=="GET" :
        div=request.GET.get('div_1')
        rly = request.GET.get('rly_1')
        message = request.GET.get('message')
        print(div,rly,'2222222222222222222222222222222222222')

        # print("@@@@@@@@@@@@@@@@@@@")
    
        print('-----------', request.user)
        print('-----------', request.user.username)
        print('-----------', request.user.email)
        
        



        
        
        #m.MessageInsp.objects.create(message_sent=message)
        # desig_longdesc = empdata[0]['desig_longdesc']
        # print('ttttttttttttttttttttttttttttttttttttttttttttttttttttttt', desig_longdesc)
        


        
        # print(list2,'_____________')
    
                
        return render(request,"messege_send_form.html")
    return render(request,"messege_send_form.html",context)


def msgreply(request):
    print('compliance-form-send')
    listgrid=[]
    count=1
    inspect_details1=m1.Inspection_details.objects.values().order_by('-inspection_no')
    print(inspect_details1,'01234')
    cuser=request.user.username
    desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    print(cuser,desigid,'CUSER, DESIGID')
    for i in inspect_details1:
        if m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],status_flag=2,marked_to_id=desigid):        
            temp={}
            temp['sr_no']=count
            temp['inspection_no']=i['inspection_no']
            temp['inspection_note_no']=i['inspection_note_no']
            temp['inspection_title']=i['inspection_title']
            t=models.Level_Desig.objects.filter(designation_code=i['inspection_officer_id']).values('designation')
            if len(t)!=0:
                temp['inspection_officer']=t[0]['designation'] 
            else:
                temp['inspection_officer']='NA'
            temp['inspected_on']=i['inspected_on'].strftime("%d/%m/%y") if i['inspected_on']!=None else 'NA'
            temp['file_path']=i['report_path']
            listgrid.append(temp)
            count=count+1
    print(listgrid,'-------------------------,send')
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').distinct().order_by('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').distinct().order_by('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().distinct().values('department_name').order_by('department_name')
    list6=[]
    for i in list5:
        # print(i['department_name'],'_________')
        list6.append(i['department_name'])        
    context={
        'zone':list2 ,
        'division':list4,
        'dept':list6,
        'listgrid':listgrid,
        # 'list_desig':list_desig,
    }
    print(list2,'_____________')
    return render(request,'msgreply.html',context) 