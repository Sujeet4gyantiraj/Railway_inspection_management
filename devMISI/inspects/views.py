from __future__ import division
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

from xhtml2pdf import pisa
from django.template.loader import get_template
from .choices import INSPECTION_TYPE

import random
from django.db.models import Subquery,Sum,Count

def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def InspSendMail(subject, To, context):
    html_message = render_to_string('insp_mail_template.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'mfgcris@cris.org.in'
    send_mail(subject, plain_message, from_email, To, html_message=html_message)

def send_otp(request):
    if request.method == 'GET':
        print('iiii_____')
        cuser=request.user
        email=request.GET.get("email")
        print(email)
       
        print(type(email),'-------email------')
        otp=generateOTP()
        print(otp,'___')
        htmlgen = 'Your OTP is '+otp
        # send_mail('OTP request',otp,'mfgcris@cris.org.in',[email], html_message=htmlgen)
        send_mail(
                    'OTP request', #subject
                     htmlgen, #message body
                    'mfgcris@cris.org.in', # from email
                    [email], fail_silently=False, #to email
                   
                )  
        return JsonResponse({'otp':otp}, safe = False)
    return JsonResponse({}, safe = False)



def send_otp2(request):
    if request.method == 'GET':
        username=request.GET.get('username')
        email=user.objects.filter(username=username)[0].email
        print(email)
       
        otp=generateOTP()
        print(otp,'___')
        htmlgen = 'Your OTP is '+otp
        #send_mail('OTP request',otp,'crisdlwproject@gmail.com',[email], html_message=htmlgen)
        # send_mail(
        #             'OTP request', #subject
        #              htmlgen, #message body
        #             'mfgcris@cris.org.in', # from email
        #             [email], fail_silently=False, #to email
                   
        #         )  
        return JsonResponse({'otp':otp}, safe = False)
    return JsonResponse({}, safe = False)

def draft_inspection_form(request):

    empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    if empnox:
        empno = empnox[0].designation_code

        inspection=m1.Inspection_details.objects.filter(status_flag=0, inspection_officer=empno).values().order_by('-inspection_no')
        for i in inspection:
            location = list(m1.Insp_multi_location.objects.filter(inspection_no=i['inspection_no']).values())
            print(location)
            i.update({'location_item': location})
    else:
        messages.error(request, 'You are not authorize to see inspection. Please contact to admin')
        return render(request,"draft_inspection.html")

    return render(request,"draft_inspection.html",{'list1':inspection})




def fetch_email_id(request):
    empno=request.GET.get('empno')
    email_id=request.GET.get('email_id')
    flag=0
    if(models.HRMS.objects.filter(empno=empno,email=email_id).exists()):
        flag=1
    else:
        flag=0   
        return JsonResponse({'flag':flag})

def check_details(request):
    empno=request.GET.get('empno')
    if(models.HRMS.objects.filter(ipas_employee_id=empno).exists()):
        empf_name=models.HRMS.objects.filter(ipas_employee_id=empno)[0].employee_first_name
        empm_name=models.HRMS.objects.filter(ipas_employee_id=empno)[0].employee_middle_name
        empl_name=models.HRMS.objects.filter(ipas_employee_id=empno)[0].employee_last_name
        if (empm_name == None and  empl_name == None):
            name=str(empf_name)
        elif(empm_name==None):
            name=str(empf_name) + " " + str(empl_name)
        elif(empl_name == None):
            name=str(empf_name) + " " + str(empm_name)
        else:
            name=str(empf_name) + " " + str(empm_name) + " " + str(empl_name)
        print(name)
        empno1=models.HRMS.objects.filter(ipas_employee_id=empno)[0].ipas_employee_id
        empname=models.HRMS.objects.filter(ipas_employee_id=empno)[0].employee_first_name
        empmname=models.HRMS.objects.filter(ipas_employee_id=empno)[0].employee_middle_name
        emplname=models.HRMS.objects.filter(ipas_employee_id=empno)[0].employee_last_name
        birthdate=models.HRMS.objects.filter(ipas_employee_id=empno)[0].date_of_birth
        appointmentdate=models.HRMS.objects.filter(ipas_employee_id=empno)[0].appointment_date
        superannuation_date=models.HRMS.objects.filter(ipas_employee_id=empno)[0].superannuation_date
        gender=models.HRMS.objects.filter(ipas_employee_id=empno)[0].gender
        billunit=models.HRMS.objects.filter(ipas_employee_id=empno)[0].billunit
        service_status=models.HRMS.objects.filter(ipas_employee_id=empno)[0].service_status
        pc7_level=models.HRMS.objects.filter(ipas_employee_id=empno)[0].paylevel
        station_des=models.HRMS.objects.filter(ipas_employee_id=empno)[0].current_place
        dept_desc=models.HRMS.objects.filter(ipas_employee_id=empno)[0].department
        desig_longdesc=models.HRMS.objects.filter(ipas_employee_id=empno)[0].designation
        email=models.HRMS.objects.filter(ipas_employee_id=empno)[0].official_email_id
        contactno=models.HRMS.objects.filter(ipas_employee_id=empno)[0].official_mobile_no
        railwaygroup=models.HRMS.objects.filter(ipas_employee_id=empno)[0].railway_group
        rl_type=models.HRMS.objects.filter(ipas_employee_id=empno)[0].rltype
        subdepartment=models.HRMS.objects.filter(ipas_employee_id=empno)[0].sub_department
        currentzone=models.HRMS.objects.filter(ipas_employee_id=empno)[0].current_zone
        currentunitdivision=models.HRMS.objects.filter(ipas_employee_id=empno)[0].current_unit_division
        hrms_id=models.HRMS.objects.filter(ipas_employee_id=empno)[0].hrms_employee_id
        if models.railwayLocationMaster.objects.filter(location_description=currentunitdivision).exists():
            rlyid=models.railwayLocationMaster.objects.filter(location_description=currentunitdivision)[0].rly_unit_code
            
        if(m1.empmast.objects.filter(empno=empno).exists()):
               
            m1.empmast.objects.filter(empno=empno).update(empname=empname,empmname=empmname,emplname=emplname,birthdate=birthdate,appointmentdate=appointmentdate,
                                        superannuation_date=superannuation_date,gender=gender,billunit=billunit,service_status=service_status,
                                        pc7_level=pc7_level,station_des=station_des,dept_desc=dept_desc,desig_longdesc=desig_longdesc,email=email,
                                        contactno=contactno,railwaygroup=railwaygroup,rl_type=rl_type,subdepartment=subdepartment,
                                        currentzone=currentzone,currentunitdivision=currentunitdivision)
        else:
            m1.empmast.objects.create(hrms_id_id=hrms_id,empno=empno1,empname=empname,empmname=empmname,emplname=emplname,birthdate=birthdate,appointmentdate=appointmentdate,
                                        superannuation_date=superannuation_date,gender=gender,billunit=billunit,service_status=service_status,
                                        pc7_level=pc7_level,station_des=station_des,dept_desc=dept_desc,desig_longdesc=desig_longdesc,email=email,
                                        contactno=contactno,railwaygroup=railwaygroup,rl_type=rl_type,subdepartment=subdepartment,
                                        currentzone=currentzone,currentunitdivision=currentunitdivision) 
        context={
            'name':str(name),
        }
        return JsonResponse(context)
    else:
        bono=[]        
        return JsonResponse(bono,safe = False)


def fetch_emp(request):
    email_id=request.GET.get('email_id')
    print(email_id)
        
    if(models.Level_Desig.objects.filter(official_email_ID=email_id).exists()):
        # designation_id=m1.HRMS.objects.filter(empno=emp_id)[0].designation_id
        # designation=models.Designation_Master.objects.filter(designation_master_no=designation_id)[0].designation
        # designation=models.HRMS.objects.filter(ipas_employee_id=emp_id)[0].designation
        # empf_name=models.HRMS.objects.filter(ipas_employee_id=emp_id)[0].employee_first_name
        # empm_name=models.HRMS.objects.filter(ipas_employee_id=emp_id)[0].employee_middle_name
        # empl_name=models.HRMS.objects.filter(ipas_employee_id=emp_id)[0].employee_last_name
        designation=models.Level_Desig.objects.filter(official_email_ID=email_id)[0].designation
        # if(empf_name==None):
        #     name=str(empm_name) + " " + str(empl_name)
        # elif(empm_name==None):
        #     name=str(empf_name) + " " + str(empl_name)
        # elif(empl_name==None):
        #     name=str(empf_name) + " " + str(empm_name)
        
        # rly=models.HRMS.objects.filter(ipas_employee_id=emp_id)[0].current_zone
        # division=models.HRMS.objects.filter(ipas_employee_id=emp_id)[0].current_unit_division
        # email_idd=models.HRMS.objects.filter(ipas_employee_id=emp_id)[0].official_email_id
        
        # desigg=models.Level_Desig.objects.filter(designation_code=designation)[0].designation
        # rly_code=models.railwayLocationMaster.objects.filter(rly_unit_code=rly_id)[0].location_code
        # if div_id!=None:
        #     div_code=models.railwayLocationMaster.objects.filter(rly_unit_code=div_id)[0].location_code
        # else:
        #     div_code=''
        context={
            # 'designation':str(designation),
            # 'empname':str(empname),
            # 'rly_code':str(rly_code),
            # 'div_code':str(div_code),
            # 'desigg':str(desigg),
            # 'email_idd':str(email_idd),
            # 'designation':str(designation),
            # 'rly':str(rly),
            # 'division':str(division),
            # 'email_idd':str(email_idd),
            'designation':str(designation),
        }
        return JsonResponse(context)
    else:
        bono=[]        
        return JsonResponse(bono,safe = False)
        
# def signup(request):
#     if request.method == "POST":
#         submit_form=request.POST.get('submit_form')
#         if(submit_form=="submit_form"):
#             empno=request.POST.get('emp_id')
#             empname=request.POST.get('empname')
#             designation=request.POST.get('designation')
#             email_id=request.POST.get('email_id')
#             password=request.POST.get('password')
#             rly_code=request.POST.get('rly_id')
#             rly_id=models.railwayLocationMaster.objects.filter(location_code=rly_code)[0].rly_unit_code
#             div_code=request.POST.get('div_id')
#             div_id=models.railwayLocationMaster.objects.filter(location_code=div_code)[0].rly_unit_code
#             if(user.objects.filter(first_name=empname,email=email_id).exists()):
#                 messages.success(request,'User Already Exists.')
#             else:    
#                 user.objects.create_user(first_name=empname,email=email_id,password=password)
#                 myuser_id=user.objects.filter(first_name=empname,email=email_id)[0].id
#                 print(myuser_id,'___________-')
#                 models.empmast.objects.create(empno=empno,empname=empname,desig_longdesc=designation,email=email_id,myuser_id_id=myuser_id
#                 ,rly_id_id=rly_id,div_id_id=div_id)
#                 # send_mail(
#                 #             'OTP request', #subject
#                 #              htmlgen, #message body
#                 #             'amishu321@gmail.com', # from email
#                 #             [email], fail_silently=False, #to email
                        
#                 #         )
#                 messages.success(request,'User Created successfully.')
#     return render(request,"signup.html")

def signup(request):
    try:
        id=user.objects.filter().order_by('-id')[0].id
        id+=1
        print(id)
        if request.method == "POST":
            submit_form=request.POST.get('submit_form')
            if(submit_form=="submit_form"):
                empno=request.POST.get('empno')
                empname=request.POST.get('empname')
                desig=request.POST.get('desig')
                email_id=request.POST.get('email_id')
                password=request.POST.get('password')
                status=request.POST.get('status')
                print('1')
                print(desig)
                # models.Level_Desig.objects.filter(designation=desig).update(status=status,empno_id=empno)
                empvar=models.Level_Desig.objects.filter(empno_id=empno,official_email_ID=email_id)
                statusvar=models.Level_Desig.objects.filter(status=status,official_email_ID=email_id)
                uservar=user.objects.filter(username=email_id)
                obj = models.Level_Desig.objects.filter(empno_id=empno,status='P').values()
                print(obj)
                # if(uservar.exists()):
                #     user.objects.filter(username=email_id).update(first_name=empname,password=password,email=email_id)
                if(status=='D' and not models.Level_Desig.objects.filter(empno_id=empno,status='P').exists()):
                    messages.success(request,'Employee is not posted on any primary designation. ')
                elif(status=='D' and models.Level_Desig.objects.filter(empno_id=empno,status='P').exists()):
                    models.Level_Desig.objects.filter(designation=desig).update(status=status,empno_id=empno)
                    user.objects.filter(username=email_id).update(first_name=empname,password=password,email=email_id)
                elif(obj.exists() and status=='P'):
                    models.Level_Desig.objects.filter(empno_id=empno,status='P').update(status='V')
                    models.Level_Desig.objects.filter(designation=desig).update(status=status,empno_id=empno)
                    user.objects.filter(username=email_id).update(first_name=empname,password=password,email=email_id)
                elif(uservar.exists() and not empvar.exists() and not statusvar.exists()):
                    models.Level_Desig.objects.filter(designation=desig).update(status=status,empno_id=empno)
                    user.objects.filter(username=email_id).update(first_name=empname,password=password,email=email_id)
                    # messages.success(request,'User Already Exists.')
                elif(uservar.exists() and statusvar.exists() and not empvar.exists()):
                    models.Level_Desig.objects.filter(designation=desig).update(empno_id=empno)
                    user.objects.filter(username=email_id).update(password=password)
                elif(uservar.exists() and empvar.exists() and not statusvar.exists()):
                    models.Level_Desig.objects.filter(designation=desig).update(status=status)
                    user.objects.filter(username=email_id).update(password=password)
                elif(uservar.exists() and empvar.exists() and statusvar.exists()):
                    messages.success(request,'You are already registered.Use your login credentials')
                    #add forgot password
                else:    
                    print(empname,email_id)
                    id=user.objects.filter().order_by('-id')[0].id
                    id+=1
                    empno=request.POST.get('empno')
                    #update in level desig
                    user.objects.create_user(first_name=empname,username=email_id,password=password, id=id,email=email_id)
                    print('hlo')
                    # if(user.objects.filter(first_name=empname,username=empno).exists()):
                    #     myuser_id=user.objects.filter(first_name=empname,username=empno)[0].id
                    # print(myuser_id,'___________-')
        return render(request,"signup.html")
    except Exception as e:
        print(e)
def loginUser(request):
    # try:
        if request.method == "POST":
            _email = request.POST.get('email').strip()
            _password = request.POST.get('password').strip()
            print(_email,'____')
            print(_password,'_____')
            # obj3=models.rkvy_userEnrollment.objects.filter(user_id__email=_email).values('pending_stage')
            # check for existence
            userObj = authenticate(username=_email, password=_password)
            desig=models.Level_Desig.objects.filter(official_email_ID=_email).values('designation')
            
            global f_name
            global l_name
            global role_list 
            if userObj is not None:
                login(request, userObj)
                request.session["designation"] = desig[0]['designation']
                print("inside login&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print(userObj.username==None)
                print(userObj.username,'000000000')
                print(userObj.is_admin)
                f_name = userObj.first_name
                l_name = userObj.last_name
                if userObj.is_admin==True and userObj.user_role=="admin_super":
                    role_list = str(userObj.user_role)
                    print(role_list)
                    request.session["nav"] = custommenu()
                    return HttpResponseRedirect('/adminuserHome')
                elif userObj.is_admin==True and userObj.user_role=="admin_rly":
                    role_list = str(userObj.user_role)
                    request.session["nav"] = custommenu()
                    return HttpResponseRedirect('/zonaluserHome')
                elif userObj.is_admin==True and userObj.user_role=="admin_div":
                    role_list = str(userObj.user_role)
                    request.session["nav"] = custommenu()
                    return HttpResponseRedirect('/divisonuserHome')
                else:
                    role_list = "user"
                    request.session["nav"] = custommenu()
                    return HttpResponseRedirect('/dash_home')
                    # return render(request,"list_create_inspection_report.html")
                    
            else:
                #change 21-10
                if user.objects.filter(email=_email,is_active=False).exists():
                    messages.error(request, 'Request is not accepted yet.')
                else:
                    messages.error(request, 'Invalid Credentials')#till here 21-10
                #return HttpResponseRedirect('/rkvy_login')
                return render(request, "login.html")
        print('hhhh')
        return render(request, "login.html")



def custommenu(): 
    menustr=""
    role=role_list
    global menuname
    navmenu=m1.custom_menu.objects.filter(role=role).all().order_by('m_id')
    for menu in navmenu: 
        print(menu.menu)
        if menu.perent_id == 0 :
            menustr+="<li><div class='iocn-link'><a href="+menu.url+"><i class="+menu.icons+" ></i><span class='link_name'>"+menu.menu+"</span></a><i class='bx bxs-chevron-down arrow' ></i></div>"
            pid=menu.m_id
            sb1=m1.custom_menu.objects.filter(role=role,m_id=pid).values('menu')
            menuname = sb1[0]['menu']
            substr=submenu(navmenu,pid) 
            menustr+=substr
            menustr+="</li>" 
        elif menu.perent_id == -1 :
            menustr+="<li><a href="+menu.url+"><i class="+menu.icons+" ></i><span class='link_name'>"+menu.menu+"</span></a><ul class='sub-menu blank'><li><a class='link_name' href="+menu.url+">"+menu.menu+"</a></li></ul></li>"
    menustr+="<li><div class='iocn-link'><a href='#'><i class='bx bx-log-out-circle' ></i><span class='link_name'>"+f_name+"</span></a><i class='bx bxs-chevron-down arrow' ></i></div><ul class='sub-menu'><li><a  href='/inspect_changePassword'>Change Password</a></li><li><a href='/inspect_logout'  onclick='logoutConfirm();'>Logout</a></li></ul></li>"
    return menustr

def submenu(menubar,sid):
    role=role_list  
    menustr=""
    sb=m1.custom_menu.objects.filter(role=role,perent_id=sid).all().order_by('m_id')
    if len(sb)>0:   
        menustr="<ul class='sub-menu'><li><a class='link_name' href='#'>"+menuname+"</a></li>"
        for menu in menubar: 
            if menu.perent_id == sid :        
                menustr+="<li><a href="+menu.url+">"+menu.menu+"</a></li>"
                pid=menu.m_id
                substr=submenu(menubar,pid)
                menustr+=substr 
                menustr+="</li>"      
        menustr+="</ul>"
    return menustr


def check(request):
    print('111')
    username=request.POST.get('username')
    if user.objects.filter(username=username).exists() == True:
        status=1
    else:
        status=0
    print(status)
    return JsonResponse({'status': status, })


def admin_inspection_form(request):
    import datetime
    _now = datetime.datetime.now()
    _year = _now.year
    today = datetime.date.today().strftime("%d-%m-%Y")
    rly=railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    div=railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
    dept=departMast.objects.values('department_name')
    listw=m1.empmast.objects.values('empname').order_by('empname').distinct()
   
       
    context={
        't':today,
        'rly':rly,
        'div':div, 
        'dept':dept,
        'listw':listw,
        # 'listw1':listw1,
    }
    
    
    
    return render(request,"admin_inspection.html",context)



    

def admin_inspection_form(request):
    import datetime
    _now = datetime.datetime.now()
    _year = _now.year
    today = datetime.date.today().strftime("%d-%m-%Y")
    rly=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    div=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
    dept=models.departMast.objects.values('department_name')
    listw=m1.empmast.objects.values('empname').order_by('empname').distinct()
    context={
        't':today,
        'rly':rly,
        'div':div, 
        'dept':dept,
        'listw':listw,
    }
    
    
    
    return render(request,"admin_inspection.html",context)


def getDesignation(request):

    if request.method == "GET" or request.is_ajax():
        dept_1=request.GET.get('dept_1')
        print(dept_1,'_________++++++++++++________________')
          
        division=list(Level_Desig.objects.filter(department=dept_1).values('designation'))
        l=[]
        for i in division:
            l.append(i['designation'])
        print(l)    
        context={
            'division':l,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)


#amisha140622    
def compliance_marked_forward(request):
    if request.method == "GET" and request.is_ajax():
        item_no=request.GET.get('item_no')
        print(item_no,'item_no')
        inspection_no=request.GET.get('inspection_no')
        print(inspection_no,'inspection_no')

        cuser=request.user.username
        print(cuser,'cuser')
        cuser_id=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
        print(cuser_id,'cuser_id')
    
        marked_no=m1.Marked_Officers.objects.filter(marked_to_id=cuser_id,item_no_id=item_no)[0].marked_no
        print(marked_no,'marked_no')
        
        forward_to=request.GET.get('forward_to')
        print(forward_to,'forward_to')
        empno=models.Level_Desig.objects.filter(designation=forward_to)[0].empno_id
        print(empno,'empno')
        marked_to_forward=models.Level_Desig.objects.filter(designation=forward_to)[0].designation_code
        print(marked_to_forward,'marked_to_forward')

        myuser_id_forward=m1.MyUser.objects.filter(email=cuser)[0].id
        print(myuser_id_forward,'myuser_id_forward')
        mark=int(m1.Marked_Officers_forward.objects.last().marked_no_forward)+1 if m1.Marked_Officers_forward.objects.last()!=None else 1
        print(mark,'mark')

        # if m1.Marked_Officers_forward.objects.filter(marked_to_forward_id=marked_to_forward,marked_no_id=marked_no).exists():
        #     bono=[]
        #     return JsonResponse(bono, safe = False)
        
        created_on=datetime.now()
        m1.Marked_Officers_forward.objects.create(marked_no_forward=mark, marked_no_id=marked_no, marked_to_forward_id=marked_to_forward, created_on_forward=created_on, created_by_forward=cuser_id, myuser_id_id=myuser_id_forward,status_flag=1)
        print(m1.Marked_Officers_forward.objects.values())

        return JsonResponse({})


def compliance_forward(request,item_no):
    print(item_no)
    inspection_no=m1.Item_details.objects.filter(item_no=item_no)[0].inspection_no_id
    cuser=request.user
    desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    marked_forward=[] 
    if(m1.Marked_Officers.objects.filter(item_no_id=item_no,marked_to_id=desigid).exists()):
        marked_no=m1.Marked_Officers.objects.filter(item_no_id=item_no,marked_to_id=desigid)[0].marked_no   
        if(m1.Marked_Officers_forward.objects.filter(marked_no_id=marked_no).exists()):
            marked_forward=m1.Marked_Officers_forward.objects.filter(marked_no_id=marked_no).values()
    list1=[]
    for i in marked_forward:
        temp={}
        temp['recieved_on']=i['created_on_forward'].strftime("%d/%m/%y") if i['created_on_forward'] != None else '  Pending'
        empno=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].empno_id
        temp['designation']=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation
        name=[]
        empfname=m1.empmast.objects.filter(empno=empno)[0].empname
        print(empfname,'fname')
        empmname=m1.empmast.objects.filter(empno=empno)[0].empmname
        print(empmname,'mname')
        emplname=m1.empmast.objects.filter(empno=empno)[0].emplname
        print(emplname,'lname')
        if(empmname==None and emplname==None):
            name=empfname
        elif(empmname==None):
            name=empfname + " " + emplname
        elif(emplname==None):
            name=empfname + " " + empmname   
        else:
            name=empfname + " " + empmname + " " + emplname
        temp['marked_to_forward']=str(name)
        temp['reply']=i['compliance_forward'] if i['compliance_forward'] != None else 'Pending'
        temp['compliance_recieved_on_forward']=i['reply_on'].strftime("%d/%m/%y") if i['reply_on'] != None else 'Pending'
        list1.append(temp)
    designation=models.Level_Desig.objects.exclude(designation=None).values('designation')  
    return render(request,"compliance_forward.html",{'list1':list1,'item_no':item_no,'inspection_no':inspection_no,'desig':designation})


def fetch_forward_reply(request):
    print('hi')
    item_no=request.GET.get('item_no')
    inspection_no=m1.Item_details.objects.filter(item_no=item_no)[0].inspection_no_id
    cuser=request.user.username
    cuser_desig_id=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    empno=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].empno_id
    print(cuser_desig_id,empno,'cuser_id','empno')
    marked_forward=[] 
    if(m1.Marked_Officers.objects.filter(item_no_id=item_no,marked_to_id=cuser_desig_id).exists()):
        marked_no=m1.Marked_Officers.objects.filter(item_no_id=item_no,marked_to_id=cuser_desig_id)[0].marked_no 
        print(marked_no,"marked_no")
        if(m1.Marked_Officers_forward.objects.filter(marked_no_id=marked_no).exists()):
            marked_forward=m1.Marked_Officers_forward.objects.filter(marked_no_id=marked_no).values()
            print(marked_forward,"marked_forward")
    list1=[]
    item_list=[]
    item_list=item_no_details(inspection_no)
    for j in item_list:
        # print(type(item_no),j['count'],type(j['item_test']),int(item_no)==j['item_test'],'jjjjj')
        if(int(item_no)==j['item_test']):
            item=j['count']
            # print(item,'temp')
    for i in marked_forward:
        temp={}
        temp['recieved_on']=i['created_on_forward'].strftime("%d/%m/%y") if i['created_on_forward'] != None else 'NA'
        empno=models.Level_Desig.objects.filter(designation_code=i['marked_to_forward_id'])[0].empno_id
        temp['designation']=models.Level_Desig.objects.filter(designation_code=i['marked_to_forward_id'])[0].designation
        name=[]
        empfname=m1.empmast.objects.filter(empno=empno)[0].empname
        empmname=m1.empmast.objects.filter(empno=empno)[0].empmname
        emplname=m1.empmast.objects.filter(empno=empno)[0].emplname
        if(empmname==None and emplname==None):
            name=empfname
        elif(empmname==None):
            name=empfname + " " + emplname
        elif(emplname==None):
            name=empfname + " " + empmname   
        else:
            name=empfname + " " + empmname + " " + emplname
        print(name,'NAME-NAME')
        temp['marked_to_forward']=str(name)
        temp['reply']=i['compliance_forward'] if i['compliance_forward'] != None else ''
        temp['compliance_recieved_on_forward']=i['reply_on'].strftime("%d/%m/%y") if i['reply_on'] != None else 'NA'
        temp['marked_no_forward']=i['marked_no_forward']
        temp['status_flag']=i['status_flag']
        if(m1.Officers_Remark.objects.filter(marked_no_forward_id=i['marked_no_forward'])):
            temp['remark']=m1.Officers_Remark.objects.filter(marked_no_forward_id=i['marked_no_forward'])[0].remark
        list1.append(temp)
    print(list1,"list1list1")
    # pay_level=m1.empmast.objects.filter(empno=empno)[0].pc7_level
    # print(pay_level,'pay_level')
    desig_exclude=m1.Marked_Officers_forward.objects.filter(marked_no_id=marked_no,marked_no__item_no=item_no).values('marked_to_forward_id')
    # print(desig_exclude,'desigexclude')
    desig_name=list(models.Level_Desig.objects.exclude(Q(empno_id=None)|Q(designation_code=cuser_desig_id)|Q(designation_code__in=desig_exclude)).values('designation').order_by('designation'))
    # print(desig_name,'desig_name')
    return JsonResponse({'list1':list1,'item_no':item_no,'inspection_no':inspection_no,'desig':desig_name,'item':item,}, safe = False)


def item_no_details(insp_id):
    item_details1= list(m1.Item_details.objects.filter(inspection_no_id=insp_id).values())
    # print(item_details1,'item_details1')
    item_no_list=[]
    # count=1
    for j in item_details1:
        temp={}
        x=j['item_no']
        if m1.Marked_Officers.objects.filter(item_no_id=x).exists():
        # if j['type'] == 'SH':
            temp['count']=j['des_id']
            temp['item_test']=j['item_no']
            item_no_list.append(temp)
        # count=count+1
    return item_no_list


def compliance_filterdata_ajax(request):
    if request.method == "GET" and request.is_ajax():
        str=request.GET.get('str')
        if(str=='filter'):
            print('b')
            rly_id=request.GET.get('rly_id')
            print(rly_id,'1111')
            if(rly_id==""):
                list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
            else:    
                list3=models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=rly_id).values('location_code')
            list4=[]
            for i in list3:
                list4.append(i['location_code'])    
            print(list4,'2222')
            return JsonResponse({'div':list4})
    
        cuser=request.user.username
        desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    
    #data for reply modal    
        if(str=='reply'):
            status=request.GET.get('status')
            item_no=0
            inspection_id=0
            list3=[]
            list4=[]
            list6=[]
            desiglist=[]
        #gunjan
            if(request.GET.get('inspection_id')):
                inspection_id=request.GET.get('inspection_id')
                listdesig1=m1.Inspection_details.objects.filter(inspection_no=inspection_id).values('inspection_officer_id')
                listdesig=models.Level_Desig.objects.filter(designation_code__in=listdesig1).values('designation')
                listname1=m1.Inspection_details.objects.filter(inspection_no=inspection_id).values('modified_by')
                empfname=m1.empmast.objects.filter(empno__in=listname1)[0].empname
                empmname=m1.empmast.objects.filter(empno__in=listname1)[0].empmname
                emplname=m1.empmast.objects.filter(empno__in=listname1)[0].emplname
                #tarun
                m1.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id, marked_to_id=desigid).update(viewed_on=datetime.today())
                if(empmname==None and emplname==None):
                    listname=empfname
                elif(empmname==None):
                    listname=empfname + " " + emplname
                elif(emplname==None):
                    listname=empfname + " " + empmname   
                else:
                    listname=empfname + " " + empmname + " " + emplname
                print(listname,'rajputttttttttttttttttttttttt')
                list1=m1.Inspection_details.objects.filter(inspection_no=inspection_id).values()
                list5=[]
            # for pending/rejected reply and pending query
                if(status=='P'):
                    list5=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id,marked_to_id=desigid,status_flag=1).values('item_no_id')
            # for send reply
                elif(status=='S'):
                    list5=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id,marked_to_id=desigid,status_flag=2).values('item_no_id')
            # for accepted reply
                elif(status=='A'):
                    list5=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id,marked_to_id=desigid,status_flag=3).values('item_no_id')
            # for rejected reply    
                elif(status=='R'):
                    list5=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id,marked_to_id=desigid,status_flag=4).values('item_no_id')
            # for send query
                else:
                    list5=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id,marked_to_id=desigid).values('item_no_id')
                for i in list5:
                    list6.append(i['item_no_id'])
                list2=m1.Item_details.objects.filter(item_no__in=list6).values() 
                print(list2,'list2')
                for i in list1:
                    temp={}
                    temp['inspection_no']=i['inspection_no']
                    temp['inspection_note_no']=i['inspection_note_no'] if i['inspection_note_no']!=None else 'NA'
                    temp['inspection_title']=i['inspection_title']
                    temp['inspection_date']=i['inspected_on'].strftime("%d/%m/%y") if i['inspected_on']!=None else 'NA'
                    temp['empname']=listname if listname!=None else 'NA'
                    list3.append(temp)
                for i in listdesig:
                    temp={}
                    temp['designation']=i['designation'] if i['designation']!=None else 'NA'
                    desiglist.append(temp)
                
                    # list4.append(temp)
                for i in list2:
                    print(i,'iiii')
                    temp={} 
                    temp['item_no']=i['item_no']
                    temp['observation']=i['observation']
                    item_list=[]
                    item_list=item_no_details(inspection_id)
                    for j in item_list:
                        # print(j,'jjjjj')
                        if(i['item_no']==j['item_test']):
                            temp['item']=j['count']
                # for rejected reply
                    # print('REJECTED')
                    if(m1.Officers_Remark.objects.filter(marked_no__item_no=i['item_no'],marked_desig_id_id=desigid)):
                        temp['reply_received']=m1.Officers_Remark.objects.filter(marked_no__item_no=i['item_no'],marked_desig_id_id=desigid)[0].reply_received
                        temp['remark']=m1.Officers_Remark.objects.filter(marked_no__item_no=i['item_no'],marked_desig_id_id=desigid)[0].remark
                        temp['rejected_on']=m1.Officers_Remark.objects.filter(marked_no__item_no=i['item_no'],marked_desig_id_id=desigid)[0].rejected_on.strftime("%d/%m/%y")
                # for reverted inspection
                    # print('REVERTED')
                    if m1.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id,marked_to_id=desigid,status_flag=4): 
                        temp['revert']=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id,marked_to_id=desigid,status_flag=4)[0].revert
                        reverted_on=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id,marked_to_id=desigid,status_flag=4)[0].reverted_on
                        temp['reverted_on']=reverted_on.strftime("%d/%m/%y") if reverted_on!=None else 'NA'
                    temp['compliance']=m1.Marked_Officers.objects.filter(item_no=i['item_no'],marked_to_id=desigid)[0].compliance
                    reply_on=m1.Marked_Officers.objects.filter(item_no=i['item_no'],marked_to_id=desigid)[0].reply_on
                    temp['reply_on']=reply_on.strftime("%d/%m/%y") if reply_on!=None else 'NA'
                    list4.append(temp)  
                print(list3,'__________________________list3')
                print(list4,'__________________________________list4')
                print(desiglist,'__________________________________________desiglist') 
        # for item-wise revert option
            elif(request.GET.get('item_no')):
                item_no=request.GET.get('item_no')
                temp={}
                temp['item_no']=item_no
                temp['observation']=m1.Item_details.objects.filter(item_no=item_no)[0].observation
                # if m1.Marked_Officers.objects.filter(item_no=item_no,marked_to_id=desigid,status_flag=4): 
                #     temp['revert-modal']=m1.Marked_Officers.objects.filter(item_no=item_no,marked_to_id=desigid,status_flag=4)[0].revert
                #     reverted_on=m1.Marked_Officers.objects.filter(item_no=item_no,marked_to_id=desigid,status_flag=4)[0].reverted_on
                #     temp['reverted-on-modal']=reverted_on.strftime("%d/%m/%y") if reverted_on!=None else 'NA'
                list4.append(temp)  
            return JsonResponse({'idetails':list3,'itemdetails':list4,'desigdetails':desiglist,})
        
        item_no=request.GET.get('item_no')
        print(item_no,'item_no')
        compliance=request.GET.get('compliance')
        print(compliance,'compliance')
        remarks=request.GET.get('remarks')
        print(remarks,'remarks')
    
    #for saving merged forwarded reply
        if(str=='save'):
            if(len(compliance)!=0):
                # reply_on=datetime.now()
                m1.Marked_Officers.objects.filter(item_no_id=item_no,marked_to_id=desigid).update(compliance=compliance,status_flag=1)
                inspection_no=m1.Item_details.objects.filter(item_no=item_no)[0].inspection_no_id
            else:
                bono=[]
                return JsonResponse(bono,safe=False)
            return JsonResponse({'insp_no':inspection_no})
    #for saving revert reason    
        elif(str=='revert'):
            if(len(remarks)!=0):
                # reply_on=datetime.now()
                m1.Marked_Officers.objects.filter(item_no_id=item_no,marked_to_id=desigid).update(revert=remarks,status_flag=4,reverted_on=datetime.now())
                inspection_no=m1.Item_details.objects.filter(item_no=item_no)[0].inspection_no_id
            else:
                bono=[]
                return JsonResponse(bono,safe=False)
            return JsonResponse({'insp_no':inspection_no})


# GUNJAN
def save_data(request):
    if request.method == 'GET':
        str=request.GET.get('str')
    #for reply
        if str=="submit":
            ins_id=request.GET.get('ins_id')
            cuser=request.user.username
            desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
            item_no=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=ins_id,marked_to_id=desigid).values('item_no')
            compliance=m1.Marked_Officers.objects.filter(item_no_id__in=item_no,marked_to_id=desigid,status_flag=1).values('compliance','item_no')
            count=len(compliance)
            count_test=0
            for i in compliance:
                if(i['compliance']==None):
                    count_test=count_test+1
                    print(count_test)
                    if(count==count_test):
                        bono=[]
                        return JsonResponse(bono, safe = False)
            # for i in compliance:
                else:
                    reply_on=datetime.now()
                    m1.Marked_Officers.objects.filter(item_no_id=i['item_no'],marked_to_id=desigid).update(status_flag=2,reply_on=reply_on,status=None)
                    if m1.Marked_Officers.objects.exclude(status_flag=4).filter(item_no_id__in=item_no)[0].status_flag==2:
                        m1.Item_details.objects.filter(item_no__in=item_no,type='SH').update(status_flag=3)
                    elif m1.Marked_Officers.objects.exclude(status_flag=4).filter(item_no_id__in=item_no)[0].status_flag!=2:
                        m1.Item_details.objects.filter(item_no__in=item_no,type='SH').update(status_flag=2)
                
    #for query
        if str=="submit-forward":
            ins_id=request.GET.get('ins_id')
            cuser=request.user.username
            desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
            item_no=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=ins_id,status_flag=1).values('item_no')
            compliance_forward=m1.Marked_Officers_forward.objects.filter(marked_no__item_no_id__in=item_no,marked_to_forward_id=desigid).values('compliance_forward','marked_no_forward')
            count=len(compliance_forward)
            count_test=0
            for i in compliance_forward:
                if(i['compliance_forward']==None):
                    count_test=count_test+1
                    print(count_test)
                    if(count==count_test):
                        bono=[]
                        return JsonResponse(bono, safe = False)
                else:
                    reply_on=datetime.now()
                    m1.Marked_Officers_forward.objects.filter(marked_no_forward=i['marked_no_forward'],marked_to_forward_id=desigid).update(status_flag=2,reply_on=reply_on)
    return JsonResponse({}, safe = False) 


def compliance_filterdata(request):
    print('a')
    if request.method == "GET" and request.is_ajax():
        print('b')
        div_id=request.GET.get('div_id')
        print(div_id,'div_id')
        rly_id=request.GET.get('rly_id')
        print(rly_id,'rly_id')
        dept_id=request.GET.get('dept_id')
        print(dept_id,'dept_id')
        startDate=request.GET.get('startDate')
        startDate = datetime.strptime(startDate,'%Y-%m-%d')
        print(startDate,'startDate')
        endDate=request.GET.get('endDate')
        endDate = datetime.strptime(endDate,'%Y-%m-%d')
        print(endDate,'endDate')
        str=request.GET.get('str')
        list=[]
        count=1
    #GUNJAN
        # inspect_details=models.Inspection_details.objects.filter(zone=rly_id,division=div_id,dept=dept_id,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
        if rly_id=="" and div_id=="" and dept_id=="":
            print('00')
            inspect_details=m1.Inspection_details.objects.filter(status_flag=1,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
        elif div_id=="" and dept_id=="":
            print(div_id,dept_id, '11')
            insp_details=m1.Insp_multi_location.objects.filter(type='HQ',item=rly_id).values('inspection_no_id')
            inspect_details=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=insp_details,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
            # inspect_details=m1.Inspection_details.objects.filter(status_flag=1,zone=rly_id,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
        elif rly_id=="":
            print(rly_id, '22')
            insp_details=m1.Insp_multi_location.objects.filter(Q(type='DPT',item=dept_id)).values('inspection_no_id')
            inspect_details=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=insp_details,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
            # inspect_details=m1.Inspection_details.objects.filter(status_flag=1,dept=dept_id,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
        elif div_id=="":
            print(div_id, '33')
            insp_details=m1.Insp_multi_location.objects.filter(Q(type='HQ',item=rly_id)&Q(type='DPT',item=dept_id)).values('inspection_no_id')
            inspect_details=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=insp_details,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
            # inspect_details=m1.Inspection_details.objects.filter(status_flag=1,zone=rly_id,dept=dept_id,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
        elif dept_id=="":
            print(dept_id, '44')
            insp_details=m1.Insp_multi_location.objects.filter(Q(type='HQ',item=rly_id)&Q(type='DIV',item=div_id)).values('inspection_no_id')
            inspect_details=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=insp_details,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
            # inspect_details=m1.Inspection_details.objects.filter(status_flag=1,zone=rly_id,division=div_id,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
        else:
            print(rly_id,div_id,dept_id, '55')
            insp_details=m1.Insp_multi_location.objects.filter(Q(type='HQ',item=rly_id)&Q(type='DIV',item=div_id)&Q(type='DPT',item=dept_id)).values('inspection_no_id')
            inspect_details=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=insp_details,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
            # inspect_details=m1.Inspection_details.objects.filter(status_flag=1,zone=rly_id,division=div_id,dept=dept_id,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
        print(inspect_details,'01234')
        cuser=request.user.username
        desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    # data of pending reply view
        if(str=='pending'):
            for i in inspect_details:
                if m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],marked_to_id=desigid,status_flag=1):
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
                    temp['viewed_on']=i['modified_on'].strftime("%d/%m/%y") if i['modified_on']!=None else 'Pending'
                    temp['file_path']=i['report_path']
                    list.append(temp)
                    count=count+1
            print(list,'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    # data of sended reply view
        if(str=='send'):
            for i in inspect_details:
                if m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],marked_to_id=desigid,status_flag=2):
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
                    temp['viewed_on']=i['modified_on'].strftime("%d/%m/%y") if i['modified_on']!=None else 'Pending'
                    temp['file_path']=i['report_path']
                    list.append(temp)
                    count=count+1
            print(list,'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    # data of accepted reply view
        elif(str=='accept'):
            for i in inspect_details:
                if m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],marked_to_id=desigid,status_flag=3):
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
                    temp['viewed_on']=i['modified_on'].strftime("%d/%m/%y") if i['modified_on']!=None else 'Pending'
                    temp['file_path']=i['report_path']
                    list.append(temp)
                    count=count+1
            print(list,'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    # data of rejected reply view
        elif(str=='reject'):
            for i in inspect_details:
                item=m1.Item_details.objects.filter(inspection_no_id=i['inspection_no']).values('item_no')
                marked=m1.Marked_Officers.objects.filter(item_no_id__in=item,marked_to_id=desigid).values('marked_no')
                print(marked,'rejectreject')
                if(len(marked)!=0):
                    if m1.Officers_Remark.objects.filter(marked_no_id__in=marked,marked_desig_id_id=desigid):
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
                        temp['inspected_on']=i['inspected_on'].strftime("%d/%m/%y") if i['inspected_on']!=None else 'Pending'
                        temp['file_path']=i['report_path']
                        list.append(temp)
                        count=count+1
                print(list,'-------------------------')
    # data of rejected reply view
        elif(str=='revert'):
            for i in inspect_details:
                if m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],marked_to_id=desigid,status_flag=4):
                    print(count,'countcount')
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
                    t1=m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],marked_to_id=desigid,status_flag=4).values('reverted_on')
                    temp['reverted_on']=t1[0]['reverted_on'].strftime("%d/%m/%y") if t1[0]['reverted_on']!=None else 'NA'
                    temp['file_path']=i['report_path']
                    list.append(temp)
                    count=count+1
            print(list,'-------------------------')            
    # data of pending query view
        elif(str=='pending-forward'):
            for i in inspect_details:      
                marked_no=m1.Marked_Officers_forward.objects.filter(marked_to_forward_id=desigid).values('marked_no_id')
                print(marked_no,'marked_no')
                if m1.Marked_Officers.objects.filter(item_no__inspection_no_id=i['inspection_no'],marked_no__in=marked_no,status_flag=1):
                    item_no=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=i['inspection_no'],marked_no__in=marked_no)[0].item_no_id
                    print('abcabcabc')
                    if m1.Marked_Officers_forward.objects.filter(marked_no__item_no=item_no,status_flag=1,marked_to_forward_id=desigid):  
                        print('ENTERED')
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
                        list.append(temp)
                        count=count+1
                print(list,'LIST-------------------------LIST')
     # data of sent query view
        elif(str=='sent-forward'):
            for i in inspect_details:      
                marked_no=m1.Marked_Officers_forward.objects.filter(marked_to_forward_id=desigid).values('marked_no_id')
                print(marked_no,'marked_no')
                if m1.Marked_Officers.objects.filter(item_no__inspection_no_id=i['inspection_no'],marked_no__in=marked_no,status_flag=1):
                    item_no=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=i['inspection_no'],marked_no__in=marked_no)[0].item_no_id
                    print('abcabcabc')
                    if m1.Marked_Officers_forward.objects.filter(marked_no__item_no=item_no,status_flag=1,marked_to_forward_id=desigid):  
                        print('ENTERED')
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
                        list.append(temp)
                        count=count+1
                print(list,'LIST-------------------------LIST')
        # END GUNJAN
        return JsonResponse({'inspect_details':list,})
 
 
def compliance_alterdata(request):
    if request.method == "GET" and request.is_ajax():
        list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').order_by('location_code')
        list2=[]
        for i in list1:
            list2.append(i['location_code'])    
        # print(list2,'zones')
        list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').order_by('location_code')
        list4=[]
        for i in list3:
            list4.append(i['location_code'])    
        # print(list4,'divisions')
        list5=models.departMast.objects.all().values('department_name')
        list6=[]
        for i in list5:
            # print(i['department_name'],'department')
            list6.append(i['department_name'])  
    return JsonResponse({'change_rly':list2,'change_div':list4,'change_dept':list6})


def compliance_form(request):
    print('compliance-form')
    listgrid=[]
    count=1
    inspect_details1=m1.Inspection_details.objects.filter(status_flag=1).values().order_by('-inspection_no')
    print(inspect_details1,'01234')
    cuser=request.user.username
    desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    print(cuser,desigid,'CUSER, DESIGID')
    for i in inspect_details1:
        if m1.Marked_Officers.objects.filter(item_no__inspection_no_id=i['inspection_no'],status_flag=1,marked_to_id=desigid):        
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
            t1=m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],marked_to_id=desigid,status_flag=1).values('viewed_on')
            temp['viewed_on']=t1[0]['viewed_on'].strftime("%d/%m/%y") if t1[0]['viewed_on']!=None else 'Pending'
            temp['file_path']=i['report_path']
            listgrid.append(temp)
            count=count+1
    print(listgrid,'-------------------------,pending')
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').order_by('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').order_by('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name').order_by('department_name')
    list6=[]
    for i in list5:
        # print(i['department_name'],'_________')
        list6.append(i['department_name']) 
    designation=models.Level_Desig.objects.exclude(Q(empno_id=None)).values('designation').order_by('designation')
    context={
        'zone':list2 ,
        'division':list4,
        'dept':list6,
        'listgrid':listgrid,
        'desig':designation,
    }
    print(list2,'_____________')
    return render(request,'compliance_form.html',context)


def compliance_form_send(request):
    print('compliance-form-send')
    listgrid=[]
    count=1
    inspect_details1=m1.Inspection_details.objects.filter(status_flag=1).values().order_by('-inspection_no')
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
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').order_by('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').order_by('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name').order_by('department_name')
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
    return render(request,'compliance_form_send.html',context)


def compliance_form_accept(request):
    print('compliance-form-accept')
    listgrid=[]
    count=1
    inspect_details1=m1.Inspection_details.objects.filter(status_flag=1).values().order_by('-inspection_no')
    print(inspect_details1,'01234')
    cuser=request.user.username
    desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    print(cuser,desigid,'CUSER, DESIGID')
    for i in inspect_details1:
        if m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],marked_to_id=desigid,status_flag=3):        
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
            # t1=m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],marked_to_id=desigid,status_flag=1).values('viewed_on')
            # temp['viewed_on']=t1[0]['viewed_on'].strftime("%d/%m/%y") if t1[0]['viewed_on']!=None else 'Pending'
            temp['file_path']=i['report_path']
            listgrid.append(temp)
            count=count+1
    print(listgrid,'-------------------------,accept')
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').order_by('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').order_by('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name').order_by('department_name')
    list6=[]
    for i in list5:
        # print(i['department_name'],'_________')
        list6.append(i['department_name'])        
    context={
        'zone':list2 ,
        'division':list4,
        'dept':list6,
        'listgrid':listgrid,
    }
    print(list2,'_____________')
    return render(request,'compliance_form_accept.html',context)


def compliance_form_reject(request):
    print('compliance-form-reject')
    listgrid=[]
    count=1
    inspect_details1=m1.Inspection_details.objects.filter(status_flag=1).values().order_by('-inspection_no')
    print(inspect_details1,'0123401234')
    cuser=request.user.username
    desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    print(cuser,desigid,'CUSER, DESIGID')
    for i in inspect_details1:
        item=m1.Item_details.objects.filter(inspection_no_id=i['inspection_no']).values('item_no')
        marked=m1.Marked_Officers.objects.filter(item_no_id__in=item,marked_to_id=desigid,status='R').values('marked_no')
        print(marked,'rejectreject')
        if(len(marked)!=0):
            # if m1.Officers_Remark.objects.filter(marked_no_id__in=marked,marked_to_reject_id=desigid):
            if m1.Officers_Remark.objects.filter(marked_no_id__in=marked):
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
                # t1=m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],marked_to_id=desigid,status_flag=1).values('viewed_on')
                # temp['viewed_on']=t1[0]['viewed_on'].strftime("%d/%m/%y") if t1[0]['viewed_on']!=None else 'Pending'
                temp['file_path']=i['report_path']
                listgrid.append(temp)
            count=count+1
    print(listgrid,'-------------------------,reject')
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').order_by('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').order_by('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name').order_by('department_name')
    list6=[]
    for i in list5:
        # print(i['department_name'],'_________')
        list6.append(i['department_name'])        
    context={
        'zone':list2 ,
        'division':list4,
        'dept':list6,
        'listgrid':listgrid,
    }
    print(list2,'_____________')
    return render(request,'compliance_form_reject.html',context)    


def compliance_form_revert(request):
    print('compliance-form-revert')
    listgrid=[]
    count=1
    inspect_details1=m1.Inspection_details.objects.filter(status_flag=1).values().order_by('-inspection_no')
    print(inspect_details1,'0123401234')
    cuser=request.user.username
    desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    print(cuser,desigid,'CUSER, DESIGID')
    for i in inspect_details1:
        if m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],marked_to_id=desigid,status_flag=4): 
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
            t1=m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],marked_to_id=desigid,status_flag=4).values('reverted_on')
            temp['reverted_on']=t1[0]['reverted_on'].strftime("%d/%m/%y") 
            temp['file_path']=i['report_path']
            listgrid.append(temp)
        count=count+1
    print(listgrid,'-------------------------,revert')
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').order_by('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').order_by('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name').order_by('department_name')
    list6=[]
    for i in list5:
        # print(i['department_name'],'_________')
        list6.append(i['department_name'])        
    context={
        'zone':list2 ,
        'division':list4,
        'dept':list6,
        'listgrid':listgrid,
    }
    print(list2,'_____________')
    return render(request,'compliance_form_revert.html',context)        


def compliance_query(request):
    print('compliance-query')
    listgrid=[]
    count=1
    inspect_details1=m1.Inspection_details.objects.filter(status_flag=1).values().order_by('-inspection_no')
    print(inspect_details1,'01234')
    cuser=request.user.username
    desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    print(cuser,desigid,'CUSER, DESIGID')
    for i in inspect_details1:
        # if m1.Marked_Officers.objects.filter(item_no_id__inspection_no=i['inspection_no'],status_flag=1):
            marked_no=m1.Marked_Officers_forward.objects.filter(marked_to_forward_id=desigid).values('marked_no_id')
            print(marked_no,'marked_no')
            if m1.Marked_Officers.objects.filter(item_no__inspection_no_id=i['inspection_no'],marked_no__in=marked_no,status_flag=1):
                item_no=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=i['inspection_no'],marked_no__in=marked_no)[0].item_no_id
                print('abcabcabc')
                if m1.Marked_Officers_forward.objects.filter(marked_no__item_no=item_no,status_flag=1,marked_to_forward_id=desigid) or m1.Marked_Officers_forward.objects.filter(marked_no__item_no=item_no,status_flag=3,marked_to_forward_id=desigid):  
                    print('ENTERED')
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
                    temp['item_no']=item_no
                    listgrid.append(temp)
                    count=count+1
    print(listgrid,'-------------------------,pending')
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').order_by('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').order_by('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name').order_by('department_name')
    list6=[]
    for i in list5:
        # print(i['department_name'],'_________')
        list6.append(i['department_name'])       
    context={
        'zone':list2 ,
        'division':list4,
        'dept':list6,
        'listgrid':listgrid,
    }
    print(list2,'_____________')
    return render(request,'compliance_query.html',context)


def compliance_query_send(request):
    print('compliance-query-send')
    listgrid=[]
    count=1
    inspect_details1=m1.Inspection_details.objects.filter(status_flag=1).values().order_by('-inspection_no')
    print(inspect_details1,'01234')
    cuser=request.user.username
    desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    print(cuser,desigid,'CUSER, DESIGID')
    marked_no=m1.Marked_Officers_forward.objects.exclude(status_flag=1).filter(marked_to_forward_id=desigid).values('marked_no_id')
    print(marked_no,'marked_no')
    for i in inspect_details1:
        if m1.Marked_Officers.objects.filter(item_no__inspection_no_id=i['inspection_no'],marked_no__in=marked_no):
            item_no=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=i['inspection_no'],marked_no__in=marked_no).values('item_no_id')
            print(item_no,'item_no')
            for x in item_no:
                # print(x['item_no_id'])
                if m1.Marked_Officers_forward.objects.filter(marked_no__item_no_id=x['item_no_id'],marked_to_forward_id=desigid,status_flag=2):  
                    print('ENTERED2')
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
                    temp['item_no']=item_no
                    listgrid.append(temp)
                    count=count+1
    print(listgrid,'-------------------------,pending')
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').order_by('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').order_by('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name').order_by('department_name')
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
    return render(request,'compliance_query_send.html',context)


def compliance_filterdata_ajax1(request):
    if request.method == "GET" and request.is_ajax():
        str=request.GET.get('str')
        
        if(str=='filter'):
            print('b')
            rly_id=request.GET.get('rly_id')
            print(rly_id,'1111')
            if(rly_id==""):
                list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').order_by('location_code')
            else:    
                list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').order_by('location_code')
            list4=[]
            for i in list3:
                list4.append(i['location_code'])    
            print(list4,'2222')
            return JsonResponse({'div':list4})
        
        cuser=request.user.username
        desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
        print(cuser,desigid,'CUSER, DESIGID')
        
        if(str=='reply'):
            status=request.GET.get('status')
            inspection_id=request.GET.get('inspection_id')
            listdesig1=m1.Inspection_details.objects.filter(inspection_no=inspection_id).values('inspection_officer_id')
            listdesig=models.Level_Desig.objects.filter(designation_code__in=listdesig1).values('designation')
            listname1=m1.Inspection_details.objects.filter(inspection_no=inspection_id).values('modified_by')
            empfname=m1.empmast.objects.filter(empno__in=listname1)[0].empname
            empmname=m1.empmast.objects.filter(empno__in=listname1)[0].empmname
            emplname=m1.empmast.objects.filter(empno__in=listname1)[0].emplname
            if(empmname==None and emplname==None):
                listname=empfname
            elif(empmname==None):
                listname=empfname + " " + emplname
            elif(emplname==None):
                listname=empfname + " " + empmname   
            else:
                listname=empfname + " " + empmname + " " + emplname
            print(listname,'rajputttttttttttttttttttttttt')
            list1=m1.Inspection_details.objects.filter(inspection_no=inspection_id).values()
            listf=m1.Marked_Officers_forward.objects.filter(marked_to_forward_id=desigid).values('marked_no_id')
            print(listf,'listf')
            list5=[]
            list3=[]
            list4=[]
            listremark=[]
            listdate=[]
            desiglist=[]
        
        # pending query
            if (status=='P'):
                print('PENDING LIST')
                list5=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id,marked_no__in=listf,status_flag=1).values('item_no_id')
                print(list5,'PLIST5')
                list6=[]
                for i in list5:
                    list6.append(i['item_no_id'])
                list2=m1.Item_details.objects.filter(item_no__in=list6).values() 
                for i in list2:
                    temp={}
                    temp['item_no']=i['item_no']  
                    temp['observation']=i['observation']
                    item_list=[]
                    item_list=item_no_details(inspection_id)
                    for j in item_list:
                        print(j,'jjjjj')
                        temp['item']=j['count']
                    if(m1.Marked_Officers_forward.objects.exclude(status_flag=2).filter(marked_no__item_no=i['item_no'],marked_to_forward_id=desigid)):
                        print('inside if condition')
                        temp['compliance_forward']=m1.Marked_Officers_forward.objects.exclude(status_flag=2).filter(marked_no__item_no=i['item_no'],marked_to_forward_id=desigid)[0].compliance_forward
                        print(temp['compliance_forward'],'HAHAHAHAHAHAHAHAHAHAHA')
                        temp['reply_on_forward']=m1.Marked_Officers_forward.objects.exclude(status_flag=2).filter(marked_no__item_no=i['item_no'],marked_to_forward_id=desigid)[0].reply_on
                        created_on_forward=m1.Marked_Officers_forward.objects.exclude(status_flag=2).filter(marked_no__item_no=i['item_no'],marked_to_forward_id=desigid)[0].created_on_forward 
                        temp['created_on_forward']=created_on_forward.strftime("%d/%m/%y")
                        id_reject=m1.Marked_Officers_forward.objects.exclude(status_flag=2).filter(marked_no__item_no=i['item_no'],marked_to_forward_id=desigid)[0].marked_no_forward
                        if m1.Officers_Remark.objects.filter(marked_no_forward_id=id_reject):
                            remarkk=m1.Officers_Remark.objects.filter(marked_no_forward_id=id_reject,status_flag=0)[0].remark
                            datee=m1.Officers_Remark.objects.filter(marked_no_forward_id=id_reject,status_flag=0)[0].rejected_on.strftime("%d/%m/%y")
                            temp['remark']=remarkk if remarkk!=None else 'NA'
                            temp['rejected_on']=datee 
                        else:
                            temp['remark']='NA'
                            temp['rejected_on']='NA' 
                    list4.append(temp) 
            
        # sent query    
            elif (status=='S'):
                print('SENT LIST')
                list5=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id,marked_no__in=listf).values('item_no_id') 
                print(list5,'SLIST5')
                list6=[]
                for i in list5:
                    list6.append(i['item_no_id'])
                list2=m1.Item_details.objects.filter(item_no__in=list6).values() 
                for i in list2:
                    temp={}
                    temp['item_no']=i['item_no']  
                    temp['observation']=i['observation']
                    item_list=[]
                    item_list=item_no_details(inspection_id)
                    for j in item_list:
                        print(j,'jjjjj')
                        temp['item']=j['count']
                    if(m1.Marked_Officers_forward.objects.filter(marked_no__item_no=i['item_no'],marked_to_forward_id=desigid,status_flag=2)):
                        temp['compliance_forward']=m1.Marked_Officers_forward.objects.filter(marked_no__item_no=i['item_no'],marked_to_forward_id=desigid,status_flag=2)[0].compliance_forward
                        print(temp['compliance_forward'],'HAHAHAHAHAHAHAHAHAHAHA')
                        temp['reply_on_forward']=m1.Marked_Officers_forward.objects.filter(marked_no__item_no=i['item_no'],marked_to_forward_id=desigid,status_flag=2)[0].reply_on.strftime("%d/%m/%y")
                        temp['created_on_forward']=m1.Marked_Officers_forward.objects.filter(marked_no__item_no=i['item_no'],marked_to_forward_id=desigid,status_flag=2)[0].created_on_forward              
                    list4.append(temp)   
            
            for i in list1:
                temp={}
                temp['inspection_no']=i['inspection_no']
                temp['inspection_note_no']=i['inspection_note_no'] if i['inspection_note_no']!=None else 'NA'
                temp['inspection_title']=i['inspection_title']
                temp['inspection_date']=i['inspected_on'].strftime("%d/%m/%y") if i['inspected_on']!=None else 'NA'
                temp['empname']=listname if listname!=None else 'NA'
                list3.append(temp)
            for i in listdesig:
                temp={}
                temp['designation']=i['designation'] if i['designation']!=None else 'NA'
                desiglist.append(temp) 
            print(list3,'__________________________list3list3')
            print(list4,'__________________________________list4list4')
            print(desiglist,'__________________________________________desiglistdesiglist') 
            return JsonResponse({'idetails':list3,'itemdetails':list4,'desigdetails':desiglist,})
        
        item_no=request.GET.get('item_no')
        compliance_forward=request.GET.get('compliance_forward')
   
    # save as draft for forwarded reply
        if(str=='save-forward'):
            if(len(compliance_forward)!=0):
                m1.Marked_Officers_forward.objects.filter(marked_no_id__item_no_id=item_no,marked_to_forward_id=desigid).update(compliance_forward=compliance_forward,status_flag=1)
                return JsonResponse({})
            else:
                bono=[]
                return JsonResponse(bono,safe=False)


def viewdate_ajax(request):
    if request.method == "GET" and request.is_ajax():
        ins_id=request.GET.get('inspection_id')
        cuser=request.user.username
        desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
        print(cuser,desigid,'CUSER, DESIGID')
        item_no=m1.Item_details.objects.filter(inspection_no_id=ins_id).values('item_no')
        print(item_no,'viewed_on')
        if m1.Marked_Officers.objects.filter(item_no_id__in=item_no, marked_to_id=desigid, viewed_on=None):
            m1.Marked_Officers.objects.filter(item_no_id__in=item_no, marked_to_id=desigid, viewed_on=None).update(viewed_on=datetime.now())
        return JsonResponse({}, safe = False) 


def pending_byme(request):
    print('pending_byme')
    listgrid=[]
    count=1
    cuser=request.user.username
    desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    # print(cuser,desigid,'CUSER, DESIGID')
    item_details=m1.Item_details.objects.filter(inspection_no__inspection_officer=desigid).values().order_by('-inspection_no__inspected_on')
    # print(item_details,'01234')
    for i in item_details:
        # i['type'] == 'SH' and 
        if m1.Marked_Officers.objects.filter(item_no_id=i['item_no'], status_flag=1):
            # print('ENTERED')
            temp={}
            temp['sr_no']=count
            temp['inspection_no']=i['inspection_no_id']
            note_no=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'],inspection_officer=desigid)[0].inspection_note_no
            temp['inspection_note_no']=note_no
            temp['item_no']=i['item_no']
            temp['observation']=i['observation']
            inspected_on=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'],inspection_officer=desigid)[0].inspected_on
            temp['inspected_on']=inspected_on.strftime("%d/%m/%y") if inspected_on!=None else 'NA'
            mark=m1.Marked_Officers.objects.filter(item_no=i['item_no'], status_flag=1).values()
            desig_longdesc1=""
            marked_officers1 = ""
            for x in mark:
                marked=models.Level_Desig.objects.filter(designation_code=x['marked_to_id'])
                # print('yyyyyyyy', marked[0].designation)
                if  marked[0].designation:
                    desig_longdesc1 += marked[0].designation+', ' 
            # desig_long = desig_longdesc1.rstrip(' ,') 
            # print('========', desig_long, '========')
            # temp['marked_officers']=desig_long
                marked_officers1 += marked[0].empno_id+', '
            if marked_officers1 != '':
                testdesig=desig_longdesc1.split(',')
                # print(testdesig,'ASDFGHJKL',testdesig.pop(),'ASDFGHJKL')
                testdesig.pop()
                testmarkofficer=''
                alldesig = models.Level_Desig.objects.filter(designation__in=testdesig).values('d_level').distinct('d_level')
                # print(alldesig,'alldesig')
                for i in alldesig:
                    # for GMs
                    if i['d_level'] == 'GM':
                        print('GM-GM')
                        lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(designation_code=desigid).count()
                        print(lst1,'lst1lst1')
                        if lst1 != 0:
                            print('GM-GM-1')
                            lst2=list(models.Level_Desig.objects.filter(designation__in=testdesig).exclude(d_level=i['d_level']).values('designation').order_by('designation'))
                            if testmarkofficer != '':
                                print('GM-GM-2')
                                testmarkofficer+=','
                            testmarkofficer=testmarkofficer+"All GM's/ZR"
                            testdesig=list(map(lambda d: d['designation'], lst2))
                            print(testdesig,'testest1')
                            temp['marked_officers']="All GM's/ZR"
                            print(temp['marked_officers'])
                    # for BMs
                    elif i['d_level'] == 'BM':
                        print('BM-BM')
                        lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(designation_code=desigid).count()
                        print(lst1,'lst1lst1')
                        if lst1 != 0:
                            lst2=list(models.Level_Desig.objects.filter(designation__in=testdesig).exclude(d_level=i['d_level']).values('designation').order_by('designation'))
                            if testmarkofficer != '':
                                testmarkofficer+=','
                            testmarkofficer=testmarkofficer+"All Board Member's"
                            testdesig=list(map(lambda d: d['designation'], lst2))
                            temp['marked_officers']="All Board Member's"
                            print(temp['marked_officers'])
                    # for PHODs
                    elif i['d_level'] == 'PHOD':
                        print('PHOD-PHOD')
                        lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(designation_code=desigid).count()
                        if lst1 == 0:
                            lst2=list(models.Level_Desig.objects.filter(designation__in=testdesig).exclude(d_level=i['d_level']).values('designation').order_by('designation'))
                            if testmarkofficer != '':
                                testmarkofficer+=','
                            testmarkofficer=testmarkofficer+"All PHOD's"
                            testdesig=list(map(lambda d: d['designation'], lst2))
                            temp['marked_officers']="All PHOD's"
                            print(temp['marked_officers'])
                        else:
                            hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
                            for ii in hq:
                                rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
                                if models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exists():
                                    lst3=models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exclude(designation_code=desigid).count()
                                    if lst3 == 0:
                                        lst2=list(models.Level_Desig.objects.filter(designation__in=testdesig).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('designation').order_by('designation'))
                                        if testmarkofficer != '':
                                            testmarkofficer+=','
                                        testmarkofficer=testmarkofficer+"All PHOD's"+ii['parent_location_code']
                                        testdesig=list(map(lambda d: d['designation'], lst2))
                                        temp['marked_officers']=temp['marked_officers']+"All PHOD's/"+ii['parent_location_code']
                                        print(temp['marked_officers'])
                    # for DRMs
                    elif i['d_level'] == 'DRM':
                        print('DRM-DRM')
                        lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(designation_code=desigid).count()
                        print(lst1,'lst1lst1')
                        if lst1 == 0:
                            lst2=list(models.Level_Desig.objects.filter(designation__in=testdesig).exclude(d_level=i['d_level']).values('designation').order_by('designation'))
                            if testmarkofficer != '':
                                testmarkofficer+=','
                            testmarkofficer=testmarkofficer+"All DRM's"
                            testdesig=list(map(lambda d: d['designation'], lst2))
                            temp['marked_officers']="All DRM's"
                            print(temp['marked_officers'])
                        else:
                            print('DRM-DRM-DRM')
                            hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
                            for ii in hq:
                                rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
                                if models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exists():
                                    lst3=models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exclude(designation_code=desigid).count()
                                    if lst3 == 0:
                                        lst2=list(models.Level_Desig.objects.filter(designation__in=testdesig).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('designation').order_by('designation'))
                                        if testmarkofficer != '':
                                            testmarkofficer+=','
                                        testmarkofficer=testmarkofficer+"All DRM's/"+ii['parent_location_code']
                                        print(testmarkofficer,'testmarkofficer')
                                        testdesig=list(map(lambda d: d['designation'], lst2))
                                        print(testdesig,'testdesig')
                                        temp['marked_officers']=temp['marked_officers']+"All DRM's/"+ii['parent_location_code']
                                        print(temp['marked_officers'])
                for i in range(len(testdesig)):
                    if testmarkofficer != '':
                        testmarkofficer+=','
                    testmarkofficer=testmarkofficer+testdesig[i]
                temp['marked_officers']=testmarkofficer
                print(temp['marked_officers'],'testest1')
            listgrid.append(temp)
            count=count+1
    print(listgrid,'-------------------------,pending')
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').order_by('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').order_by('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name').order_by('department_name')
    list6=[]
    for i in list5:
        # print(i['department_name'],'_________')
        list6.append(i['department_name'])       
    context={
        'zone':list2 ,
        'division':list4,
        'dept':list6,
        'listgrid':listgrid,
    }
    print(list2,'_____________')
    return render(request,'pending_byme.html',context)


def pending_forme(request):
    print('pending_forme')
    listgrid=[]
    count=1
    cuser=request.user.username
    desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    print(cuser,desigid,'CUSER, DESIGID')
    item_details=m1.Item_details.objects.values().order_by('-inspection_no__inspected_on')
    print(item_details,'01234')
    for i in item_details:
        # i['type'] == 'SH' and 
        if m1.Marked_Officers.objects.filter(item_no_id=i['item_no'], marked_to_id=desigid, status_flag=1):
            temp={}
            temp['sr_no']=count
            temp['inspection_no']=i['inspection_no_id']
            note_no=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'])[0].inspection_note_no
            temp['inspection_note_no']=note_no
            temp['item_no']=i['item_no']
            temp['observation']=i['observation']
            inspected_on=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'])[0].inspected_on
            temp['inspected_on']=inspected_on.strftime("%d/%m/%y") if inspected_on!=None else 'NA'
            inspect_officer=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'])[0].inspection_officer_id
            inspecting_officer=models.Level_Desig.objects.filter(designation_code=inspect_officer)[0].designation
            temp['inspecting_officer']=inspecting_officer if inspecting_officer!=None else 'NA'
            listgrid.append(temp)
            count=count+1
    print(listgrid,'-------------------------,pending')
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').order_by('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').order_by('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name').order_by('department_name')
    list6=[]
    for i in list5:
        # print(i['department_name'],'_________')
        list6.append(i['department_name'])       
    context={
        'zone':list2 ,
        'division':list4,
        'dept':list6,
        'listgrid':listgrid,
    }
    print(list2,'_____________')
    return render(request,'pending_forme.html',context)


def pending_item_filterdata(request):
    print('a')
    if request.method == "GET" and request.is_ajax():
        print('b')
        rly_id=request.GET.get('rly_id')
        div_id=request.GET.get('div_id')
        dept_id=request.GET.get('dept_id')
        # location=request.GET.get('location')
        str=request.GET.get('str')
        print(str,'WORK TO DO')
        cuser=request.user.username
        desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
        print(cuser,desigid,'CUSER, DESIGID')
        list=[]
        count=1
    # for inspection done by me
        if(str=='by_me'):
            if rly_id=="" and div_id=="" and dept_id=="":
                print('00')
                item_details=m1.Item_details.objects.filter(inspection_no__inspection_officer=desigid).values().order_by('-inspection_no__inspected_on')
            elif div_id=="" and dept_id=="":
                print(div_id,dept_id, '11')
                item_details=m1.Item_details.objects.filter(inspection_no__inspection_officer=desigid,inspection_no__zone=rly_id).values().order_by('-inspection_no__inspected_on')
            elif rly_id=="":
                print(rly_id, '22')
                item_details=m1.Item_details.objects.filter(inspection_no__inspection_officer=desigid,inspection_no__dept=dept_id).values().order_by('-inspection_no__inspected_on')
            elif div_id=="":
                print(div_id, '33')
                item_details=m1.Item_details.objects.filter(inspection_no__inspection_officer=desigid,inspection_no__zone=rly_id,inspection_no__dept=dept_id).values().order_by('-inspection_no__inspected_on')
            elif dept_id=="":
                print(dept_id, '44')
                item_details=m1.Item_details.objects.filter(inspection_no__inspection_officer=desigid,inspection_no__zone=rly_id,inspection_no__division=div_id).values().order_by('-inspection_no__inspected_on')
            else:
                print(rly_id,div_id,dept_id, '55')
                item_details=m1.Item_details.objects.filter(inspection_no__inspection_officer=desigid,inspection_no__zone=rly_id,inspection_no__division=div_id,inspection_no__dept=dept_id).values().order_by('-inspection_no__inspected_on')
            print(item_details,'01234')

            for i in item_details:
                if i['type'] == 'SH' and m1.Marked_Officers.objects.filter(item_no_id=i['item_no'], status_flag=1):
                    print('ENTERED')
                    temp={}
                    temp['sr_no']=count
                    temp['inspection_no']=i['inspection_no_id']
                    note_no=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'],created_by=cuser)[0].inspection_note_no
                    temp['inspection_note_no']=note_no
                    temp['item_no']=i['item_no']
                    temp['observation']=i['observation']
                    inspected_on=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'],created_by=cuser)[0].inspected_on
                    temp['inspected_on']=inspected_on.strftime("%d/%m/%y") if inspected_on!=None else 'NA'
                    mark=m1.Marked_Officers.objects.filter(item_no=i['item_no']).values()
                    desig_longdesc1=""
                    for x in mark:
                        print('xxxxxxxxx', x['myuser_id_id'])
                        marked=models.Level_Desig.objects.filter(designation_code=x['marked_to_id'])
                        print('yyyyyyyy', marked[0].designation)
                        if  marked[0].designation:
                            desig_longdesc1 += marked[0].designation+', ' 
                    desig_long = desig_longdesc1.rstrip(' ,') 
                    print('========', desig_long, '========')
                    temp['marked_officers']=desig_long
                    list.append(temp)
                    count=count+1
            print(list,'listlist-------------------------')
    
    # for inspection done by others
        if(str=='for_me'):
            if rly_id=="" and div_id=="" and dept_id=="":
                print('00')
                item_details=m1.Item_details.objects.filter().values().order_by('-inspection_no__inspected_on')
            elif div_id=="" and dept_id=="":
                print(div_id,dept_id, '11')
                item_details=m1.Item_details.objects.filter(inspection_no__zone=rly_id).values().order_by('-inspection_no__inspected_on')
            elif rly_id=="":
                print(rly_id, '22')
                item_details=m1.Item_details.objects.filter(inspection_no__dept=dept_id).values().order_by('-inspection_no__inspected_on')
            elif div_id=="":
                print(div_id, '33')
                item_details=m1.Item_details.objects.filter(inspection_no__zone=rly_id,inspection_no__dept=dept_id).values().order_by('-inspection_no__inspected_on')
            elif dept_id=="":
                print(dept_id, '44')
                item_details=m1.Item_details.objects.filter(inspection_no__zone=rly_id,inspection_no__division=div_id).values().order_by('-inspection_no__inspected_on')
            else:
                print(rly_id,div_id,dept_id, '55')
                item_details=m1.Item_details.objects.filter(inspection_no__zone=rly_id,inspection_no__division=div_id,inspection_no__dept=dept_id).values().order_by('-inspection_no__inspected_on')
            print(item_details,'01234')
            
            for i in item_details:
                if i['type'] == 'SH' and m1.Marked_Officers.objects.filter(item_no_id=i['item_no'], marked_emp=cuser, status_flag=1):
                    print('ENTERED')
                    temp={}
                    temp['sr_no']=count
                    temp['inspection_no']=i['inspection_no_id']
                    note_no=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'])[0].inspection_note_no
                    temp['inspection_note_no']=note_no
                    temp['item_no']=i['item_no']
                    temp['observation']=i['observation']
                    inspected_on=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'])[0].inspected_on
                    temp['inspected_on']=inspected_on.strftime("%d/%m/%y") if inspected_on!=None else 'NA'
                    inspect_officer=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'])[0].created_by
                    inspecting_officer=models.Level_Desig.objects.filter(empno_id=inspect_officer)[0].designation
                    temp['inspecting_officer']=inspecting_officer if inspecting_officer!=None else 'NA'
                    list.append(temp)
                    count=count+1
            print(list,'listlist-------------------------')
    return JsonResponse({'item_details':list,})


def reject_forward_reply(request):
    print('HAHAHAHAHAHAHA')
    if request.method == "GET" and request.is_ajax():
        print('condition 1')
        forward=request.GET.get('forward')
        print(forward,'forward')
        remark=request.GET.get('remark')
        print(remark,'remark')
        cuser=request.user.username
        desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
        print(cuser,desigid,'CUSER, DESIGID')
        reject_list=m1.Marked_Officers_forward.objects.filter(marked_to_forward_id=desigid).values()
        print(reject_list,'reject_list')
        for i  in reject_list:
            if m1.Marked_Officers_forward.objects.filter(marked_no_forward=forward):
                desigid=m1.Marked_Officers_forward.objects.filter(marked_no_forward=forward)[0].marked_to_forward_id
                if(m1.Officers_Remark.objects.filter(marked_no_forward_id=forward).exists()):
                    m1.Officers_Remark.objects.filter(marked_no_forward_id=forward).update(status_flag=1)
                # else:
                m1.Officers_Remark.objects.create(rejected_on=datetime.now(), reply_on=i['reply_on'],reply_received=i['compliance_forward'],marked_no_forward_id=forward, marked_desig_id_id=desigid,remark=remark,)
                m1.Marked_Officers_forward.objects.filter(marked_no_forward=forward).update(status_flag=3)
                return JsonResponse({}, safe = False) 
    return JsonResponse({})


def compliance_form_forward(request):
    print('compliance-form-forward')
    listgrid=[]
    count=1
    cuser=request.user.username
    desigid=models.Level_Desig.objects.filter(official_email_ID=cuser)[0].designation_code
    print(cuser,desigid,'CUSER, DESIGID')
    item_details=m1.Item_details.objects.values().order_by('-inspection_no__inspected_on')
    print(item_details,'01234')
    for i in item_details:
        if i['type'] == 'SH' and m1.Marked_Officers.objects.filter(item_no_id=i['item_no'], marked_to_id=desigid, status_flag=1):
            marked=m1.Marked_Officers.objects.filter(item_no_id=i['item_no'],status_flag=1,marked_to_id=desigid).values('item_no_id')
            if m1.Marked_Officers_forward.objects.filter(marked_no_id__item_no_id__in=marked,status_flag=1):
                temp={}
                temp['sr_no']=count
                temp['inspection_no']=i['inspection_no_id']
                note_no=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'])[0].inspection_note_no
                temp['inspection_note_no']=note_no
                temp['item_no']=i['item_no']
                temp['observation']=i['observation']
                inspected_on=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'])[0].inspected_on
                temp['inspected_on']=inspected_on.strftime("%d/%m/%y") if inspected_on!=None else 'NA'
                inspect_officer=m1.Inspection_details.objects.filter(inspection_no=i['inspection_no_id'])[0].inspection_officer_id
                inspecting_officer=models.Level_Desig.objects.filter(designation_code=inspect_officer)[0].designation
                print(inspecting_officer,'inspecting_officer')
                temp['inspecting_officer']=inspecting_officer if inspecting_officer!=None else 'NA'
                listgrid.append(temp)
                count=count+1
    print(listgrid,'-------------------------,pending')
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code').order_by('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').order_by('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name').order_by('department_name')
    list6=[]
    for i in list5:
        # print(i['department_name'],'_________')
        list6.append(i['department_name']) 
    context={
        'zone':list2 ,
        'division':list4,
        'dept':list6,
        'listgrid':listgrid,
    }
    print(list2,'_____________')
    return render(request,'compliance_form_forward.html',context)


# END-GUNJAN
# def home(request):
#     if request.method == "POST":
#         firstName=request.POST.get('firstName')
#         middleName=request.POST.get('middleName')
#         lastName=request.POST.get('lastName')
#         email=request.POST.get('official_emailID')
#         official_mobileNo=request.POST.get('official_mobileNo')
#         personal_emailID=request.POST.get('personal_emailID')
#         personal_mobileNo=request.POST.get('personal_mobileNo')
#         faxNo=request.POST.get('faxNo')
#         aadhaarNo=request.POST.get('aadhaarNo')
#         password=request.POST.get('password')
#         user.objects.create_user(first_name=firstName,middle_name=middleName,last_name=lastName
#         ,email=email,official_mobileNo=official_mobileNo,personal_emailID=personal_emailID,
#         personal_mobileNo=personal_mobileNo,faxNo=faxNo,aadhaar_no=aadhaarNo,password=password)
#     return render(request, 'home.html')

#furqan

def railway_zone(request):
    data = models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_description','location_code').order_by('location_code')
    #data1 = models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_description','location_code')
    list1=[]

        
    for i in data:
        temp={}
        c1=0
        c2=0
        c3=0
        t= m1.Inspection_details.objects.filter(zone=i['location_code']).values('inspection_no')
        if len(t)>0:
            for j in t:
                temp1=m1.Item_details.objects.filter(inspection_no=j['inspection_no']).values()
                for c in temp1:
                    if c['status_flag'] ==1:
                        c1 +=1
                    elif c['status_flag'] ==2:
                        c2+=1
                    elif c['status_flag'] ==3:
                        c3+=1
                        
            temp3=len(temp1)     
        else:
            temp3=0
        
        temp['ins_no']=temp3
        temp['location_description']=i['location_description']
        temp['location_code']=i['location_code']
        temp['c1']= c1
        temp['c2']= c2
        temp['c3']= c3
        list1.append(temp)
    return JsonResponse({'data':list1}, safe=False)

def item_divsion(request):
    data1 = models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_description','parent_location_code','location_code').order_by('parent_location_code','location_code')
    #print(data1)
    list2=[]
    for i in data1:
        temp1={}
        c1=0
        c2=0
        c3=0
        t1 = m1.Inspection_details.objects.filter(division=i['location_code']).values()
        print(t1)
        if len(t1)>0:
            for j in t1:
               temp2 = m1.Item_details.objects.filter(inspection_no=j['inspection_no']).values()
               for c in temp2:
                    if c['status_flag'] ==1:
                        c1 +=1
                    elif c['status_flag'] ==2:
                        c2+=1
                    elif c['status_flag'] ==3:
                        c3+=1
            temp4 = len(temp2)
        else:
            temp4=0
        
        
        temp1['ins_no']=temp4
        temp1['location_description']=i['location_description']
        temp1['location_code']=i['location_code']
        temp1['parent_location_code']=i['parent_location_code']
        temp1['c1'] = c1
        temp1['c2'] = c2
        temp1['c3'] = c3
        list2.append(temp1)
       
    return JsonResponse({'data1':list2}, safe=False)
#24.06.22
def item_detail_view(request):
    itdv = m1.Item_details.objects.values('inspection_no','inspection_no__inspection_title','inspection_no__dept','inspection_no__inspected_on','status','inspection_no__inspection_officer','target_date','observation', 'item_no') 
    return render(request,'items_dt_view.html', context={'itdv':itdv})
#27-06-22
def item_view_inspect(request, item):
    ivi = m1.Item_details.objects.filter(item_no=item).values('item_no','inspection_no','inspection_no__zone','inspection_no__dept','inspection_no__location','item_title','modified_on','modified_by','status_flag','status','created_on','observation','marked_officers','created_by','target_date')

    return render(request,'item_view_inspect.html',context={'ivi':ivi})

from django.shortcuts import render,redirect
def schedular_form(request):
    
    list1=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')

    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
    print(list3)
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])
        print(list4)
    #empdata=m1.empmast.objects.values('empname','empno', 'desig_longdesc')
    #desig_longdesc = empdata[0]['desig_longdesc']
    list5=list(models.Level_Desig.objects.all().values('designation_code', 'designation'))
    list6=models.departMast.objects.all().values('department_name')
    #new code
    ins_id=request.GET.get('ins_id')
    # print(ins_id,'______________________________')
    ins_detail=[]
    item_id=[]
    length = 0
    sh = []
    ssh = []
    if ins_id!=None:
        # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        ins_detail=list(m1.Inspection_details.objects.filter(inspection_no=ins_id).values())
        item_details1= list(m1.Item_details.objects.filter(inspection_no_id=ins_id).values().order_by('item_no'))
        item_data= m1.Item_details.objects.filter(inspection_no_id=ins_id, type="H").values()
        length += item_data.count()

        for zb in item_details1:
            item_id.append(zb['des_id'])

        for x in range(len(item_data)):
            mid= str(x+1)+'.'
            itmdata = m1.Item_details.objects.filter(inspection_no_id=ins_id, type="SH", des_id__startswith=mid).values()
            ssh.append(0)
            sh.append(len(itmdata))
            for y in range(len(itmdata)):
                nid= str(x+1)+'.'+ str(y+1)+'.'
                itmdata1 = m1.Item_details.objects.filter(inspection_no_id=ins_id, type="SSH", des_id__startswith=nid).count()
                ssh.append(itmdata1)
        
        print('len', length,'sh',  sh,'ssh', ssh)
        for j in item_details1:
            
            if j['type'] == 'SH':
                mark=m1.Marked_Officers.objects.filter(item_no=j['item_no']).values()
                print('---------', j['item_no'])
                mrkoffi = {}
                desig_longdesc1 =''
                marked_officers1 = ''
                for x in mark:
                    # print('xxxxxxxxx', x['myuser_id_id'])
                    
                    marked=m1.empmast.objects.filter(myuser_id=x['myuser_id_id'])
                    # print('yyyyyyyy', marked[0].desig_longdesc)
                    desig_longdesc1 += marked[0].desig_longdesc+','
                    marked_officers1 += marked[0].empno+','
                # print('kkkkkkkkkkkkkkk', desig_longdesc1)
                mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': desig_longdesc1})
                
                j.update({'mrkoffi': mrkoffi})
                # print('mmmmmmmm', desig_longdesc1)
            
        ins_detail[0].update({'item_details1': item_details1})
        # print('00000000', ins_detail)
        # print('00000000', ins_detail)

    if request.method == 'POST':
        print(request.POST)
        event_title = request.POST.get('event_title')
        description = request.POST.get('description')
        x= m1.Events(event_title=event_title,description=description)
      #  y= x.event_id
        t=x.save()
                
        y1= m1.Events.objects.get(event_title=event_title,description=description)


        Railways_act = request.POST.get('Railways_act0')
        Division_act = request.POST.get('Division_act0')
        location3_act = request.POST.get('location3_act0')
        date_to_act = request.POST.get('date_to_act0')
        date_to_act = datetime.strptime(date_to_act, '%d-%m-%Y').strftime('%Y-%m-%d')
        z=m1.Event_activty(Railways_act=Railways_act,Division_act=Division_act,location3_act=location3_act,date_to_act=date_to_act,event_id=y1)
        # print('--------------check event activity data-------',z)
        z.save()
        
    
        mylen = int(request.POST.get('len2'))
        
        for i in range(mylen-1):
          Railways_act1 = request.POST.get("Railways_act0" + str(i))
          Division_act1 = request.POST.get("Division_act0" + str(i))
          print("divsion",Division_act1)
          location3_act1 = request.POST.get("location3_act0" + str(i))
          date_to_act1 = request.POST.get("date_to_act0" + str(i))
          print("mydata",date_to_act1)
          date_to_act12 = datetime.strptime(str(date_to_act1),'%d-%m-%Y').strftime('%Y-%m-%d')
        
          m1.Event_activty.objects.create(Railways_act=Railways_act1,Division_act=Division_act1,location3_act=location3_act1,date_to_act=date_to_act12,event_id=y1)                   
        # empdata=m1.empmast.objects.filter(myuser_id=request.user).values('empname','empno', 'desig_longdesc')
        # desig_longdesc = empdata[0]['desig_longdesc']
        # list5=list(m1.Designation_Master.objects.all().values('master_name','designation_master_no','master_email'))
        # list6=models.departMast.objects.all().values('department_name')
  

        list1=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
        print("list1",list1)
        list2=[]
        for i in list1:
        # print(i['location_code'],'_________')
          list2.append(i['location_code'])
          list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
          print("list3",list3)
          list4=[]
        for i in list3:
        # print(i['location_code'],'_________')
           list4.append(i['location_code'])
        print(list4)
        messages.success(request,"data is saved")
        
        # for new code
        ins_id=request.GET.get('ins_id')
    # print(ins_id,'______________________________')
    ins_detail=[]
    item_id=[]
    length = 0
    sh = []
    ssh = []
    if ins_id!=None:
        # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        ins_detail=list(m1.Inspection_details.objects.filter(inspection_no=ins_id).values())
        item_details1= list(m1.Item_details.objects.filter(inspection_no_id=ins_id).values().order_by('item_no'))
        item_data= m1.Item_details.objects.filter(inspection_no_id=ins_id, type="H").values()
        length += item_data.count()

        for zb in item_details1:
            item_id.append(zb['des_id'])

        for x in range(len(item_data)):
            mid= str(x+1)+'.'
            itmdata = m1.Item_details.objects.filter(inspection_no_id=ins_id, type="SH", des_id__startswith=mid).values()
            ssh.append(0)
            sh.append(len(itmdata))
            for y in range(len(itmdata)):
                nid= str(x+1)+'.'+ str(y+1)+'.'
                itmdata1 = m1.Item_details.objects.filter(inspection_no_id=ins_id, type="SSH", des_id__startswith=nid).count()
                ssh.append(itmdata1)
        
        print('len', length,'sh',  sh,'ssh', ssh)
        for j in item_details1:
            
            if j['type'] == 'SH':
                mark=m1.Marked_Officers.objects.filter(item_no=j['item_no']).values()
                print('---------', j['item_no'])
                mrkoffi = {}
                desig_longdesc1 =''
                marked_officers1 = ''
                for x in mark:
                    print('xxxxxxxxx', x['myuser_id_id'])
                    
                    marked=m1.empmast.objects.filter(myuser_id=x['myuser_id_id'])
                    print('yyyyyyyy', marked[0].desig_longdesc)
                    desig_longdesc1 += marked[0].desig_longdesc+','
                    marked_officers1 += marked[0].empno+','
                print('kkkkkkkkkkkkkkk', desig_longdesc1)
                mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': desig_longdesc1})
                
                j.update({'mrkoffi': mrkoffi})
                # print('mmmmmmmm', desig_longdesc1)
            
        ins_detail[0].update({'item_details1': item_details1})
        # print('00000000', ins_detail)
        print('00000000', ins_detail)

        # Event_Activity.objects.create(Railways=Railways,Division=Division,location3=location3,date_to=date_to)
 
        
    
    return render(request,'schedular_form.html',context={'Zone':list2,'Division':list4,'marked_to':list5,'department':list6, 'ins_detail':ins_detail,
            'item_id': item_id,
            'length_of_h': length,
            'sh_list': sh,
            'ssh_list': ssh}) 
from django.core.paginator import Paginator
def schedular(request):
    
    sdv = list(m1.Event_activty.objects.values('event_id__event_title','event_id__description','Railways_act','Division_act','location3_act','date_to_act','status').order_by('-activity_id'))
    for i in sdv:        
        if i['status'] == '0':
            print("Event is in begining")
        
    paginator = Paginator(sdv, 6) # Show 6  event in one page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'Schedular.html',context={'page_obj': page_obj})

def EditFunction(request):
    if request.method == 'GET' and request.is_ajax():
        activity_id = request.GET.get('id')
        activity_obj = list(m1.Event_activty.objects.filter(activity_id=activity_id).values('Railways_act','Division_act','location3_act','date_to_act','activity_id'))
        print('print ajax edit',activity_obj)
        # return JsonResponse({'activity_obj':activity_obj})
        return JsonResponse(activity_obj,safe=False)
    return JsonResponse({'success':False},status=400)

def saveFunction(request):
    if request.method == 'POST' and request.is_ajax():
        rail = request.POST.get('railways')
        div = request.POST.get('Division')
        location = request.POST.get('location')
        date = request.POST.get('date')
        # updated_date = datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')

        activity_id = request.POST.get('activity_id')
        print('----checking save function-----',rail)
        print('-----check division-----',div)
        print('-----location-----',location)
        print('-----date-----',date)
        print('-----activity_id-----',activity_id)
        act_obj = m1.Event_activty.objects.filter(activity_id=activity_id).update(Railways_act=rail,Division_act=div,location3_act=location,date_to_act=date)
        return JsonResponse(act_obj,safe=False)
    return JsonResponse({'success':False},status=400)

# end furqan
def create_inspection_details(request):
    if request.method == "POST" and request.is_ajax():
        from datetime import datetime
        final=request.POST.get('final_partinspected')
        final_id=request.POST.get('id_partinspected')


        rly=json.loads(request.POST.get('zone'))
        div=json.loads(request.POST.get('division'))
        dept=json.loads(request.POST.get('department'))
        loc=json.loads(request.POST.get('location'))
        insdt=request.POST.get('txtDate2')
        print(insdt, '-----------')
        if 'to' in insdt:
            dt = insdt.split('to')
            st_date = dt[0].strip()
            en_date = dt[1].strip()

            start_date = datetime.strptime(st_date, '%d/%m/%Y').strftime('%Y-%m-%d')
            inspected_on = datetime.strptime(en_date, '%d/%m/%Y').strftime('%Y-%m-%d')

        else:
            
            inspected_on = datetime.strptime(insdt, '%d/%m/%Y').strftime('%Y-%m-%d')
            start_date = datetime.strptime(insdt, '%d/%m/%Y').strftime('%Y-%m-%d')

        
    
        
        title=request.POST.get('titleinsp')
        send_to=request.POST.get('send_to')
        send_desig=request.POST.get('send_desig')
        
        
        
        finalval = json.loads(final)
        final_allid = json.loads(final_id)

        
        year = str(datetime.now().year)

        # empno=models.Level_Desig.objects.filter(official_email_ID=request.user)
        empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation
            ddesig = empnox[0].designation_code


        else:
            messages.error(request, 'Employee id not found')
            


        # desig = models.Level_Desig.objects.get(empno=empno).designation


        # last_note = m1.Inspection_details.objects.aggregate(Max('insp_last'))['insp_last__max']
        # note_ = year+'/'+desig+'/Insp'+'/'
        # last_note1 = m1.Inspection_details.objects.filter(inspection_note_no__istartswith=note_).aggregate(Max('insp_last'))['insp_last__max']
        
        # if last_note == None:
        #     last_note = 1
        #     note_no = year+'/'+desig+'/Insp'+'/'+ str(last_note)
            
        # else:
        #     last_note = last_note +1
        #     note_no = year+'/'+desig+'/Insp'+'/'+ str(last_note)

        
        
        note_ = year+'/'+desig+'/Insp'+'/'
        # last_note1 = m1.Inspection_details.objects.filter(inspection_note_no__istartswith=note_).aggregate(Max('insp_last'))['insp_last__max']
        last_note1 = m1.Inspection_details.objects.filter(inspection_note_no__istartswith=note_).aggregate(Max('insp_last'))
        
        # print('last_note1', last_note1)
        
        if len(last_note1) == 0:
            last_note1 = 1
            note_no = year+'/'+desig+'/Insp'+'/'+ str(last_note1)
            
        else:
            last_note1 = int(last_note1['insp_last__max']) +1
            note_no = year+'/'+desig+'/Insp'+'/'+ str(last_note1)

        
        

        # ddesig=models.Level_Desig.objects.get(empno=empno)
        

        m1.Inspection_details.objects.create(inspection_title=title,created_on=datetime.now(),created_by=empno, insp_last=last_note1,inspection_note_no=note_no, inspection_officer_id=ddesig, item_type='Insp', modified_by=empno, status_flag=1, start_date=start_date, inspected_on=inspected_on)
        
        messages.info(request, f'Inspection note successfully saved with Inspection Note No: {note_no}')
        

        inspection_id=m1.Inspection_details.objects.all().last().inspection_no
        for rl in rly:
            m1.Insp_multi_location.objects.create(inspection_no_id=inspection_id, item=rl, type='HQ')
        for di in div:
            m1.Insp_multi_location.objects.create(inspection_no_id=inspection_id, item=di, type='DIV')
        for dp in dept:
            m1.Insp_multi_location.objects.create(inspection_no_id=inspection_id, item=dp, type='DPT')
        for lo in loc:
            m1.Insp_multi_location.objects.create(inspection_no_id=inspection_id, item=lo, type='LOC')
        

        officer_email=[]
        for f, b in zip(finalval, final_allid):
            print(finalval[f], final_allid[b])
            for x,y in zip(finalval[f], final_allid[b]):
                s = y.split('.')
                if len(s) == 1:
                    hed = 'heading'+y
                    heading = finalval[f][hed]
                    m1.Item_details.objects.create(item_title=heading,status_flag=1, created_on=datetime.now(), type='H',des_id=y, inspection_no_id=inspection_id)
                    y2=str(y+'.1')
                    if y2 in final_allid[b]:
                        print('if',y2)
                        pass
                    else:
                        print('else',y2)
                        trz = 'targetdate'+y
                        officm = 'markeofficer'+y
                        chk = 'check' + y
                        
                        targetd = finalval[f][trz]
                        markof = finalval[f][officm]
                        checkbox = finalval[f][chk]

                        if checkbox == '1':
                            checkbox = 1
                        else:
                            checkbox = 0
                        markeofficer = markof.split(',')
                        if targetd:
                            t_date = datetime.strptime(targetd, '%d/%m/%Y').strftime('%Y-%m-%d')
                        else:
                            t_date = None
                        m1.Item_details.objects.filter(item_title=heading,status_flag=1, type='H',des_id=y, inspection_no_id=inspection_id).update(target_date=t_date, priority=checkbox)
                        item_id=m1.Item_details.objects.all().last().item_no
                        #mark officer
                        
                        if markof:
                            for i in markeofficer:
                                # myuser_id=m1.empmast.objects.filter(empno=i)[0].myuser_id_id
                                # desig_longdesc=m1.empmast.objects.filter(empno=i)[0].desig_longdesc
                                # print('uuuuuuuuuuuuuuuuuu', desig_longdesc)
                                Desig=models.Level_Desig.objects.filter(empno=i)
                                
                                
                                
                                email = m1.empmast.objects.filter(empno=i)[0].email
                                officer_email.append(email)

                                

                                if Desig:
                                    Desig=Desig[0].designation_code
                                    if m1.Marked_Officers.objects.all().last():
                                        marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                                    else:
                                        marked_no_id = 1
                                    m1.Marked_Officers.objects.create(marked_emp=i,created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig))
                                else:
                                    print('error')
                                    # messages.info(request, 'Employ Desig not Match in Designation Master')

                elif len(s) == 2:
                    ob = 'observation'+y
                    trz = 'targetdate'+y
                    officm = 'markeofficer'+y
                    chk = 'check' + y

                    observation = finalval[f][ob]
                    targetd = finalval[f][trz]
                    markof = finalval[f][officm]
                    markeofficer = markof.split(',')

                    checkbox = finalval[f][chk]

                    if checkbox == '1':
                        checkbox = 1
                    else:
                        checkbox = 0
                    

                    if targetd:
                        targetdate = datetime.strptime(targetd, '%d/%m/%Y').strftime('%Y-%m-%d')
                    else:
                        targetdate = None
                    print(observation)
                    m1.Item_details.objects.create(observation=observation,priority=checkbox, status_flag=1,inspection_no_id=inspection_id, des_id=y, target_date=targetdate, type='SH')
                    
                    item_id=m1.Item_details.objects.all().last().item_no
                    #mark officer
                    
                    if markof:
                        for i in markeofficer:
                            # myuser_id=m1.empmast.objects.filter(empno=i)[0].myuser_id_id
                            # desig_longdesc=m1.empmast.objects.filter(empno=i)[0].desig_longdesc
                            # print('uuuuuuuuuuuuuuuuuu', desig_longdesc)
                            Desig=models.Level_Desig.objects.filter(empno=i)
                            
                            
                            
                            email = m1.empmast.objects.filter(empno=i)[0].email
                            officer_email.append(email)

                            

                            if Desig:
                                Desig=Desig[0].designation_code
                                if m1.Marked_Officers.objects.all().last():
                                    marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                                else:
                                    marked_no_id = 1
                                m1.Marked_Officers.objects.create(created_on=datetime.now(),created_by=empno,marked_emp=i,marked_no=marked_no_id,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig))
                            else:
                                print('error')
                                # messages.info(request, 'Employ Desig not Match in Designation Master')
                    else:
                        markeofficer=""

                
                      
                else:
                    subdes = 'subdes'+y
                    subdes1 = finalval[f][subdes]
                    m1.Item_details.objects.create(item_subtitle=subdes1,status_flag=1, type='SSH',des_id=y, inspection_no_id=inspection_id)
        try:

            To=officer_email

            subject="Inspection report"
            # To=['ecegcttarun@gmail.com','kr.abhijeet6235@gmail.com']
            context = {'title': title}
                
            InspSendMail(subject, To, context)

            m1.Insp_mail_details.objects.create(subject=subject, body=title,area='Mark Of', inspection_no_id=inspection_id, send_to=send_to,send_desig=send_desig)
            messages.success(request, 'Mark officer email has been sent')
            
        except:
            print("error on sending")
            messages.error(
                request, 'Email send failed. Please Try Again.')
        # try:
        offic_mail =[]
        if send_to:
            emil = send_to.split(',')
            for i in emil:
                email = m1.empmast.objects.filter(empno=i)[0].email
                offic_mail.append(email)

            subject="Inspection report"
            To = offic_mail
            # To=['ecegcttarun@gmail.com','kr.abhijeet6235@gmail.com']
            context = {'title': title}
                
            InspSendMail(subject, To, context)
            m1.Insp_mail_details.objects.create(subject=subject, body=title, area='Copy To', inspection_no_id=inspection_id, send_to=send_to,send_desig=send_desig)
            messages.success(request, 'Copy to Email has been sent')
            
        # except:
            
        #     messages.error(request, 'Email send failed.') 

        return JsonResponse({"status": 1 })
    return JsonResponse({"success":False}, status=400)
    # except Exception as e:
    #     print("e==",e)  
    #     return render(request, "commonerrorpage.html", {})



def MailSend(subject,email_body1,To):
    try:
        # subject = "Verify Your Mail"
        email = 'mfgcris@cris.org.in'

        html_content= MIMEText(email_body1+'<br><div class="container"><img src="cid:myimage"/></div><div style="text-align:center"><a href="#"> Unsubscribe</a></div>', _subtype='html')
        text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

        text_file = open("mail.txt", "a") # opening my file
        time=datetime.now()
        date_time=time.strftime("%m/%d/%Y,%H:%M:%S")

        text_file.write("\n\n"+date_time+"\n"+email+'\n'+To+"\n"+subject+"\n"+text_content) 
        text_file.write(text_content) 
        text_file.close() #file close

        img_data = open('rkvy/static/rkvy/images/logo_rkvy.png', 'rb').read()

        html_part = MIMEMultipart(_subtype='related')

        # Create the body with HTML. Note that the image, since it is inline, is 
        # referenced with the URL cid:myimage... you should take care to make
        # "myimage" unique
        html_part.attach(html_content)

        # Now create the MIME container for the image
        img = MIMEImage(img_data, 'png')
        img.add_header('Content-Id', '<myimage>')  # angle brackets are important
        img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
        html_part.attach(img)

        # Configure and send an EmailMessage
        # Note we are passing None for the body (the 2nd parameter). You could pass plain text
        # to create an alternative part for this message
        msg = EmailMessage(subject, None, email, [To])
        msg.attach(html_part) # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
        msg.send()
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="MailSend",err_details=str(e))
        except:
            print("Internal Error!!!")


# def loginUser(request):
#     # try:
#         if request.method == "POST":
#             _email = request.POST.get('email').strip()
#             _password = request.POST.get('password').strip()
#             print(_email,'____')
#             print(_password,'_____')
#             # obj3=models.rkvy_userEnrollment.objects.filter(user_id__email=_email).values('pending_stage')
#             # check for existence
#             userObj = authenticate(username=_email, password=_password)
#             print(userObj.username)

#             print("22222222222222222222222227777777777777777777777777777777777777777777777^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",userObj)
#             if userObj is not None:
#                 login(request, userObj)
#                 print("inside login&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
#                 if userObj.user_role == 'rkvy_superadmin':
#                     return HttpResponseRedirect('/rkvy_superAdminHome')
#                 elif userObj.user_role == 'rkvy_headquarteradmin':
#                     return HttpResponseRedirect('/rkvy_headquarterAdminHome')
#                 elif userObj.user_role == 'rkvy_instituteadmin':
                    
#                     return HttpResponseRedirect('/rkvy_instituteAdminHome')
#                 elif userObj.user_role == 'rkvy_instructor':
#                     return HttpResponseRedirect('/rkvy_instructorHome')
#                 elif userObj.username=='admin':
#                     return HttpResponseRedirect('/adminuserHome')
#                 else:
#                     # return HttpResponseRedirect('/userHome')
#                     print("11111111111111111111111")
#                     return render(request, "base.html")
#                     # return render(request,"list_create_inspection_report.html")
                    
#             else:
#                 #change 21-10
#                 if user.objects.filter(email=_email,user_role='rkvy_trainee',is_active=False).exists():
#                     messages.error(request, 'Email is not verified yet. Please verify first then login again.')
#                 else:
#                     messages.error(request, 'Invalid Credentials.')#till here 21-10
#                 #return HttpResponseRedirect('/rkvy_login')

#                 return render(request, "login.html")
#         print('hhhh')
#         return render(request, "login2.html")
    # except Exception as e: 
    #     try:
    #         models.error_Table.objects.create(fun_name="login",user_id=request.user,err_details=str(e))
    #     except:
            
    #         print("Internal Error->>>>>>>>>4!!!")
    #     #messages.error(request, 'Error : '+str(e))
    #     return render(request, "login.html", {})
def userHome(request):
    return render(request,"userHome.html")

def zonaluserHome(request):
    return render(request,"zonaluserHome.html")


def divisonuserHome(request):
    return render(request,"divisonHome.html")

def requests(request):
    status=request.POST.get('status')
    id=request.user.username
    id=id[0:len(id)-3]
    lst=m1.user_request.objects.filter(rly_id=id,status='Pending').values('id','empno','myuser_id__first_name','requestDate','status')
    print(lst)
    if request.method== 'POST':
        req_id=request.POST.get('req_id')
        print(req_id)
        action=request.POST.get('action_1')
        lst=m1.user_request.objects.filter(rly_id=request.user.username,status='Accepted').values('id','empno','myuser_id__first_name','requestDate','status')

        if action=='Accept':
           
            myuser_id_id=m1.user_request.objects.filter(id=req_id).values('myuser_id_id','empno','rly_id_id')
            empdetails=models.HRMS.objects.filter(empno=myuser_id_id[0]['empno']).values('empname','designation','email','rly_id_id','div_id_id')
            m1.user_request.objects.filter(id=req_id).update(status='Accepted')
            user.objects.filter(id=myuser_id_id[0]['myuser_id_id']).update(is_active=True,user_role='user',username=myuser_id_id[0]['empno'])

            m1.empmast.objects.create(empno=myuser_id_id[0]['empno'],empname=empdetails[0]['empname'],desig_longdesc=empdetails[0]['designation']
            ,email=empdetails[0]['email'],myuser_id_id=myuser_id_id[0]['myuser_id_id']
                    ,rly_id_id=empdetails[0]['rly_id_id'],div_id_id=empdetails[0]['div_id_id'])
        if action == 'Reject':
            m1.user_request.objects.filter(id=req_id).update(status='Rejected')

    if status=='Accepted' or status=='Rejected':
            r=False
    else:
            r=True
    context={'result':lst,'r':r,'status':status}

    return render(request,"requestList.html",context)

def Divisonrequests(request):
    try:
        status=request.POST.get('status')
        id=request.user.username
        id=id[0:len(id)-3]
        lst=m1.user_request.objects.filter(rly_id=id,status='Pending').values('id','empno','myuser_id__first_name','requestDate','status')
        if request.method== 'POST':
            req_id=request.POST.get('req_id')
            print(req_id)
            action=request.POST.get('action_1')
            lst=m1.user_request.objects.filter(rly_id=request.user.username,status=status).values('id','empno','myuser_id__first_name','requestDate','status')
            if action=='Accept':
                myuser_id_id=m1.user_request.objects.filter(id=req_id).values('myuser_id_id','empno','rly_id_id')
                empdetails=models.HRMS.objects.filter(empno=myuser_id_id[0]['empno']).values('empname','designation','email','rly_id_id','div_id_id')
                m1.user_request.objects.filter(id=req_id).update(status='Accepted')

                user.objects.filter(id=myuser_id_id[0]['myuser_id_id']).update(is_active=True,user_role='user',username=myuser_id_id[0]['empno'])
                m1.empmast.objects.create(empno=myuser_id_id[0]['empno'],empname=empdetails[0]['empname'],desig_longdesc=empdetails[0]['designation']
                ,email=empdetails[0]['email'],myuser_id_id=myuser_id_id[0]['myuser_id_id']
                        ,rly_id_id=empdetails[0]['rly_id_id'],div_id_id=empdetails[0]['div_id_id'])
            if status=='Reject':
                m1.user_request.objects.filter(id=req_id).update(status='Rejected')
        print(status)
        if status=='Accepted' or status=='Rejected':
            r=False
        else:
            r=True
        context={'result':lst,'r':r,'status':status}

        return render(request,"divisonRequestList.html",context)
    except Exception as e:
        print(e)

def forgotPassword(request):
    # try:
        if request.method == "POST":
            _email = request.POST.get('email').strip()

            try:
                userObj = user.objects.get(email=_email)
                #print(userObj)
            except Exception as e:
                messages.error(request, 'Please enter registed email.')
                return HttpResponseRedirect('/forgotPassword')

            email_context = {
                "email": userObj.email,
                'domain': 'railkvy.indianrailways.gov.in',
                'site_name': 'Kaushal Vikas',
                "uid": urlsafe_base64_encode(force_bytes(userObj.pk)),
                "user": userObj,
                'token': default_token_generator.make_token(userObj),
                'protocol': 'http',
            }
            email_template_name = "email_forgotPassword_body.txt"
            email_body = render_to_string(email_template_name, email_context)
            try:
                #print("trying to send mail")
                #print(userObj.email)
                try:
                    # send_mail("Verify Your Mail", email_body, 'crisdlwproject@gmail.com',
                    #          [f'{userObj.email}'], fail_silently=False)


                    #saud faisal (28-08-2021) -----
                    subject="Reset password for RKVY login"
                    To=userObj.email
                    email_body1='<p>'+email_body+'</p>'
                    MailSend(subject,email_body1,To)
                    #end here
                    return HttpResponse('Verification Email has been successfully sent.(see also spam folder)')
                except:
                    print("error on sending")
                    messages.error(
                        request, 'Verification Email failed. Please Try Again.')
            except:
                messages.error(
                    request, 'Something went wrong.')
            return render(request, "inspects_forgotPassword.html")

        return render(request, "inspects_forgotPassword.html")
    # except Exception as e: 
    #     try:
    #         models.error_Table.objects.create(fun_name="forgotPassword",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     #messages.error(request, 'Error : '+str(e))
    #     return render(request, "commanerrorpage.html", {})


#bhartistart
def create_inspection_form(request):
    # try:
    if request.method=="POST" :
        rly=request.POST.get('zone')
        div=request.POST.get('division')
        dept=request.POST.get('department')
        loc=request.POST.get('location')
        inspection_date=request.POST.get('start')
        # print("@@@@@@@@@@@@@@@@@@@")
    
    print('-----------', request.user)
    print('-----------', request.user.username)
    print('-----------', request.user.email)
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
   
    
    # desig_longdesc = empdata[0]['desig_longdesc']
    # print('ttttttttttttttttttttttttttttttttttttttttttttttttttttttt', desig_longdesc)
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code')
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
    # print(list2,'_____________')
    ins_id=request.GET.get('ins_id')
    # print(ins_id,'______________________________')
    ins_detail=[]
    item_id=[]
    length = 0
    sh = []
    ssh = []
    if ins_id!=None:
        item_t = m1.Inspection_details.objects.filter(inspection_no=ins_id).values('item_type')
        mail_detail = m1.Insp_mail_details.objects.filter(inspection_no=ins_id, area='Copy To')
        alldesig1 =models.Level_Desig.objects.values('designation').distinct().order_by('designation')
        print('=============' , alldesig1, '==========')
        
        if mail_detail:
            new_mail_detail= mail_detail[0].send_desig
            # print(new_mail_detail, '1111111111111111')

        else:
            new_mail_detail  = 'NA'
        
        item_type = item_t[0]['item_type']
        if item_type == 'Insp':
            # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            ins_detail=list(m1.Inspection_details.objects.filter(inspection_no=ins_id, item_type='Insp').values())
            item_details1= list(m1.Item_details.objects.filter(inspection_no_id=ins_id, inspection_no__item_type='Insp').values().order_by('item_no'))
            item_data= m1.Item_details.objects.filter(inspection_no_id=ins_id, type="H").values()
            multi_loc = m1.Insp_multi_location.objects.filter(inspection_no_id=ins_id).values()
            
            length += item_data.count()

            for zb in item_details1:
                item_id.append(zb['des_id'])

            for x in range(len(item_data)):
                mid= str(x+1)+'.'
                itmdata = m1.Item_details.objects.filter(inspection_no_id=ins_id, type="SH", des_id__startswith=mid).values()
                ssh.append(0)
                sh.append(len(itmdata))
                for y in range(len(itmdata)):
                    nid= str(x+1)+'.'+ str(y+1)+'.'
                    itmdata1 = m1.Item_details.objects.filter(inspection_no_id=ins_id, type="SSH", des_id__startswith=nid).count()
                    ssh.append(itmdata1)
            
            print('len', length,'sh',  sh,'ssh', ssh)
            for j in item_details1:
                mrkoffi = {}
                if j['type'] == 'SH':
                    mark=m1.Marked_Officers.objects.filter(item_no=j['item_no']).values()
                    print('---------', j['item_no'])
                    
                    desig_longdesc1 =''
                    marked_officers1 = ''
                    for x in mark:
                        # print('xxxxxxxxx', x['myuser_id_id'])
                        
                        # marked=m1.empmast.objects.filter(myuser_id=x['myuser_id_id'])
                        
                        # print('yyyyyyyy', marked[0].desig_longdesc)
                        # if marked[0].desig_longdesc:
                        #     desig_longdesc1 += marked[0].desig_longdesc+','

                        des = models.Level_Desig.objects.filter(designation_code=x['marked_to_id'])
                        desig_longdesc1 += des[0].designation+','
                        marked_officers1 += des[0].empno_id+','

                        print(des)
                    print('kkkkkkkkkkkkkkk', desig_longdesc1)


                    #################################   changed #############################
                    testmarkofficer=''
                    lstdict=[]
                    if marked_officers1 != '':
                        testdesig=desig_longdesc1.split(',')
                        testempno=marked_officers1.split(',')
                        testdesig.pop()
                        testempno.pop()
                        
                        
                        alldesig = models.Level_Desig.objects.filter(empno__in=testempno).values('d_level').distinct('d_level')
                        
                        for i in alldesig:
                            if i['d_level'] == 'GM':
                                lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(empno__in=testempno).count()
                                if lst1 == 0:
                                    lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level']).values('empno','designation').order_by('designation'))
                                    if testmarkofficer != '':
                                        testmarkofficer+=','
                                    testmarkofficer=testmarkofficer+"All GM's/ZR"
                                    # testempno=set(testempno)
                                    # part=set(map(lambda d: d['partno'], part))
                                    interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                    testempno=list(map(lambda d: d['empno'], lst2))
                                    testdesig=list(map(lambda d: d['designation'], lst2))
                                    lstdict.append({"desig":"All GM's/ZR","empno":list(interkey)})

                            elif i['d_level'] == 'BM':
                                lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(empno__in=testempno).count()
                                if lst1 == 0:
                                    lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level']).values('empno','designation').order_by('designation'))
                                    if testmarkofficer != '':
                                        testmarkofficer+=','
                                    testmarkofficer=testmarkofficer+"All Board Member's"
                                    # testempno=set(testempno)
                                    # part=set(map(lambda d: d['partno'], part))
                                    interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                    testempno=list(map(lambda d: d['empno'], lst2))
                                    testdesig=list(map(lambda d: d['designation'], lst2))
                                    lstdict.append({"desig":"All Board Member's","empno":list(interkey)})


                            elif i['d_level'] == 'PHOD':
                                lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(empno__in=testempno).count()
                                if lst1 == 0:
                                    lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level']).values('empno','designation').order_by('designation'))
                                    if testmarkofficer != '':
                                        testmarkofficer+=','
                                    testmarkofficer=testmarkofficer+"All PHOD's"
                                    # testempno=set(testempno)
                                    # part=set(map(lambda d: d['partno'], part))
                                    interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                    testempno=list(map(lambda d: d['empno'], lst2))
                                    testdesig=list(map(lambda d: d['designation'], lst2))
                                    lstdict.append({"desig":"All PHOD's","empno":list(interkey)})
                                else:
                                    hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
                                    for ii in hq:
                                        rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
                                        if models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exists():
                                            lst3=models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exclude(empno__in=testempno).count()
                                            if lst3 == 0:
                                                lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('empno','designation').order_by('designation'))
                                                if testmarkofficer != '':
                                                    testmarkofficer+=','
                                                testmarkofficer=testmarkofficer+"All PHOD's"+ii['parent_location_code']
                                                # testempno=set(testempno)
                                                # part=set(map(lambda d: d['partno'], part))
                                                interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                                testempno=list(map(lambda d: d['empno'], lst2))
                                                testdesig=list(map(lambda d: d['designation'], lst2))
                                                lstdict.append({"desig":"All PHOD's/"+ii['parent_location_code'],"empno":list(interkey)})



                            elif i['d_level'] == 'DRM':
                                lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(empno__in=testempno).count()
                                if lst1 == 0:
                                    lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level']).values('empno','designation').order_by('designation'))
                                    if testmarkofficer != '':
                                        testmarkofficer+=','
                                    testmarkofficer=testmarkofficer+"All DRM's"
                                    # testempno=set(testempno)
                                    # part=set(map(lambda d: d['partno'], part))
                                    interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                    testempno=list(map(lambda d: d['empno'], lst2))
                                    testdesig=list(map(lambda d: d['designation'], lst2))
                                    lstdict.append({"desig":"All DRM's","empno":list(interkey)})
                                else:
                                    hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
                                    for ii in hq:
                                        rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
                                        if models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exists():
                                            lst3=models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exclude(empno__in=testempno).count()
                                            if lst3 == 0:
                                                lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('empno','designation').order_by('designation'))
                                                if testmarkofficer != '':
                                                    testmarkofficer+=','
                                                testmarkofficer=testmarkofficer+"All DRM's/"+ii['parent_location_code']
                                                # testempno=set(testempno)
                                                # part=set(map(lambda d: d['partno'], part))
                                                interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                                testempno=list(map(lambda d: d['empno'], lst2))
                                                testdesig=list(map(lambda d: d['designation'], lst2))
                                                lstdict.append({"desig":"All DRM's/"+ii['parent_location_code'],"empno":list(interkey)})


                        
                        for i in range(len(testdesig)):
                            if testmarkofficer != '':
                                testmarkofficer+=','
                            testmarkofficer=testmarkofficer+testdesig[i]
                            lstdict.append({"desig":testdesig[i],"empno":[testempno[i]]})

                    
                    mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': testmarkofficer,'custom_key':json.dumps(lstdict)})

                    #################################  end      #############################

                    
                    
                    j.update({'mrkoffi': mrkoffi})
                    # print('mmmmmmmm', desig_longdesc1)
                elif j['type'] == 'H':
                    mark=m1.Marked_Officers.objects.filter(item_no=j['item_no'])

                    if mark.exists():
                        if mark[0].marked_to is not None: 
                            print('---------', j['item_no'])
                            # mrkoffi = {}
                            desig_longdesc1 =''
                            marked_officers1 = ''
                            for x in mark.values():
                                # print('xxxxxxxxx', x['myuser_id_id'])
                                
                                # marked=m1.empmast.objects.filter(myuser_id=x['myuser_id_id'])
                            
                                # des = models.Level_Desig.objects.filter(empno_id=marked[0].empno)
                                # desig_longdesc1 += des[0].designation+','
                                # print(des)
                            
                                # marked_officers1 += marked[0].empno+','

                                des = models.Level_Desig.objects.filter(designation_code=x['marked_to_id'])
                                desig_longdesc1 += des[0].designation+','
                                marked_officers1 += des[0].empno_id+','

                            print('kkkkkkkkkkkkkkk', desig_longdesc1)

                            if marked_officers1 != '':
                                testdesig=desig_longdesc1.split(',')
                                testempno=marked_officers1.split(',')
                                testdesig.pop()
                                testempno.pop()
                                testmarkofficer=''
                                lstdict=[]
                                alldesig = models.Level_Desig.objects.filter(empno__in=testempno).values('d_level').distinct('d_level')
                                
                                for i in alldesig:
                                    if i['d_level'] == 'GM':
                                        lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(empno__in=testempno).count()
                                        if lst1 == 0:
                                            lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level']).values('empno','designation').order_by('designation'))
                                            if testmarkofficer != '':
                                                testmarkofficer+=','
                                            testmarkofficer=testmarkofficer+"All GM's/ZR"
                                            # testempno=set(testempno)
                                            # part=set(map(lambda d: d['partno'], part))
                                            interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                            testempno=list(map(lambda d: d['empno'], lst2))
                                            testdesig=list(map(lambda d: d['designation'], lst2))
                                            lstdict.append({"desig":"All GM's/ZR","empno":list(interkey)})

                                    elif i['d_level'] == 'BM':
                                        lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(empno__in=testempno).count()
                                        if lst1 == 0:
                                            lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level']).values('empno','designation').order_by('designation'))
                                            if testmarkofficer != '':
                                                testmarkofficer+=','
                                            testmarkofficer=testmarkofficer+"All Board Member's"
                                            # testempno=set(testempno)
                                            # part=set(map(lambda d: d['partno'], part))
                                            interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                            testempno=list(map(lambda d: d['empno'], lst2))
                                            testdesig=list(map(lambda d: d['designation'], lst2))
                                            lstdict.append({"desig":"All Board Member's","empno":list(interkey)})


                                    elif i['d_level'] == 'PHOD':
                                        lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(empno__in=testempno).count()
                                        if lst1 == 0:
                                            lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level']).values('empno','designation').order_by('designation'))
                                            if testmarkofficer != '':
                                                testmarkofficer+=','
                                            testmarkofficer=testmarkofficer+"All PHOD's"
                                            # testempno=set(testempno)
                                            # part=set(map(lambda d: d['partno'], part))
                                            interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                            testempno=list(map(lambda d: d['empno'], lst2))
                                            testdesig=list(map(lambda d: d['designation'], lst2))
                                            lstdict.append({"desig":"All PHOD's","empno":list(interkey)})
                                        else:
                                            hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
                                            for ii in hq:
                                                rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
                                                if models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exists():
                                                    lst3=models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exclude(empno__in=testempno).count()
                                                    if lst3 == 0:
                                                        lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('empno','designation').order_by('designation'))
                                                        if testmarkofficer != '':
                                                            testmarkofficer+=','
                                                        testmarkofficer=testmarkofficer+"All PHOD's"+ii['parent_location_code']
                                                        # testempno=set(testempno)
                                                        # part=set(map(lambda d: d['partno'], part))
                                                        interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                                        testempno=list(map(lambda d: d['empno'], lst2))
                                                        testdesig=list(map(lambda d: d['designation'], lst2))
                                                        lstdict.append({"desig":"All PHOD's/"+ii['parent_location_code'],"empno":list(interkey)})



                                    elif i['d_level'] == 'DRM':
                                        lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(empno__in=testempno).count()
                                        if lst1 == 0:
                                            lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level']).values('empno','designation').order_by('designation'))
                                            if testmarkofficer != '':
                                                testmarkofficer+=','
                                            testmarkofficer=testmarkofficer+"All DRM's"
                                            # testempno=set(testempno)
                                            # part=set(map(lambda d: d['partno'], part))
                                            interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                            testempno=list(map(lambda d: d['empno'], lst2))
                                            testdesig=list(map(lambda d: d['designation'], lst2))
                                            lstdict.append({"desig":"All DRM's","empno":list(interkey)})
                                        else:
                                            hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
                                            for ii in hq:
                                                rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
                                                if models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exists():
                                                    lst3=models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exclude(empno__in=testempno).count()
                                                    if lst3 == 0:
                                                        lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('empno','designation').order_by('designation'))
                                                        if testmarkofficer != '':
                                                            testmarkofficer+=','
                                                        testmarkofficer=testmarkofficer+"All DRM's/"+ii['parent_location_code']
                                                        # testempno=set(testempno)
                                                        # part=set(map(lambda d: d['partno'], part))
                                                        interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                                        testempno=list(map(lambda d: d['empno'], lst2))
                                                        testdesig=list(map(lambda d: d['designation'], lst2))
                                                        lstdict.append({"desig":"All DRM's/"+ii['parent_location_code'],"empno":list(interkey)})


                                
                                for i in range(len(testdesig)):
                                    if testmarkofficer != '':
                                        testmarkofficer+=','
                                    testmarkofficer=testmarkofficer+testdesig[i]
                                    lstdict.append({"desig":testdesig[i],"empno":[testempno[i]]})

                    
                            mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': testmarkofficer,'custom_key':json.dumps(lstdict)})
                            

                            #################################  end      #############################

                            
                            
                            j.update({'mrkoffi': mrkoffi, 'chk_cts':'YES'})
                        else:
                            j.update({'mrkoffi': '', 'chk_cts':'YES'})
                    else:

                        j.update({'chk_cts':'NO'})
                ins_detail[0].update({'item_details1': item_details1})
                # print('00000000', ins_detail)
                print('00000000', ins_detail)
            

                print('rrrrrrrrrrrrrrr', item_id)
            context={
                
                'ins_detail':ins_detail,
                'item_id': item_id,
                'length_of_h': length,
                'sh_list': sh,
                'ssh_list': ssh,
                'multi_loc': multi_loc,
                'Zone':list2 ,
                'division':list4,
                'department':list6,
                'new_mail_detail': new_mail_detail,
                'alldesig':alldesig1,
                'desg_no':desg_no,
                
                }  
            
            return render(request,"edit_inspection_form.html",context)
        elif item_type == 'Chk':
            #visnu code
            ins_detail=list(m1.Inspection_details.objects.filter(inspection_no=ins_id, item_type='Chk').values('zone','division','dept','location','inspected_on','inspection_title'))
            item_details1= list(m1.Item_details.objects.filter(inspection_no_id=ins_id, inspection_no__item_type='Chk').values('observation').order_by('item_no'))
            #visnu code
            
             
            empdata=m1.empmast.objects.filter(myuser_id=request.user).values('empname','empno', 'desig_longdesc')
            desig_longdesc = empdata[0]['desig_longdesc']
            
            # print('ttttttttttttttttttttttttttttttttttttttttttttttttttttttt', desig_longdesc)
            
            list1=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
            list2=[]
            for i in list1:
                # print(i['location_code'],'_________')
                list2.append(i['location_code'])
            list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
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
            
        
            context={
                'Zone':list2 ,
                'division':list4,
                'marked_to':list5,
                'department':list6,
                'desig': desig_longdesc,
                'ins_detail':ins_detail,
                'item_details1':item_details1
            
                }
                
            return render(request, 'search_checklist_template_report.html',context)
            
        else:
            messages.error(request, 'oops error')
    else:     
        return render(request,"create_inspection_form.html", context)

    # except Exception as e:
    #     print("e==",e) 



def autoFetchLocation(request):
    if request.method == 'GET' and request.is_ajax():
        last_val = request.GET.get('last_val')
        # list1=list(models.locationMaster.objects.values_list('city', flat=True).order_by('city').distinct('city'))

        # list1=list(models.locationMaster.objects.filter(city__istartswith=last_val).values('city','pincode').order_by('city').distinct('city'))
        # print(list1)
        list1 = []
        list_obj = models.station_master.objects.filter(station_name__istartswith=last_val).values('station_name').order_by('station_name').distinct('station_name')
        for i in list_obj:
            list1.append({'city': i['station_name']})
        return JsonResponse(list1, safe=False)
    return JsonResponse({'success': False})



    # except Exception as e:
    #     print("e==",e) 



def autoFetchLocation(request):
    if request.method == 'GET' and request.is_ajax():
        last_val = request.GET.get('last_val')
        # list1=list(models.locationMaster.objects.values_list('city', flat=True).order_by('city').distinct('city'))

        # list1=list(models.locationMaster.objects.filter(city__istartswith=last_val).values('city','pincode').order_by('city').distinct('city'))
        # print(list1)
        list1 = []
        list_obj = models.station_master.objects.filter(station_name__istartswith=last_val).values('station_name').order_by('station_name').distinct('station_name')
        for i in list_obj:
            list1.append({'city': i['station_name']})
        return JsonResponse(list1, safe=False)
    return JsonResponse({'success': False})


def update_draft_data(request):
    if request.method == "POST" and request.is_ajax():
        from datetime import datetime
        final=request.POST.get('final_partinspected')
        final_id=request.POST.get('id_partinspected')

        rly=json.loads(request.POST.get('zone'))
        div=json.loads(request.POST.get('division'))
        dept=json.loads(request.POST.get('department'))
        loc=json.loads(request.POST.get('location'))

        insdt=request.POST.get('txtDate2')
        print(insdt, '-----------')
        if 'to' in insdt:
            dt = insdt.split('to')
            st_date = dt[0].strip()
            en_date = dt[1].strip()

            start_date = datetime.strptime(st_date, '%d/%m/%Y').strftime('%Y-%m-%d')
            inspected_on = datetime.strptime(en_date, '%d/%m/%Y').strftime('%Y-%m-%d')

        else:
            
            inspected_on = datetime.strptime(insdt, '%d/%m/%Y').strftime('%Y-%m-%d')
            start_date = datetime.strptime(insdt, '%d/%m/%Y').strftime('%Y-%m-%d')
        
        title=request.POST.get('titleinsp')
        inspection_no=request.POST.get('inspection_no')
        btnValues=request.POST.get('buttonValues')
        send_to=request.POST.get('send_to')
        send_desig=request.POST.get('send_desig')
        
        
        
        finalval = json.loads(final)
        final_allid = json.loads(final_id)
        # empno=models.Level_Desig.objects.filter(official_email_ID=request.user)
        empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation

        else:
            messages.error(request,'You are not authorize to create inspection.Please contact to admin')

        # ddesig=models.Level_Desig.objects.get(empno=empno)

        if btnValues == 'Save as draft':
            m1.Inspection_details.objects.filter(inspection_no=inspection_no).update(inspection_title=title,status_flag=0, modified_by=empno,modified_on=datetime.now(), start_date=start_date, inspected_on=inspected_on)
            
            for rl in rly:
                rly_d = m1.Insp_multi_location.objects.filter(inspection_no_id=inspection_no,item=rl,  type='HQ')
                if not rly_d.exists():
                    
                    m1.Insp_multi_location.objects.create(inspection_no_id=inspection_no, item=rl, type='HQ')
                
            for di in div:
                div_d = m1.Insp_multi_location.objects.filter(inspection_no_id=inspection_no,item=di,  type='DIV')
                if not div_d.exists():
                    
                    m1.Insp_multi_location.objects.create(inspection_no_id=inspection_no,item=di, type='DIV')
            for dp in dept:
                dept_d = m1.Insp_multi_location.objects.filter(inspection_no_id=inspection_no,item=dp,type='DPT')
                if not dept_d.exists():
                    
                    m1.Insp_multi_location.objects.create(inspection_no_id=inspection_no,item=dp,type='DPT')
            for lo in loc:
                loc_d = m1.Insp_multi_location.objects.filter(inspection_no_id=inspection_no, item=lo, type='LOC')
                if not loc_d.exists():
                    
                    m1.Insp_multi_location.objects.create(inspection_no_id=inspection_no,item=lo, type='LOC')

            inspectionid = m1.Item_details.objects.filter(inspection_no_id=inspection_no)
            if inspectionid.exists():
                m1.Item_details.objects.filter(inspection_no_id=inspection_no).delete()
                for f, b in zip(finalval, final_allid):
                    print(finalval[f], final_allid[b])
                    for x,y in zip(finalval[f], final_allid[b]):
                        s = y.split('.')
                        if len(s) == 1:
                            hed = 'heading'+y
                            heading = finalval[f][hed]
                            m1.Item_details.objects.create(item_title=heading, status_flag=0,created_on=datetime.now(),modified_on=datetime.now(), type='H',des_id=y, inspection_no_id=inspection_no)
                            y2=str(y+'.1')
                            if y2 in final_allid[b]:
                                print('if',y2)
                                pass
                            else:
                                print('else',y2)
                                trz = 'targetdate'+y
                                officm = 'markeofficer'+y
                                chk = 'check'+y
                                
                                targetd = finalval[f][trz]
                                markof = finalval[f][officm]
                                markeofficer = markof.split(',')
                                checkbox = finalval[f][chk]
                                if checkbox == '1':
                                    checkbox = 1
                                elif checkbox== '0':
                                    checkbox = 0


                                if targetd:
                                    t_date = datetime.strptime(targetd, '%d/%m/%Y').strftime('%Y-%m-%d')
                                else:
                                    t_date = None
                                m1.Item_details.objects.filter(item_title=heading,status_flag=0, type='H',des_id=y, inspection_no_id=inspection_no).update(target_date=t_date, priority=checkbox)
                                print('00000000000000000000000', t_date)
                                item_id=m1.Item_details.objects.all().last().item_no
                                #mark officer 
                                officer_email=[]
                                if markof:
                                    for i in markeofficer:
                                        # myuser_id=m1.empmast.objects.filter(empno=i)[0].myuser_id_id
                                        # desig_longdesc=m1.empmast.objects.filter(empno=i)[0].desig_longdesc
                                        # print('uuuuuuuuuuuuuuuuuu', desig_longdesc)
                                        Desig=models.Level_Desig.objects.filter(empno=i)
                                        
                                        
                                        
                                        email = m1.empmast.objects.filter(empno=i)[0].email
                                        officer_email.append(email)

                                        

                                        if Desig:
                                            Desig=Desig[0].designation_code
                                            if m1.Marked_Officers.objects.all().last():
                                                marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                                            else:
                                                marked_no_id = 1
                                            m1.Marked_Officers.objects.create(created_on=datetime.now(),created_by=empno,marked_emp=i,marked_no=marked_no_id,status_flag=0,item_no_id=item_id,marked_to_id=int(Desig))
                                        else:
                                            messages.info(request, 'Employ Desig not Match in Designation Master')
                                else:
                                    if m1.Marked_Officers.objects.all().last():
                                        marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                                    else:
                                        marked_no_id = 1
                                    m1.Marked_Officers.objects.create(created_on=datetime.now(),created_by=empno,marked_no=marked_no_id,status_flag=0,item_no_id=item_id)

                        elif len(s) == 2:
                            ob = 'observation'+y
                            trz = 'targetdate'+y
                            officm = 'markeofficer'+y

                            chk = 'check'+y

                            observation = finalval[f][ob]
                            targetd = finalval[f][trz]
                            markof = finalval[f][officm]
                            checkbox = finalval[f][chk]

                            if checkbox == '1':
                                checkbox = 1
                            elif checkbox == '0':
                                checkbox = 0
                            
                            markeofficer = markof.split(',')
                            if targetd:

                                targetdate = datetime.strptime(targetd, '%d/%m/%Y').strftime('%Y-%m-%d')
                            else:
                                targetdate = None
                            print(observation)
                            m1.Item_details.objects.create(observation=observation,priority=checkbox,status_flag=0,modified_on=datetime.now(), created_on=datetime.now(),inspection_no_id=inspection_no, des_id=y, target_date=targetdate, type='SH')
                            
                            item_id=m1.Item_details.objects.all().last().item_no
                            if markof:
                                #mark officer
                                
                                for i in markeofficer:
                                    print('iiiiiiiiiiiiiiiiii', i)
                                    if i != '':
                                        # myuser_id=m1.empmast.objects.filter(empno=i)[0].myuser_id_id
                                        # desig_longdesc=m1.empmast.objects.filter(empno=i)[0].desig_longdesc
                                        # print('eeeeeeeeeeeeeee', desig_longdesc)
                                        Desig=models.Level_Desig.objects.filter(empno=i)
                                        if Desig:
                                            Desig=Desig[0].designation_code
                                            if m1.Marked_Officers.objects.all().last():
                                                marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                                            else:
                                                marked_no_id = 1
                                            m1.Marked_Officers.objects.create(created_on=datetime.now(),created_by=empno,marked_no=marked_no_id,status_flag=0,item_no_id=item_id,marked_to_id=int(Desig))
                                        else:
                                            messages.info(request, 'Employ Desig not Match in Level Desig')
                                    else:
                                        pass
                            else:
                                markeofficer=''
                        
                        else:
                            subdes = 'subdes'+y
                            subdes1 = finalval[f][subdes]
                            m1.Item_details.objects.create(item_subtitle=subdes1,status_flag=0,modified_on=datetime.now(), created_on=datetime.now(),type='SSH',des_id=y, inspection_no_id=inspection_no)
            else:
                for f, b in zip(finalval, final_allid):
                    print(finalval[f], final_allid[b])
                    for x,y in zip(finalval[f], final_allid[b]):
                        s = y.split('.')
                        if len(s) == 1:
                            hed = 'heading'+y
                            heading = finalval[f][hed]
                            m1.Item_details.objects.create(item_title=heading,status_flag=0, modified_on=datetime.now(),created_on=datetime.now(),type='H',des_id=y, inspection_no_id=inspection_no)
                        elif len(s) == 2:
                            ob = 'observation'+y
                            trz = 'targetdate'+y
                            officm = 'markeofficer'+y
                            chk = 'check'+y
                            observation = finalval[f][ob]
                            targetd = finalval[f][trz]
                            markof = finalval[f][officm]

                            checkbox = finalval[f][chk]

                            if checkbox == '1':
                                checkbox = 1
                            elif checkbox == '0':
                                checkbox = 0
                            
                            markeofficer = markof.split(',')
                            if targetd:

                                targetdate = datetime.strptime(targetd, '%d/%m/%Y').strftime('%Y-%m-%d')
                            else:
                                targetdate = None
                            print(observation)
                            m1.Item_details.objects.create(observation=observation,priority=checkbox,modified_on=datetime.now(),created_on=datetime.now(),status_flag=0, inspection_no_id=inspection_no, des_id=y, target_date=targetdate, type='SH')
                            
                            item_id=m1.Item_details.objects.all().last().item_no
                            if markof:
                                #mark officer
                                
                                for i in markeofficer:
                                    print('iiiiiiiiiiiiiiiiii', i)
                                    if i != '':
                                        # myuser_id=m1.empmast.objects.filter(empno=i)[0].myuser_id_id
                                        # desig_longdesc=m1.empmast.objects.filter(empno=i)[0].desig_longdesc
                                        # print('eeeeeeeeeeeeeee', desig_longdesc)
                                        Desig=models.Level_Desig.objects.filter(empno=i)
                                        if Desig:
                                            Desig=Desig[0].designation_code
                                            if m1.Marked_Officers.objects.all().last():
                                                marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                                            else:
                                                marked_no_id = 1
                                            m1.Marked_Officers.objects.create(created_on=datetime.now(),created_by=empno,marked_no=marked_no_id,marked_emp=i, status_flag=1, item_no_id=item_id,marked_to_id=int(Desig))
                                        else:
                                            print('error')
                                            
                                    else:
                                        pass
                            else:
                                markeofficer=''
                        
                        else:
                            subdes = 'subdes'+y
                            subdes1 = finalval[f][subdes]
                            m1.Item_details.objects.create(item_subtitle=subdes1,modified_on=datetime.now(), created_on=datetime.now(), status_flag=0, type='SSH',des_id=y, inspection_no_id=inspection_no)
            return JsonResponse({"status": "Record Saved as Draft." })
        elif btnValues=='Submit':
            #657777
            m1.Inspection_details.objects.filter(inspection_no=inspection_no)
            

            for rl in rly:
                rly_d = m1.Insp_multi_location.objects.filter(inspection_no_id=inspection_no,item=rl,  type='HQ')
                if not rly_d.exists():
                    
                    m1.Insp_multi_location.objects.create(inspection_no_id=inspection_no, item=rl, type='HQ')
                
            for di in div:
                div_d = m1.Insp_multi_location.objects.filter(inspection_no_id=inspection_no,item=di,  type='DIV')
                if not div_d.exists():
                    
                    m1.Insp_multi_location.objects.create(inspection_no_id=inspection_no,item=di, type='DIV')
            for dp in dept:
                dept_d = m1.Insp_multi_location.objects.filter(inspection_no_id=inspection_no,item=dp,type='DPT')
                if not dept_d.exists():
                    
                    m1.Insp_multi_location.objects.create(inspection_no_id=inspection_no,item=dp,type='DPT')
            for lo in loc:
                loc_d = m1.Insp_multi_location.objects.filter(inspection_no_id=inspection_no, item=lo, type='LOC')
                if not loc_d.exists():
                    
                    m1.Insp_multi_location.objects.create(inspection_no_id=inspection_no,item=lo, type='LOC')

            year = str(datetime.now().year)
            # desig = m1.empmast.objects.get(myuser_id=request.user).desig_longdesc
            if desig:
                last_note = m1.Inspection_details.objects.filter(inspection_no=inspection_no)[0].inspection_note_no
                if last_note ==''or last_note == None:
                    # _note = m1.Inspection_details.objects.filter(inspection_note_no__contains='Insp', inspection_note_no__isnull=False).order_by('-inspection_note_no')[0]
                    note_ = year+'/'+desig+'/Insp'+'/'
                    _note_no = m1.Inspection_details.objects.filter(inspection_note_no__istartswith=note_, insp_last__isnull=False).aggregate(Max('insp_last'))
                    print('+++++++++++++', _note_no)
                    if _note_no['insp_last__max'] is not None:
                    
                        x = _note_no['insp_last__max']
                        insp = int(x)+1
                        note_no = year+'/'+desig+'/Insp'+'/'+ str(insp)
                    else:
                        insp = 1
                        note_no = year+'/'+desig+'/Insp'+'/'+ str(insp)

                    
                # last_note1 = m1.Inspection_details.objects.filter(inspection_note_no__istartswith=note_).aggregate(Max('insp_last'))['insp_last__max']
                # last_note1 = m1.Inspection_details.objects.filter(inspection_note_no__istartswith=note_).values('insp_last')
                
                # # print('last_note1', last_note1)
                
                # if len(last_note1) == 0:
                #     last_note1 = 1
                #     note_no = year+'/'+desig+'/Insp'+'/'+ str(last_note1)
                    
                # else:
                #     last_note1 = int(last_note1[0]['insp_last']) +1
                #     note_no = year+'/'+desig+'/Insp'+'/'+ str(last_note1)
                    
                    
                    m1.Inspection_details.objects.filter(inspection_no=inspection_no).update(inspection_note_no=str(note_no), insp_last=insp)
                    messages.info(request, f'Inspection note successfully saved with Inspection Note No: {note_no}')
            else:
                print('insert desig')

            m1.Inspection_details.objects.filter(inspection_no=inspection_no).update(inspection_title=title,modified_by=empno, status_flag=1, start_date=start_date, inspected_on=inspected_on)
            inspectionid = m1.Item_details.objects.filter(inspection_no_id=inspection_no)
            
            officer_email=[]
            if inspectionid.exists():
                m1.Item_details.objects.filter(inspection_no_id=inspection_no).delete()
                
                for f, b in zip(finalval, final_allid):
                    print(finalval[f], final_allid[b])
                    for x,y in zip(finalval[f], final_allid[b]):
                        s = y.split('.')
                        if len(s) == 1:
                            hed = 'heading'+y
                            heading = finalval[f][hed]
                            m1.Item_details.objects.create(item_title=heading,created_on=datetime.now(), status_flag=1,type='H',des_id=y, inspection_no_id=inspection_no)
                            
                            y2=str(y+'.1')
                            if y2 in final_allid[b]:
                                print('if',y2)
                                pass
                            else:
                                print('else',y2)
                                trz = 'targetdate'+y
                                officm = 'markeofficer'+y
                                chk =  'check'+y
                                
                                targetd = finalval[f][trz]
                                markof = finalval[f][officm]
                                checkbox = finalval[f][chk]
                                if checkbox == '1':
                                    checkbox = 1
                                elif checkbox == '0':
                                    checkbox = 0
                                

                                markeofficer = markof.split(',')
                                if targetd:
                                    t_date = datetime.strptime(targetd, '%d/%m/%Y').strftime('%Y-%m-%d')
                                else:
                                    t_date = None
                                
                                m1.Item_details.objects.filter(item_title=heading, status_flag=1, type='H',des_id=y, inspection_no_id=inspection_no).update(modified_on=datetime.now(),priority=checkbox, target_date=t_date)
                                item_id=m1.Item_details.objects.all().last().item_no
                                #mark officer
                                
                                if markof:
                                    for i in markeofficer:
                                        # myuser_id=m1.empmast.objects.filter(empno=i)[0].myuser_id_id
                                        # desig_longdesc=m1.empmast.objects.filter(empno=i)[0].desig_longdesc
                                        # print('uuuuuuuuuuuuuuuuuu', desig_longdesc)
                                        Desig=models.Level_Desig.objects.filter(empno=i)
                                        email = m1.empmast.objects.filter(empno=i)[0].email
                                        officer_email.append(email)

                                        

                                        if Desig:
                                            Desig=Desig[0].designation_code
                                            if m1.Marked_Officers.objects.all().last():
                                                marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                                            else:
                                                marked_no_id = 1
                                            m1.Marked_Officers.objects.create(created_on=datetime.now(),created_by=empno,marked_emp=i,marked_no=marked_no_id,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig))
                                        else:
                                            print('error')
                                            # messages.info(request, 'error')

                        elif len(s) == 2:
                            ob = 'observation'+y
                            trz = 'targetdate'+y
                            officm = 'markeofficer'+y
                            chk =  'check'+y
                            observation = finalval[f][ob]
                            targetd = finalval[f][trz]
                            markof = finalval[f][officm]

                            checkbox = finalval[f][chk]
                            if checkbox == '1':
                                checkbox = 1
                            elif checkbox == '0':
                                checkbox = 0
                            
                            markeofficer = markof.split(',')
                            if targetd:
                                targetdate = datetime.strptime(targetd, '%d/%m/%Y').strftime('%Y-%m-%d')
                            else:
                                targetdate = None
                            print(observation)
                            m1.Item_details.objects.create(observation=observation,priority=checkbox,created_on=datetime.now(),status_flag=1,inspection_no_id=inspection_no, des_id=y, target_date=targetdate, type='SH')
                            
                            item_id=m1.Item_details.objects.all().last().item_no
                            if markof:
                                #mark officer
                                
                                for i in markeofficer:
                                    print('iiiiiiiiiiiiiiiiii', i)
                                    if i != '':
                                        # myuser_id=m1.empmast.objects.filter(empno=i)[0].myuser_id_id
                                        # desig_longdesc=m1.empmast.objects.filter(empno=i)[0].desig_longdesc
                                        # print('eeeeeeeeeeeeeee', desig_longdesc)
                                        
                                        Desig=models.Level_Desig.objects.filter(empno=i)
                                        email = m1.empmast.objects.filter(empno=i)[0].email
                                        officer_email.append(email)
                                        if Desig:
                                            Desig=Desig[0].designation_code
                                            if m1.Marked_Officers.objects.all().last():
                                                marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                                            else:
                                                marked_no_id = 1
                                            m1.Marked_Officers.objects.create(marked_no=marked_no_id,marked_emp=i,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig))
                                        else:
                                            print('error1')
                                            # messages.info(request, 'error')
                                    else:
                                        pass
                            else:
                                markeofficer=''
                        
                        else:
                            subdes = 'subdes'+y
                            subdes1 = finalval[f][subdes]
                            m1.Item_details.objects.create(item_subtitle=subdes1,status_flag=1,created_on=datetime.now(), type='SSH',des_id=y, inspection_no_id=inspection_no)
            else:
                
                for f, b in zip(finalval, final_allid):
                    print(finalval[f], final_allid[b])
                    for x,y in zip(finalval[f], final_allid[b]):
                        s = y.split('.')
                        if len(s) == 1:
                            hed = 'heading'+y
                            heading = finalval[f][hed]
                            m1.Item_details.objects.create(item_title=heading,created_on=datetime.now(), status_flag=1, type='H',des_id=y, inspection_no_id=inspection_no)
                        elif len(s) == 2:
                            ob = 'observation'+y
                            trz = 'targetdate'+y
                            officm = 'markeofficer'+y
                            chk =  'check'+y

                            observation = finalval[f][ob]
                            targetd = finalval[f][trz]
                            markof = finalval[f][officm]

                            checkbox = finalval[f][chk]
                            if checkbox == '1':
                                checkbox = 1
                            elif checkbox == '0':
                                checkbox = 0
                            
                            markeofficer = markof.split(',')
                            if targetd:
                                targetdate = datetime.strptime(targetd, '%d/%m/%Y').strftime('%Y-%m-%d')
                            else:
                                targetdate = None
                            print(observation)
                            m1.Item_details.objects.create(observation=observation,priority=checkbox,created_on=datetime.now(), status_flag=1,inspection_no_id=inspection_no, des_id=y, target_date=targetdate, type='SH')
                            
                            item_id=m1.Item_details.objects.all().last().item_no
                            
                            if markof:
                                #mark officer
                                
                                for i in markeofficer:
                                    print('iiiiiiiiiiiiiiiiii', i)
                                    if i != '':
                                        # myuser_id=m1.empmast.objects.filter(empno=i)[0].myuser_id_id
                                        # desig_longdesc=m1.empmast.objects.filter(empno=i)[0].desig_longdesc
                                        # print('eeeeeeeeeeeeeee', desig_longdesc)
                                        Desig=models.Level_Desig.objects.filter(empno=i)

                                        email = m1.empmast.objects.filter(empno=i)[0].email
                                        officer_email.append(email)
                                        
                                        if Desig:
                                            Desig=Desig[0].designation_code
                                            if m1.Marked_Officers.objects.all().last():
                                                marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                                            else:
                                                marked_no_id = 1
                                            m1.Marked_Officers.objects.create(created_on=datetime.now(),created_by=empno,marked_no=marked_no_id,marked_emp=i, item_no_id=item_id,marked_to_id=int(Desig))
                                        else:
                                            messages.info(request, 'Employ Desig not Match in Level Desig')
                                    else:
                                        pass
                            else:
                                markeofficer=''

                            
                        
                        else:
                            subdes = 'subdes'+y
                            subdes1 = finalval[f][subdes]
                            m1.Item_details.objects.create(item_subtitle=subdes1,created_on=datetime.now(), status_flag=1, type='SSH',des_id=y, inspection_no_id=inspection_no)
            
            # try:
            To = officer_email
            subject="Inspection report"
            # To=['ecegcttarun@gmail.com','kr.abhijeet6235@gmail.com']
            context = {'title': title}
                
            InspSendMail(subject, To, context)

            m1.Insp_mail_details.objects.create(subject=subject, body=title,area='Mark Of', inspection_no_id=inspection_no, send_to=send_to,send_desig=send_desig)
            messages.success(request, 'Email has been sent')
            
            # except:
            #     messages.error(request, 'Email send failed.') 
            
            
            
            try:
                offic_mail =[]
                if send_to:
                    emil = send_to.split(',')
                    for i in emil:
                        email = m1.empmast.objects.filter(empno=i)[0].email
                        offic_mail.append(email)

                    subject="Inspection report"
                    To = offic_mail
                    # To=['ecegcttarun@gmail.com','kr.abhijeet6235@gmail.com']
                    context = {'title': title}
                        
                    InspSendMail(subject, To, context)
                    m1.Insp_mail_details.objects.create(subject=subject, body=title, area='Copy To', inspection_no_id=inspection_no, send_to=send_to,send_desig=send_desig)
                    messages.success(request, 'Email has been sent')
                
            except:
                
                messages.error(request, 'Email send failed.') 
            
            
            return JsonResponse({"status": "Record Saved" })
        else:
            return JsonResponse({"status": "Error" })
    return JsonResponse({"success":False}, status=400)
    # except Exception as e:
    #     print("e==",e)  
    #     return render(request, "commonerrorpage.html", {})


def save_draft_data(request):
    if request.method == "POST" and request.is_ajax():
        from datetime import datetime
        final=request.POST.get('final_partinspected')
        final_id=request.POST.get('id_partinspected')
        rly=json.loads(request.POST.get('zone'))
        div=json.loads(request.POST.get('division'))
        dept=json.loads(request.POST.get('department'))
        loc=json.loads(request.POST.get('location'))

        send_to=request.POST.get('send_to')
        send_desig=request.POST.get('send_desig')

        
        insdt=request.POST.get('txtDate2')
        print(insdt, '------777-----')

        if 'to' in insdt:
            dt = insdt.split('to')
            st_date = dt[0].strip()
            en_date = dt[1].strip()

            start_date = datetime.strptime(st_date, '%d/%m/%Y').strftime('%Y-%m-%d')
            inspected_on = datetime.strptime(en_date, '%d/%m/%Y').strftime('%Y-%m-%d')

        else:
            
            inspected_on = datetime.strptime(insdt, '%d/%m/%Y').strftime('%Y-%m-%d')
            start_date = datetime.strptime(insdt, '%d/%m/%Y').strftime('%Y-%m-%d')
       
        title=request.POST.get('titleinsp')

        finalval = json.loads(final)
        final_allid = json.loads(final_id)

        
        

        # empno=models.Level_Desig.objects.filter(official_email_ID=request.user)
        empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
        print('==============', len(empnox[0].empno_id))
        if empnox:
            empno = empnox[0].empno_id
            ddesig = empnox[0].designation_code

        else:
            messages.error(request, 'You are not authorize to create inspection. Please contact to admin')
        
        # ddesig=models.Level_Desig.objects.get(empno=empno)
     
        m1.Inspection_details.objects.create(inspection_title=title,item_type='Insp', created_on=datetime.now(), inspection_officer_id=ddesig, status_flag=0,modified_by=empno, created_by=empno,start_date=start_date,inspected_on=inspected_on)
        inspection_id=m1.Inspection_details.objects.all().last().inspection_no


        m1.Insp_mail_details.objects.create(area='Copy To', inspection_no_id=inspection_id, send_to=send_to,send_desig=send_desig)


        for rl in rly:
            m1.Insp_multi_location.objects.create(inspection_no_id=inspection_id, item=rl, type='HQ')
        for di in div:
            m1.Insp_multi_location.objects.create(inspection_no_id=inspection_id, item=di, type='DIV')
        for dp in dept:
            m1.Insp_multi_location.objects.create(inspection_no_id=inspection_id, item=dp, type='DPT')
        for lo in loc:
            m1.Insp_multi_location.objects.create(inspection_no_id=inspection_id, item=lo, type='LOC')


        for f, b in zip(finalval, final_allid):
            print(finalval[f], final_allid[b])
            for x,y in zip(finalval[f], final_allid[b]):
                s = y.split('.')
                if len(s) == 1:
                    hed = 'heading'+y
                    heading = finalval[f][hed]
                    m1.Item_details.objects.create(item_title=heading,status_flag=0,created_by=empno, created_on=datetime.now(), type='H',des_id=y, inspection_no_id=inspection_id)

                    y2=str(y+'.1')
                    if y2 in final_allid[b]:
                        print('if',y2)
                        pass
                    else:
                        print('else',y2)
                        trz = 'targetdate'+y
                        officm = 'markeofficer'+y
                        chk = 'check'+y
                        
                        targetd = finalval[f][trz]
                        markof = finalval[f][officm]
                        markeofficer = markof.split(',')
                        checkbox = finalval[f][chk]

                        if checkbox == '1':
                            checkbox = 1
                        elif checkbox== '0':
                            checkbox = 0


                        if targetd:
                            t_date = datetime.strptime(targetd, '%d/%m/%Y').strftime('%Y-%m-%d')
                        else:
                            t_date = None
                        m1.Item_details.objects.filter(item_title=heading,status_flag=0, type='H',des_id=y, inspection_no_id=inspection_id).update(target_date=t_date, priority=checkbox)
                        print('00000000000000000000000', t_date)
                        item_id=m1.Item_details.objects.all().last().item_no
                        #mark officer 
                        officer_email=[]
                        if markof:
                            for i in markeofficer:
                                # myuser_id=m1.empmast.objects.filter(empno=i)[0].myuser_id_id
                                # desig_longdesc=m1.empmast.objects.filter(empno=i)[0].desig_longdesc
                                # print('uuuuuuuuuuuuuuuuuu', desig_longdesc)
                                Desig=models.Level_Desig.objects.filter(empno=i)
                                
                                
                                
                                email = m1.empmast.objects.filter(empno=i)[0].email
                                officer_email.append(email)

                                

                                if Desig:
                                    Desig=Desig[0].designation_code
                                    if m1.Marked_Officers.objects.all().last():
                                        marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                                    else:
                                        marked_no_id = 1
                                    m1.Marked_Officers.objects.create(created_on=datetime.now(),created_by=empno,marked_emp=i,marked_no=marked_no_id,status_flag=0,item_no_id=item_id,marked_to_id=int(Desig))
                                else:
                                    messages.info(request, 'Employ Desig not Match in Designation Master')
                        else:
                            if m1.Marked_Officers.objects.all().last():
                                marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                            else:
                                marked_no_id = 1
                            m1.Marked_Officers.objects.create(created_on=datetime.now(),created_by=empno,marked_no=marked_no_id,status_flag=0,item_no_id=item_id)

                elif len(s) == 2:
                    ob = 'observation'+y
                    trz = 'targetdate'+y
                    officm = 'markeofficer'+y
                    chk = 'check'+y

                    observation = finalval[f][ob]
                    targetd = finalval[f][trz]
                    markof = finalval[f][officm]
                    
                    checkbox = finalval[f][chk]

                    if checkbox == '1':
                        checkbox = 1
                    elif checkbox== '0':
                        checkbox = 0

                    markeofficer = markof.split(',')
                    
                    if targetd:
                        targetdate = datetime.strptime(targetd, '%d/%m/%Y').strftime('%Y-%m-%d')
                    else:
                        targetdate = None

                    m1.Item_details.objects.create(observation=observation,priority=checkbox, status_flag=0,created_by=empno,created_on=datetime.now(), inspection_no_id=inspection_id, des_id=y, target_date=targetdate, type='SH')
                    
                    item_id=m1.Item_details.objects.all().last().item_no
                    if markof:
                        #mark officer
                        for i in markeofficer:
                            # myuser_id=m1.empmast.objects.filter(empno=i)[0].myuser_id_id
                            # desig_longdesc=m1.empmast.objects.filter(empno=i)[0].desig_longdesc
                            # print('eeeeeeeeeeeeeee', desig_longdesc)
                            Desig=models.Level_Desig.objects.filter(empno=i)
                            if Desig:
                                Desig=Desig[0].designation_code
                                if m1.Marked_Officers.objects.all().last():
                                    marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                                else:
                                    marked_no_id = 1
                                m1.Marked_Officers.objects.create(created_on=datetime.now(),created_by=empno,marked_no=marked_no_id,marked_emp=i, status_flag=0,item_no_id=item_id,marked_to_id=int(Desig))
                            else:
                                print('error')
                    else:
                        markeofficer=''
                
                else:
                    subdes = 'subdes'+y
                    subdes1 = finalval[f][subdes]
                    m1.Item_details.objects.create(item_subtitle=subdes1,status_flag=0,created_by=empno,created_on=datetime.now(), type='SSH',des_id=y, inspection_no_id=inspection_id)

        return JsonResponse({"status": 1 })
    return JsonResponse({"success":False}, status=400)
    # except Exception as e:
    #     print("e==",e)  
    #     return render(request, "commonerrorpage.html", {})


def nominate_officer(request):
    try:
        print("$%^%*()&*^%")
        officers_list=list(m1.empmast.objects.all().values('empmname','empno', 'desig_longdesc'))
        print(officers_list)
        context={
            'officers_list':officers_list
        }
            
        return JsonResponse(context, safe = False)
    except Exception as e:
        print("e==",e)  
        


#bhartiend

# #niyati



# def employeeList(request):
#     current_user = request.user
#     emp=m1.empmast.objects.get(pk=current_user.username) 
#     employees=m1.empmast.objects.all().order_by('empname') 
#     category = m1.empmast.objects.filter(decode_paycategory__isnull=False).values('decode_paycategory').distinct()
#     department=models.departMast.objects.filter(delete_flag=False).values('department_name').order_by('department_name').distinct()
#     context={
#         'emp':emp,
#         'department':department,
#         'employees':employees,
#         'sub':0,
#         'category':category,
       
#         'user':usermaster,
        
#      }
#     return render(request, 'employeeList.html',context)


# def viewEmployee_Det(request):
    
#     if request.method == "GET" and request.is_ajax()
#         empno = request.GET.get('empno') 
#         emp = m1.empmast.objects.filter(empno=empno)[0]
#         print(empno,'empno')
#         context={  
#         'empno':emp.empno,
#         'empname':emp.empname,
#         'birthdate':emp.birthdate,
#         'dateapp':emp.appointmentdate,
#         'office_or':emp.office_orderno,
#         'sex':emp.sex,
#         'emp_inctype':emp.emp_inctype,
#         'marital_status':emp.marital_status,
#         'email':emp.email,
#         'contactno':emp.contactno,
#         'ticket_no':emp.ticket_no,
#         'idcard_no':emp.idcard_no,
#         'emp_inctype':emp.emp_inctype,
#         'inc_category':emp.inc_category,
#         'desig':emp.desig_longdesc,
#         'status':emp.emp_status,
#         'dept':emp.dept_desc,
#         'category':emp.decode_paycategory,
#         'payband':emp.payband,
#         'scalecode':emp.scalecode,
#         'paylevel':emp.pc7_level,
#         'gradepay':emp.payrate,
#         'date_of_joining':emp.date_of_joining,
#         'date_of_promotion':emp.date_of_promotion,
#         'station_dest':emp.station_des,
#         'wau':emp.wau,
#         'billunit':emp.billunit,
#         'service':emp.service_status,
#         'emptype':emp.emptype,
#         'medicalcode':emp.medicalcode,
#         'tradecode':emp.tradecode,
#         'role':emp.role,
#         'shop_section':emp.shop_section,

        
    
#         }  
    
    
#         return JsonResponse(context, safe = False)
#     return JsonResponse({"success":False}, status=400)


# def  get_emp_detNew(request):
#     if request.method == "GET" and request.is_ajax():
#         empno = request.GET.get('empno') 
#         obj = m1.empmast.objects.filter(empno=empno).all() 
#         rno=len(obj)
#         if rno==0:            
#            context={            
#             'rno':rno ,
#            }  
#         else:          
#            context={  
#             'rno':rno ,          
#             'empno':obj[0].empno,
#             'empname':obj[0].empname,
#             'birthdate':obj[0].birthdate,
#             'dateapp':obj[0].appointmentdate,
#             'office_orderno':obj[0].office_orderno,
#             'sex':obj[0].sex,
            
#             'marital_status':obj[0].marital_status,
#             'email':obj[0].email,
#             'contactno':obj[0].contactno,
            
#             'desig':obj[0].desig_longdesc,
#             'status':obj[0].emp_status,
#             'dept':obj[0].dept_desc,
#             'category':obj[0].decode_paycategory,
#             'payband':obj[0].payband,
#             'scalecode':obj[0].scalecode,
#             'paylevel':obj[0].pc7_level,
#             'gradepay':obj[0].payrate,
#             'joining_date':obj[0].date_of_joining,
#             'date_of_promotion':obj[0].date_of_promotion,
#             'station_dest':obj[0].station_des,
#             'wau':obj[0].wau,
#             'billunit':obj[0].billunit,
#             'service':obj[0].service_status,
#             'emptype':obj[0].emptype,
#             'ticket_no':obj[0].ticket_no,
#             'idcard_no':obj[0].idcard_no,
#             'emp_inctype':obj[0].emp_inctype,
#             'inc_category':obj[0].inc_category,
            
       
#            }  
       
       
#         return JsonResponse(context, safe = False)
#     return JsonResponse({"success":False}, status=400)

import json
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
       
        
#         parent=models.Level_Desig.objects.filter(designation=parentdesig).values('designation_code')
#         print(parent)
#         employeeUpdate=m1.empmast.objects.filter(empno=empno1).first()
#         var1=models.Level_Desig.objects.filter(designation=designation).first()
#         print(employeeUpdate,'----number')
#         var1.parent_desig_code=parent[0]['designation_code']
#         var1.save()
#         employeeUpdate.role=emprole
#         print(employeeUpdate.role)
#         empl=m1.empmast.objects.filter(empno=empno1).first()
#         print(empl)
#         sno=m1.empmastnew.objects.all().last().sno
        
#         m1.empmastnew.objects.create(sno=sno+1,emp_id=empl,shop_section=sop)
#         employeeUpdate.parent=emprole 
#         employeeUpdate.dept_desc=department
       
#         employeeUpdate.desig_longdesc=designation
        
#         employeeUpdate.save()
       
#         messages.success(request, 'Successfully Activate!')
        
        
#     return JsonResponse({'saved':'save'})


def getDesigbyDepartment(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
         
        obj=list(models.Level_Desig.objects.filter(department=department).values('designation').order_by('designation').distinct('designation'))
        print(obj,'____________________________________')
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)


# def officer_bydiv(request):
#     if request.method == "GET" and request.is_ajax():
#         div_1 = request.GET.get('div_1')
         
#         div_id=railwayLocationMaster.objects.filter(location_code=div_1)[0].rly_unit_code
#         obj=list(models.empmast.objects.filter(division_id=div_id).values('empname').order_by('empname'))
#         context={
#             'obj':obj,
#         }
#         return JsonResponse(context, safe = False)
#     return JsonResponse({"success":False}, status=400)


 

def getsection_byshop1(request):
    if request.method == "GET" and request.is_ajax():
        shop = request.GET.get('shop')
        print(shop)  
         
        shop_id=models.shop_section.objects.filter(shop_code=shop).values('section_code')
        
       
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
         
        desig_id=models.Level_Desig.objects.filter(designation=designation)[0].designation_code
        print(desig_id)
        role=list(models.roles.objects.filter(designation_code=desig_id).values('role').distinct('role'))
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
        
        desig_id=models.Level_Desig.objects.filter(department=department,pc7_level__gte=paylevel1).values('designation')
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
         
        dept_id=models.departMast.objects.filter(department_name=department)[0].department_code
        print(dept_id)
        shop_code=list(models.shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
        
        l=[]
        for i in shop_code:
            l.append(i['shop_code'])
        print(l)    
        context={
            'shop_code':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


def getsection_byshop(request):
     if request.method == "GET" and request.is_ajax():
        shop = request.GET.get('shop')
        print(shop)  
         
        shop=list(models.shop_section.objects.filter(shop_code=shop).values('section_code').distinct('section_code'))
        print(shop)
    
        l=[]
        for i in shop:
            l.append(i['section_code'])
        print(l)    
        context={
            'shop':l,
        } 
        return JsonResponse(context, safe = False)
     return JsonResponse({"success":False}, status=400)

    

# def getshop_bydept(request):
#     if request.method == "GET" and request.is_ajax():
#         dept = request.GET.get('dept')
#         print(dept)  
         
#         dept_id=models.departMast.objects.filter(department_name=dept)[0].department_code
#         print(dept_id)
#         shop=list(models.shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
#         print(shop)
#         l=[]
#         for i in shop:
#             l.append(i['shop_code'])
#         print(l)    
#         context={
#             'shop':l,
#         } 
#         return JsonResponse(context, safe = False)
#     return JsonResponse({"success":False}, status=400)


# def post_bydept(request):
#     if request.method == "GET" and request.is_ajax():
#         dept1 = request.GET.get('dept1')
#         print(dept1)
#         dept_id=models.departMast.objects.filter(department_name=dept1)[0].department_code
#         print(dept_id)
#         post=list(models.Post_master.objects.filter(department_code_id=dept_id).values('post_desc').distinct('post_desc'))
#         print(post)
#         context={
#             'post':post,
#         }
       
        
       
#         return JsonResponse(context, safe = False)
#     return JsonResponse({"success":False}, status=400)


# def getpost_bydept(request):
#     if request.method == "GET" and request.is_ajax():
#         dept = request.GET.get('dept')
#         print(dept)  
         
#         dept_id=models.departMast.objects.filter(department_name=dept)[0].department_code
#         print(dept_id)
#         post=list(models.Post_master.objects.filter(department_code_id=dept_id).values('post_desc').distinct('post_desc'))
#         print(post)
#         l=[]
#         for i in post:
#             l.append(i['post_desc'])
#         print(l)    
#         context={
#             'post':l,
#         } 
#         return JsonResponse(context, safe = False)
#     return JsonResponse({"success":False}, status=400)



# def shop_data(request):
#     if request.method == 'POST' or request.is_ajax():
        
#         dept = request.POST.get('dept')
#         shop = request.POST.get('shop')
#         print(dept)
#         print(shop)
#         dept_id=models.departMast.objects.filter(department_name=dept)[0].department_code
#         print(dept_id)
#         count=1
#         shopcode=models.shop_section.objects.filter(department_code_id=dept_id).distinct('shop_code').count()+1
#         print(shopcode,"+++++++++")
#         c = ('%02d' % shopcode)
#         shopcode1=c

#         # for i in shopcode:
#         #     c = ('%02d' % shopcode)
#         #     shopcode1=c
#         #     count+1
#         #     print(shopcode1)
       
#         print(shopcode1)
        
#         shop_id=str(120)+str(dept_id)+str(shopcode1)
#         print(shop_id)
#         section_id=shop_id+'00'
#         print(section_id)
#         section_code=int(section_id[5:9])
        
        
#         print(section_code,'--------------__________--------------------')
#         models.shop_section.objects.create(department_code_id=dept_id,shop_code=shop,shop_id=shop_id,section_id=section_id,rly_unit_code=120,section_code=section_code)
#         messages.success(request,'Data saved successfully')
        
            
#     return JsonResponse({'saved':'save'})


def inspection_doneby_list(request):
    empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    
    if empnox:
        empno = empnox[0].designation_code
        desig = empnox[0].designation


        # print('@@@@@@@@@@@@@')
        rly=request.POST.getlist('zone')
        div=request.POST.getlist('division')
        dept=request.POST.getlist('department')
        loc=request.POST.getlist('location')
        # start_date=request.POST.get('start')
        # end_date=request.POST.get('txtDate2')
        # get_designation=request.POST.get('get_designation')
        # print(request.user,"~~~~~~~~~")
        
        list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code')
        list4=[]
        for i in list3:
            list4.append(i['location_code'])    
        # print(list4,'_________llllllllll_____')
        list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code')
        list2=[]
        for i in list1:
            # print(i['location_code'],'_________')
            list2.append(i['location_code'])
            
        list5=list(models.departMast.objects.all().values('department_name')) 
        item=[] 
        # print(list5)
        
        try: 
            
            if len(rly) != 0 or len(dept) !=0 or len(div)!=0 or len(loc)!=0:
                print('rly', rly)
                loca = m1.Insp_multi_location.objects.filter(Q(item__in=rly)|Q(item__in=div)|Q(item__in=dept)|Q(item__in=loc), inspection_no__status_flag=1, inspection_no__inspection_officer=empno ).values_list('inspection_no', flat=True)
                print('!!!!!!!!!!', loca)
                mydata=list(m1.Inspection_details.objects.filter(inspection_no__in=loca).values().order_by('-inspection_no'))
                # print(mydata)
                for i in mydata:
                    location = list(m1.Insp_multi_location.objects.filter(inspection_no=i['inspection_no']).values())
                    print(location)
                    i.update({'location_item': location})
                print("########")
                
                
                
            else:
                mydata=list(m1.Inspection_details.objects.filter(status_flag=1, inspection_officer=empno).values().order_by('-inspection_no'))
                # print(mydata)
                for i in mydata:
                    location = list(m1.Insp_multi_location.objects.filter(inspection_no=i['inspection_no']).values())
                    print(location)
                    i.update({'location_item': location})
                print('666666666', mydata)

                
                    
                    
        except Exception as e:
            print("e==",e)  
        
        context={
            'Zone':list2 ,
            'division':list4,
            'department':list5,
            'mydata':mydata,
            'item':item,
            'desig': desig
        }
        
        
        return render(request,"inspection_doneby_list.html",context)
    else:
        messages.error(request, 'You are not authorize to draft inspection. Please contact to admin')
        return render(request,"inspection_doneby_list.html")

def getSearchValue_ajax(request):
    if request.method == 'POST' and request.is_ajax():
        
        
        rly=json.loads(request.POST.get('zone1'))
        div=json.loads(request.POST.get('division1'))
        dept=json.loads(request.POST.get('department1'))
        loc=json.loads(request.POST.get('location1'))
        
        dates = request.POST.get('date_range')
        print(rly, div, dept, loc, dates, '==================')
        empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    
        if empnox:
            empno = empnox[0].designation_code
            desig = empnox[0].designation
        end = ''
        start = ''
        if dates:
            sp_date = dates.split('-')
            print(sp_date, '00000')
            start  = datetime.strptime(sp_date[0].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
            
            end  = datetime.strptime(sp_date[1].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
            

        print(start, end, ':date')
        # loca1 = m1.Insp_multi_location.objects.filter((Q(item__in=rly)|Q(item__in=div)|Q(item__in=dept)|Q(item__in=loc)| Q(inspection_no__created_on__gte=start , inspection_no__created_on__lte=end)) & Q(inspection_no__status_flag=1, inspection_no__inspection_officer=empno)).values_list('inspection_no', flat=True)
        # print(loca1, 'insp data:', len(loca1))
        loca = m1.Insp_multi_location.objects.filter((Q(item__in=rly)|Q(item__in=div)|Q(item__in=dept)|Q(item__in=loc) & Q(inspection_no__created_on__gte=start , inspection_no__created_on__lte=end)) & Q(inspection_no__status_flag=1, inspection_no__inspection_officer=empno)).values_list('inspection_no', flat=True)
        # print('!!!!!!!!!!', loca)
        mydata=list(m1.Inspection_details.objects.filter(inspection_no__in=loca).values().order_by('-inspection_no'))
        print(mydata, 'mydata', len(mydata))
        for i in mydata:
            location = list(m1.Insp_multi_location.objects.filter(inspection_no=i['inspection_no']).values())
            # print(location)
            insp = m1.Marked_Officers.objects.filter(item_no__inspection_no=i['inspection_no'])
            over_all = insp.count()
            remaning = insp.filter(status_flag=2).count()
            if over_all != 0:
                persentage  = (remaning/over_all)*100
                persentage = round(persentage)
            else:
                persentage = 0

            i.update({'location_item': location, 'persentage': persentage})
        
        print(mydata)
        return JsonResponse({'mydata':mydata}, safe=False)

    return JsonResponse({'success': False}, status=400)


def getSearchValueClose_ajax(request):
    if request.method == 'POST' and request.is_ajax():
        
        
        rly=json.loads(request.POST.get('zone1'))
        div=json.loads(request.POST.get('division1'))
        dept=json.loads(request.POST.get('department1'))
        loc=json.loads(request.POST.get('location1'))
        
        dates = request.POST.get('date_range')
        print(rly, div, dept, loc, dates, '==================')
        empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    
        if empnox:
            empno = empnox[0].designation_code
            desig = empnox[0].designation
        end = ''
        start = ''
        if dates:
            sp_date = dates.split('-')
            print(sp_date, '00000')
            start  = datetime.strptime(sp_date[0].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
            
            end  = datetime.strptime(sp_date[1].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
            

        print(start, end, ':date')
        # loca1 = m1.Insp_multi_location.objects.filter((Q(item__in=rly)|Q(item__in=div)|Q(item__in=dept)|Q(item__in=loc)| Q(inspection_no__created_on__gte=start , inspection_no__created_on__lte=end)) & Q(inspection_no__status_flag=1, inspection_no__inspection_officer=empno)).values_list('inspection_no', flat=True)
        # print(loca1, 'insp data:', len(loca1))
        loca = m1.Insp_multi_location.objects.filter((Q(item__in=rly)|Q(item__in=div)|Q(item__in=dept)|Q(item__in=loc) & Q(inspection_no__created_on__gte=start , inspection_no__created_on__lte=end)) & Q(inspection_no__status_flag=4, inspection_no__inspection_officer=empno)).values_list('inspection_no', flat=True)
        # print('!!!!!!!!!!', loca)
        mydata=list(m1.Inspection_details.objects.filter(inspection_no__in=loca).values().order_by('-inspection_no'))
        print(mydata, 'mydata', len(mydata))
        for i in mydata:
            location = list(m1.Insp_multi_location.objects.filter(inspection_no=i['inspection_no']).values())
            # print(location)
            insp = m1.Marked_Officers.objects.filter(item_no__inspection_no=i['inspection_no'])
            over_all = insp.count()
            remaning = insp.filter(status_flag=3).count()
            if over_all != 0:
                persentage  = (remaning/over_all)*100
                persentage = round(persentage)
            else:
                persentage = 0
            i.update({'location_item': location, 'persentage': persentage})
        
        print(mydata)
        return JsonResponse({'mydata':mydata}, safe=False)

    return JsonResponse({'success': False}, status=400)



def getSearchValueRecived_ajax(request):
    if request.method == 'POST' and request.is_ajax():
        
        
        rly=json.loads(request.POST.get('zone1'))
        div=json.loads(request.POST.get('division1'))
        dept=json.loads(request.POST.get('department1'))
        loc=json.loads(request.POST.get('location1'))
        
        dates = request.POST.get('date_range')
        print(rly, div, dept, loc, dates, '==================')
        empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    
        if empnox:
            empno = empnox[0].designation_code
            desig = empnox[0].designation
        end = ''
        start = ''
        if dates:
            sp_date = dates.split('-')
            print(sp_date, '00000')
            start  = datetime.strptime(sp_date[0].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
            
            end  = datetime.strptime(sp_date[1].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
            

        print(start, end, ':date')
        # loca1 = m1.Insp_multi_location.objects.filter((Q(item__in=rly)|Q(item__in=div)|Q(item__in=dept)|Q(item__in=loc)| Q(inspection_no__created_on__gte=start , inspection_no__created_on__lte=end)) & Q(inspection_no__status_flag=1, inspection_no__inspection_officer=empno)).values_list('inspection_no', flat=True)
        # print(loca1, 'insp data:', len(loca1))
        loca = m1.Insp_multi_location.objects.filter((Q(item__in=rly)|Q(item__in=div)|Q(item__in=dept)|Q(item__in=loc) & Q(inspection_no__created_on__gte=start , inspection_no__created_on__lte=end)) & Q( inspection_no__inspection_officer=empno)).values_list('inspection_no', flat=True)
        # print('!!!!!!!!!!', loca)
        # mydata=list(m1.Inspection_details.objects.filter(inspection_no__in=loca).values().order_by('-inspection_no'))
        # print(mydata, 'mydata', len(mydata))
        # for i in mydata:
        #     location = list(m1.Insp_multi_location.objects.filter(inspection_no=i['inspection_no']).values())
        #     # print(location)
        #     i.update({'location_item': location})
        
        # print(mydata)
        obj1 = m1.Marked_Officers.objects.filter(status_flag=2,item_no__inspection_no__inspection_officer=empno, item_no__inspection_no__in=loca).values('item_no__inspection_no').distinct()
        
        mydata1 =[]
        for i in obj1:
            insp = i['item_no__inspection_no']
            mydata = list(m1.Inspection_details.objects.filter(inspection_no=insp).values())
            location = list(m1.Insp_multi_location.objects.filter(inspection_no=insp).values())
            for j in mydata:
                j.update({'location_item': location})
            
            
            
            mydata1.extend(mydata)
        print('iiiiiiiiiiiii',  mydata1)

            
        return JsonResponse({'mydata':mydata1}, safe=False)

    return JsonResponse({'success': False}, status=400)



def getSearchValueCorrigendum_ajax(request):
    if request.method == 'POST' and request.is_ajax():
        
        
        rly=json.loads(request.POST.get('zone1'))
        div=json.loads(request.POST.get('division1'))
        dept=json.loads(request.POST.get('department1'))
        loc=json.loads(request.POST.get('location1'))
        
        dates = request.POST.get('date_range')
        print(rly, div, dept, loc, dates, '==================')
        empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    
        if empnox:
            empno = empnox[0].designation_code
            desig = empnox[0].designation
        end = ''
        start = ''
        if dates:
            sp_date = dates.split('-')
            print(sp_date, '00000')
            start  = datetime.strptime(sp_date[0].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
            
            end  = datetime.strptime(sp_date[1].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
            

        print(start, end, ':date')
        # loca1 = m1.Insp_multi_location.objects.filter((Q(item__in=rly)|Q(item__in=div)|Q(item__in=dept)|Q(item__in=loc)| Q(inspection_no__created_on__gte=start , inspection_no__created_on__lte=end)) & Q(inspection_no__status_flag=1, inspection_no__inspection_officer=empno)).values_list('inspection_no', flat=True)
        # print(loca1, 'insp data:', len(loca1))
        loca = m1.Insp_multi_location.objects.filter((Q(item__in=rly)|Q(item__in=div)|Q(item__in=dept)|Q(item__in=loc) & Q(inspection_no__created_on__gte=start , inspection_no__created_on__lte=end)) & Q( inspection_no__inspection_officer=empno)).values_list('inspection_no', flat=True)
        # print('!!!!!!!!!!', loca)
        # mydata=list(m1.Inspection_details.objects.filter(inspection_no__in=loca).values().order_by('-inspection_no'))
        # print(mydata, 'mydata', len(mydata))
        # for i in mydata:
        #     location = list(m1.Insp_multi_location.objects.filter(inspection_no=i['inspection_no']).values())
        #     # print(location)
        #     i.update({'location_item': location})
        
        # print(mydata)
        obj1 = m1.Marked_Officers.objects.filter(status_flag=4,item_no__inspection_no__inspection_officer=empno, item_no__inspection_no__in=loca).values('item_no__inspection_no').distinct()
        
        mydata1 =[]
        for i in obj1:
            insp = i['item_no__inspection_no']
            mydata = list(m1.Inspection_details.objects.filter(inspection_no=insp).values())
            location = list(m1.Insp_multi_location.objects.filter(inspection_no=insp).values())
            for j in mydata:
                j.update({'location_item': location})
            
            
            
            mydata1.extend(mydata)
        print('iiiiiiiiiiiii',  mydata1)

            
        return JsonResponse({'mydata':mydata1}, safe=False)

    return JsonResponse({'success': False}, status=400)



        
def created_checklist(request):

    empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    
    if empnox:
        empno = empnox[0].designation_code
        desig = empnox[0].designation


        # print('@@@@@@@@@@@@@')
        rly=request.POST.getlist('zone')
        div=request.POST.getlist('division')
        dept=request.POST.getlist('department')
        loc=request.POST.getlist('location')
        # start_date=request.POST.get('start')
        # end_date=request.POST.get('txtDate2')
        # get_designation=request.POST.get('get_designation')
        print(rly, div, dept, loc, "~~~~~~~~~")
        
        list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code')
        list4=[]
        for i in list3:
            list4.append(i['location_code'])    
        # print(list4,'_________llllllllll_____')
        list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code')
        list2=[]
        for i in list1:
            # print(i['location_code'],'_________')
            list2.append(i['location_code'])
            
        list5=list(models.departMast.objects.all().values('department_name')) 
        item=[] 
        # print(list5)
        
        try: 
            
            if len(rly) != 0 or len(dept) !=0 or len(div)!=0 or len(loc)!=0:
                print('rly', rly)
                loca = m1.Insp_multi_location.objects.filter(Q(item__in=rly)|Q(item__in=div)|Q(item__in=dept)|Q(item__in=loc), inspection_no__status_flag=1, inspection_no__inspection_officer=empno ).values_list('inspection_no', flat=True)
                # print('!!!!!!!!!!', loca)
                mydata=list(m1.Inspection_details.objects.filter(inspection_no__in=loca).values().order_by('-inspection_no'))
                # print(mydata)
                for i in mydata:
                    location = list(m1.Insp_multi_location.objects.filter(inspection_no=i['inspection_no']).values())
                    print(location)
                    i.update({'location_item': location})
                # print("########")
                
                
            else:
                mydata=list(m1.Inspection_details.objects.filter(status_flag=1, inspection_officer=empno).values().order_by('-inspection_no'))
                # print(mydata)
                for i in mydata:
                    insp = m1.Marked_Officers.objects.filter(item_no__inspection_no=i['inspection_no'])
                    over_all = insp.count()
                    remaning = insp.filter(status_flag=2).count()
                    if over_all != 0:
                        persentage  = (remaning/over_all)*100
                        persentage = round(persentage)
                    else:
                        persentage = 0

                    print('**********', over_all, remaning, persentage,i['inspection_no'])
                    location = list(m1.Insp_multi_location.objects.filter(inspection_no=i['inspection_no']).values())
                    # print(location)
                    i.update({'location_item': location, 'persentage': persentage})
                # print('666666666', mydata)
                    
                    
        except Exception as e:
            print("e==",e)  
        
        context={
            'Zone':list2 ,
            'division':list4,
            'department':list5,
            'mydata':mydata,
            'item':item,
            'desig': desig
        }
        
        
        return render(request,"list_create_inspection_report.html",context)
    else:
        messages.error(request, 'You are not authorize to draft inspection. Please contact to admin')
        return render(request,"list_create_inspection_report.html")
        
             
      
def viewInspectionsDoneReport(request, insp_id):

    ins_detail=list(m1.Inspection_details.objects.filter(inspection_no=insp_id).values())
    item_details1= list(m1.Item_details.objects.filter(inspection_no_id=insp_id).values())
    for j in item_details1:
        
        if j['type'] == 'SH':
            mark=m1.Marked_Officers.objects.filter(item_no=j['item_no']).values()
            print('---------', j['item_no'])
            mrkoffi = {}
            desig_longdesc1 =''
            marked_officers1 = ''
            for x in mark:
                print('xxxxxxxxx', x['myuser_id_id'])
                
                marked=m1.empmast.objects.filter(myuser_id=x['myuser_id_id'])
                print('yyyyyyyy', marked[0].desig_longdesc)
                desig_longdesc1 += marked[0].desig_longdesc+','
                marked_officers1 += marked[0].empno+','
            print('kkkkkkkkkkkkkkk', desig_longdesc1)
            mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': desig_longdesc1})
            
            j.update({'mrkoffi': mrkoffi})
            # print('mmmmmmmm', desig_longdesc1)
        
    ins_detail[0].update({'item_details1': item_details1})
    # print('00000000', ins_detail)
    print('00000000', ins_detail)

    context={
        'ins_detail':ins_detail
        
        }  
        
    return render(request, 'view_inspection_done.html', context)


def section_data(request):
    if request.method == 'POST' or request.is_ajax():
        
        dept1 = request.POST.get('dept1')
        print(dept1)
        sectiondept = request.POST.get('sectiondept')
        print(sectiondept)
        sec = request.POST.get('sec')
        print(sec)
        dept_id=models.departMast.objects.filter(department_name=dept1)[0].department_code
        print(dept_id)
        shopcode=models.shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).last().section_id
        shopcode_id=models.shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).last().shop_id
        section_code=models.shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).last().section_code
        print(shopcode)
        #shop_id=str(int(shopcode[0:-2]))+str(int(shopcode[-2:-1])+1)
        #print(shop_id,'____________________________________________________shop_id___________')
        shop_id=int(shopcode)+1
        sec_code=int(section_code)+1
        if models.shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).exists():

            models.shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).create(section_id=shop_id,section_desc=sec,shop_code=sectiondept,department_code_id=dept_id,shop_id=shopcode_id,section_code=sec_code)
            messages.success(request,'Data saved successfully')
        
            
    return JsonResponse({'saved':'save'})


def dept_data(request):
    if request.method == 'POST' or request.is_ajax():
        current_user = request.user
        emp=m1.empmast.objects.get(pk=current_user.username).values('wau')
        emp['wau']
        department = request.POST.get('department')
        now = datetime.datetime.now()
        

        p=str(now).split(' ')
        
        s=p[0].split('-')
        day2 = s[0]
        month2 = s[1]
        year2 = s[2]
        
        date1 = year2+""+month2+""+day2
        
        time=str(p[1]).replace(':','')
        obj=list(models.departMast.objects.filter(department_name=department).values('department_name').distinct())
        sc_1=int(models.departMast.objects.last().department_code)
        print(sc_1)
           
        print(obj,'obj')
        if len(obj)==0:
            print('a')
            models.departMast.objects.create(department_name=department, department_code=sc_1+1,modified_by=emp.empno,rly_unit_code_id=emp['wau'])
            messages.success(request,'Data saved successfully')
        else:
            messages.error(request,'Department Already Exists!')
            print('b')
            # railwayLocationMaster.objects.filter(location_code=location_code).update(location_type=location_type, location_description=desc, parent_location_code=ploco_code, location_type_desc=type_desc, rstype=rstype, station_code=st_code)
           
    return JsonResponse({'saved':'save'})

# def shop_section(request):
#     current_user = request.user
#     emp=m1.empmast.objects.get(pk=current_user.username) 
#     unit=models.departMast.objects.filter(delete_flag=False).values('department_name').order_by('department_name').distinct('department_name')
#     list=[]
#     cur= connection.cursor()
#     cur.execute('''select department_name,shop_code,shop_id,section_code,section_id from dlw_shop_section a join dlw_departMast b on
#     a.department_code_id=b.department_code order by (b.department_name,a.shop_code,a.section_code) ''')
#     d=cur.fetchall()
#     print(d,'________________')
#     for i in d:
#         temp={}
#         temp['department_name']=i[0]
#         temp['shop_code']=i[1]
#         temp['shop_id']=i[2]
#         temp['section_code']=i[3]
#         temp['section_id']=i[4]
#         list.append(temp)
#     print('list',list,'_____________________________')    
#     # val = models.shop_section.objects.filter(department_code_id__isnull=False).values('shop_code','shop_id','section_code','section_id','department_code_id').distinct() 
#     # for i in val:
#     #     temp={}
#     #     temp['shop_code']=i['shop_code']
#     #     temp['shop_id']=i['shop_id']
#     #     temp['section_code']=i['section_code']
#     #     temp['section_id']=i['section_id']
#     #     if models.departMast.objects.filter(department_code=i['department_code_id']).exists():
#     #         temp['department_name']=models.departMast.objects.filter(department_code=i['department_code_id'])[0].department_name 
#     #     else:
#     #         temp['department_name']='None'     
#     #     list.append(temp)

#     # mylist = []
#     # for i in unit:
#     #     temp={}
#     #     #y = models.department_master.objects.filter(department_name=i['department_name'],delete_flag=False).order_by('shop_code').values('shop_code')
#     #     print(y,'--------')
#     #     temp['department_name']=i['department_name']
#     #     str=""
#     #     for j in y:
#     #         print(j,'-----------')
#     #         if(j['shop_code']!=None):
#     #             str+=j['shop_code'] + "\r\n"
#     #     temp['shop_code']=str
#     #     mylist.append(temp)
#     # print(mylist,'_________')
           
   
#     context={
#         'emp':emp,
#         'list':list,
#         # 'val':val,
#         'unit':unit,
       
#     }
    
#     return render(request, 'shop_section.html',context)


# def shop_bydept(request):
#     if request.method == "GET" and request.is_ajax():
#         dept = request.GET.get('dept')
#         print("===================",dept)
#         dept_id=models.departMast.objects.filter(department_name=dept)[0].department_code
#         print("========id===========",dept_id)
#         shop_code=list(models.shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
#         print(shop_code)
#         context={
#             'shop_code':shop_code,
#         }
       
        
       
#         return JsonResponse(context, safe = False)
#     return JsonResponse({"success":False}, status=400)

def section_bydept(request):
    if request.method == "GET" and request.is_ajax():
        dept = request.GET.get('dept')
        sectiondept = request.GET.get('sectiondept')
        print(sectiondept)
        dept_id=models.departMast.objects.filter(department_name=dept)[0].department_code
        print(dept_id)
        section_desc=list(models.shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).values('section_desc').distinct('section_desc'))
        print(section_desc)
        context={
            'section_desc':section_desc,
        }
       
        
       
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


def RoleAdd(request):
    cuser=request.user
    usermaster=m1.empmast.objects.filter(empno=cuser).first()
    current_user = request.user
    emp=m1.empmast.objects.filter(pk=current_user.username).values('wau')
    rolelist=usermaster.role.split(", ")  
    list=[]
    
    val = models.roles.objects.all().filter(delete_flag=False).values('role','parent','department_code_id').order_by('role').distinct() 
    for i in val:
        temp={}
        temp['role']=i['role']
        temp['parent']=i['parent']
        if models.departMast.objects.filter(department_code=i['department_code_id']).exists():
            temp['department_name']=models.departMast.objects.filter(department_code=i['department_code_id'])[0].department_name 
        else:
            temp['department_name']='None'     
        list.append(temp)
    role = models.roles.objects.all().filter(delete_flag=False).values('role').order_by('role').distinct()
    empdep = models.departMast.objects.all().values('department_name').order_by('department_name').distinct()
    shop = models.shop_section.objects.values('shop_code').order_by('shop_code').distinct()
    users = []
    if request.method=="POST":
        rolename = request.POST.get('roldel')
        print(rolename)
        if rolename:
          
            models.custom_menu.objects.all().filter(role=rolename).delete()
            models.roles.objects.all().filter(role=rolename).update(delete_flag=True)
            userremove = m1.empmast.objects.all().values('empno').filter(role=rolename)
            for i in range(len(userremove)):
                # users.append(userremove[i]['empno'])
                m1.empmast.objects.filter(empno=userremove[i]['empno']).update(role=None,parent=None)
            # User.objects.filter(username__in=users).delete()
            messages.success(request, 'Successfully Deleted!')
        else:
            messages.error(request,"Error")
    context = {
       
        'nav':nav,
        'subnav':subnav,
        'roles' : role,
        'val':val,
        'empdep':empdep,
        'shop':shop,
        'list':list,
        'wau':emp[0]['wau'],
    }
    return render(request,'RoleAdd.html',context)


# def ajaxDeleteRoleUser(request):
#     if request.method == 'POST' or request.is_ajax():

#         rolename= request.POST.get('roledel')
#         if rolename:
#             perlist = models.custom_menu.objects.filter(role=rolename).values('url').distinct()   
#             models.custom_menu.objects.all().filter(role=rolename).delete()
#             models.roles.objects.all().filter(role=rolename).update(delete_flag=True)
#             userremove = m1.empmast.objects.all().values('empno').filter(role=rolename)
#             for i in range(len(userremove)):
               
#                 m1.empmast.objects.filter(empno=userremove[i]['empno']).update(role=None,parent=None)
            
       
#     return JsonResponse({'deleted':'delete'})


def ajaxRoleGen(request):
    
    if request.method=='POST' or request.is_ajax():
        current_user = request.user
        emp=m1.empmast.objects.get(pk=current_user.username)  
        rolename = request.POST.get('rolename')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        shop = request.POST.get('shop1')
        shop1 = json.loads(shop)
        sop =''
        for o in shop1:
            sop=sop+o+", "

        print(sop,'---------', designation)
        role=models.roles.objects.filter(role=rolename)
        desig_id=models.Level_Desig.objects.filter( designation= designation)[0].designation_code
        print(desig_id)
        dept_id=models.departMast.objects.filter(department_name=department)[0].department_code
        print(dept_id)
        if len(role)==0:
            models.roles.objects.create(role=rolename,parent=rolename,department_code_id=dept_id,modified_by=emp.empno, rly_unit=emp.wau,shop_code=sop, designation_code=desig_id)            
            messages.success(request,"succesfully added!")
        else:
            messages.error(request,"This role already exists")
    return JsonResponse({'saved':'save'})


def getDepartmentbyroles(request):
    if request.method == "GET" and request.is_ajax():
        emptdepartment = request.GET.get('emptdepartment')
               
        if emptdepartment !=None: 
            obj=list(models.departMast.objects.filter(department=emptdepartment).values('designation').order_by('designation').distinct())
            
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)


def getDesigbyDepartment(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
         
        obj=list(models.Level_Desig.objects.filter(department=department).values('designation').order_by('designation').distinct('designation'))
        print(obj,'____________________________________')
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)


def getshopcode_bydept(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
         
        dept_id=models.departMast.objects.filter(department_name=department)[0].department_code
        print(dept_id)
        shop_code=list(models.shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
        
        l=[]
        for i in shop_code:
            l.append(i['shop_code'])
        print(l)    
        context={
            'shop_code':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)

def inspect_logout(request):
    try:
        logout(request)
        return HttpResponseRedirect('/login')
    except Exception as e: 
       print(e)

def inspect_changePassword(request):
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

#niyati 150622
  

def getdiv_rly(request):

    if request.method == "GET" or request.is_ajax():
        rly=request.GET.get('rly_data')
        newrly = json.loads(rly)

        print(rly,'rly=======')
          
        division=list(models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code__in=newrly).order_by('location_code').values('location_code').distinct('location_code'))
        l=[]
        for i in division:
            l.append(i['location_code'])
        print(l)    
        context={
            'division':l,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)




def division_wise(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.getlist('rly_1[]')
        print(rly_1,'_________________________railways________________')
        div_1=request.GET.getlist('div_1[]')
        print(div_1,'___________________div________________') 
        dept_1=request.GET.getlist('dept_1[]')
        print(dept_1,'___________________dept________________') 
        hqwise=[]
        alldiv=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('rly_unit_code')
        if div_1==[] and dept_1==[]:
            alldesig=models.Level_Desig.objects.filter(rly_unit_id__in=alldiv).values('designation','empno')
            for i in alldesig:
                hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
                if len(hq)>0:
                    name=hq[0]['empname']
                    if hq[0]['empmname'] is not None:
                        name=name+' '+hq[0]['empmname']
                    if hq[0]['emplname'] is not None:
                        name=name+' '+hq[0]['emplname']
                    hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})

        elif div_1==[] and dept_1!=[]:
            alldesig=models.Level_Desig.objects.filter(rly_unit_id__in=alldiv,department__in=dept_1).values('designation','empno')
            for i in alldesig:
                hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
                if len(hq)>0:
                    name=hq[0]['empname']
                    if hq[0]['empmname'] is not None:
                        name=name+' '+hq[0]['empmname']
                    if hq[0]['emplname'] is not None:
                        name=name+' '+hq[0]['emplname']
                    hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
        elif div_1!=[] and dept_1!=[]:
            div=models.railwayLocationMaster.objects.filter(location_code__in=div_1).values('rly_unit_code')
            alldesig=models.Level_Desig.objects.filter(rly_unit_id__in=div,department__in=dept_1).values('designation','empno')
            for i in alldesig:
                hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
                if len(hq)>0:
                    name=hq[0]['empname']
                    if hq[0]['empmname'] is not None:
                        name=name+' '+hq[0]['empmname']
                    if hq[0]['emplname'] is not None:
                        name=name+' '+hq[0]['emplname']
                    hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
        elif div_1!=[] and dept_1==[]:
            div=models.railwayLocationMaster.objects.filter(location_code__in=div_1).values('rly_unit_code')
            alldesig=models.Level_Desig.objects.filter(rly_unit_id__in=div).values('designation','empno')
            for i in alldesig:
                hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
                if len(hq)>0:
                    name=hq[0]['empname']
                    if hq[0]['empmname'] is not None:
                        name=name+' '+hq[0]['empmname']
                    if hq[0]['emplname'] is not None:
                        name=name+' '+hq[0]['emplname']
                    hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
        
        context={
           'divwise':hqwise,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)



def gm_list_officers(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.getlist('rly_1[]')
        hqwise=[]
        # allrly=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('rly_unit_code')

        # if rly_1==[]:
        #     alldesig=models.Level_Desig.objects.filter(d_level='GM').values('designation','empno')
        #     for i in alldesig:
        #         hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
        #         if len(hq)>0:
        #             name=hq[0]['empname']
        #             if hq[0]['empmname'] is not None:
        #                 name=name+' '+hq[0]['empmname']
        #             if hq[0]['emplname'] is not None:
        #                 name=name+' '+hq[0]['emplname']
        #             hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
        # else:   
        hq=models.railwayLocationMaster.objects.filter(location_type_desc='HEAD QUATER').values('rly_unit_code')
        alldesig=models.Level_Desig.objects.filter(d_level='GM',rly_unit_id__in=hq).values('designation','empno')
        for i in alldesig:
            hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
            if len(hq)>0:
                name=hq[0]['empname']
                if hq[0]['empmname'] is not None:
                    name=name+' '+hq[0]['empmname']
                if hq[0]['emplname'] is not None:
                    name=name+' '+hq[0]['emplname']
                hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
    

        allgm=sorted(hqwise, key=lambda hqwise:hqwise['empname'])
        context={
           'allgm':allgm,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)


def drm_officers(request):
    if request.method == "GET" and request.is_ajax():
        div_1=request.GET.getlist('div_1[]')
        print(div_1)
        hqwise=[]
        if  div_1==[]:
            alldesig=models.Level_Desig.objects.filter(d_level='DRM').values('designation','empno')
            for i in alldesig:
                hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
                if len(hq)>0:
                    name=hq[0]['empname']
                    if hq[0]['empmname'] is not None:
                        name=name+' '+hq[0]['empmname']
                    if hq[0]['emplname'] is not None:
                        name=name+' '+hq[0]['emplname']
                    hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
        
        else:   
            hq=models.railwayLocationMaster.objects.filter(parent_location_code__in=div_1).values('rly_unit_code')
            alldesig=models.Level_Desig.objects.filter(d_level='DRM',rly_unit_id__in=hq).values('designation','empno')
            for i in alldesig:
                hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
                if len(hq)>0:
                    name=hq[0]['empname']
                    if hq[0]['empmname'] is not None:
                        name=name+' '+hq[0]['empmname']
                    if hq[0]['emplname'] is not None:
                        name=name+' '+hq[0]['emplname']
                    hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})


        alldrm=sorted(hqwise, key=lambda hqwise:hqwise['empname'])
        
        context={
           'alldrm':alldrm,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)


def phod_officers(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.getlist('rly_1[]')
        hqwise=[]
        if rly_1==[]:
            alldesig=models.Level_Desig.objects.filter(d_level='PHOD').values('designation','empno')
            for i in alldesig:
                hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
                if len(hq)>0:
                    name=hq[0]['empname']
                    if hq[0]['empmname'] is not None:
                        name=name+' '+hq[0]['empmname']
                    if hq[0]['emplname'] is not None:
                        name=name+' '+hq[0]['emplname']
                    hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
        else:   
            hq=models.railwayLocationMaster.objects.filter(location_code__in=rly_1).values('rly_unit_code')
            alldesig=models.Level_Desig.objects.filter(d_level='PHOD',rly_unit_id__in=hq).values('designation','empno')
            for i in alldesig:
                hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
                if len(hq)>0:
                    name=hq[0]['empname']
                    if hq[0]['empmname'] is not None:
                        name=name+' '+hq[0]['empmname']
                    if hq[0]['emplname'] is not None:
                        name=name+' '+hq[0]['emplname']
                    hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
        

        allphod=sorted(hqwise, key=lambda hqwise:hqwise['empname'])

        context={
           'allphod':allphod,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)

def board_officers(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.getlist('rly_1[]')
        hqwise=[]
        #mem=['BM','AM','CRB']
        mem=['BM']
        # if rly_1==[]:
        #     alldesig=models.Level_Desig.objects.filter(d_level__in=mem).values('designation','empno')
        #     for i in alldesig:
        #         hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
        #         if len(hq)>0:
        #             name=hq[0]['empname']
        #             if hq[0]['empmname'] is not None:
        #                 name=name+' '+hq[0]['empmname']
        #             if hq[0]['emplname'] is not None:
        #                 name=name+' '+hq[0]['emplname']
        #             hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
        # else:   
        hq=models.railwayLocationMaster.objects.filter(location_type_desc='RAILWAY BOARD').values('rly_unit_code')
        alldesig=models.Level_Desig.objects.filter(d_level__in=mem,rly_unit_id__in=hq).values('designation','empno')
        for i in alldesig:
            hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
            if len(hq)>0:
                name=hq[0]['empname']
                if hq[0]['empmname'] is not None:
                    name=name+' '+hq[0]['empmname']
                if hq[0]['emplname'] is not None:
                    name=name+' '+hq[0]['emplname']
                hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
        allboard=sorted(hqwise, key=lambda hqwise:hqwise['empname'])
        context={
           'allboard':allboard,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)




def designation_wise(request):
    if request.method == "GET" and request.is_ajax():
        desig=request.GET.getlist('desig[]')
        hqwise=[]
        alldesig=models.Level_Desig.objects.filter(designation__in=desig).values('designation','empno')
        for i in alldesig:
            hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
            if len(hq)>0:
                name=hq[0]['empname']
                if hq[0]['empmname'] is not None:
                    name=name+' '+hq[0]['empmname']
                if hq[0]['emplname'] is not None:
                    name=name+' '+hq[0]['emplname']
                hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
        return JsonResponse(hqwise,safe = False)
    return JsonResponse({"success":False}, status = 400)

def headqwise(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.getlist('rly_1[]')
        print(rly_1,'_________________________railwayshh________________')
        dept_1=request.GET.getlist('dept_1[]')
        print(dept_1,'_________________________departmenthh________________')
        div_1=request.GET.getlist('div_1[]')
        print(dept_1,'_________________________divisionhh________________')
        hqwise=[]
        allrly=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('rly_unit_code')
        alldiv=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('rly_unit_code')
        if rly_1==[]:
            if dept_1==[]:
                alldesig=models.Level_Desig.objects.filter(rly_unit_id__in=allrly).values('designation','empno')
                for i in alldesig:
                    hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
                    if len(hq)>0:
                        name=hq[0]['empname']
                        if hq[0]['empmname'] is not None:
                            name=name+' '+hq[0]['empmname']
                        if hq[0]['emplname'] is not None:
                            name=name+' '+hq[0]['emplname']
                        hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})

            elif dept_1!=[]:
                alldesig=models.Level_Desig.objects.filter(rly_unit_id__in=allrly,department__in=dept_1).values('designation','empno')
                for i in alldesig:
                    hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
                    if len(hq)>0:
                        name=hq[0]['empname']
                        if hq[0]['empmname'] is not None:
                            name=name+' '+hq[0]['empmname']
                        if hq[0]['emplname'] is not None:
                            name=name+' '+hq[0]['emplname']
                        hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
            # elif div_1!=[] and dept_1!=[]:
            #     div=models.railwayLocationMaster.objects.filter(location_code__in=div_1).values('rly_unit_code')
            #     alldesig=models.Level_Desig.objects.filter(rly_unit_id__in=div,department__in=dept_1).values('designation','empno')
            #     for i in alldesig:
            #         hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
            #         if len(hq)>0:
            #             name=hq[0]['empname']
            #             if hq[0]['empmname'] is not None:
            #                 name=name+' '+hq[0]['empmname']
            #             if hq[0]['emplname'] is not None:
            #                 name=name+' '+hq[0]['emplname']
            #             hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
            # elif div_1!=[] and dept_1==[]:
            #     div=models.railwayLocationMaster.objects.filter(location_code__in=div_1).values('rly_unit_code')
            #     alldesig=models.Level_Desig.objects.filter(rly_unit_id__in=div).values('designation','empno')
            #     for i in alldesig:
            #         hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
            #         if len(hq)>0:
            #             name=hq[0]['empname']
            #             if hq[0]['empmname'] is not None:
            #                 name=name+' '+hq[0]['empmname']
            #             if hq[0]['emplname'] is not None:
            #                 name=name+' '+hq[0]['emplname']
            #             hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
        else:
            hq=models.railwayLocationMaster.objects.filter(location_code__in=rly_1).values('rly_unit_code')
            if  dept_1==[]:
                alldesig=models.Level_Desig.objects.filter(rly_unit_id__in=hq).values('designation','empno')
                for i in alldesig:
                    hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
                    if len(hq)>0:
                        name=hq[0]['empname']
                        if hq[0]['empmname'] is not None:
                            name=name+' '+hq[0]['empmname']
                        if hq[0]['emplname'] is not None:
                            name=name+' '+hq[0]['emplname']
                        hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})

            elif  dept_1!=[]:
                alldesig=models.Level_Desig.objects.filter(rly_unit_id__in=hq,department__in=dept_1).values('designation','empno')
                for i in alldesig:
                    hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
                    if len(hq)>0:
                        name=hq[0]['empname']
                        if hq[0]['empmname'] is not None:
                            name=name+' '+hq[0]['empmname']
                        if hq[0]['emplname'] is not None:
                            name=name+' '+hq[0]['emplname']
                        hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
            # elif div_1!=[] and dept_1!=[]:
            #     div=models.railwayLocationMaster.objects.filter(parent_location_code__in=rly_1,location_code__in=div_1).values('rly_unit_code')
            #     alldesig=models.Level_Desig.objects.filter(rly_unit_id__in=div,department__in=dept_1).values('designation','empno')
            #     for i in alldesig:
            #         hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
            #         if len(hq)>0:
            #             name=hq[0]['empname']
            #             if hq[0]['empmname'] is not None:
            #                 name=name+' '+hq[0]['empmname']
            #             if hq[0]['emplname'] is not None:
            #                 name=name+' '+hq[0]['emplname']
            #             hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
            # elif div_1!=[] and dept_1==[]:
            #     div=models.railwayLocationMaster.objects.filter(parent_location_code__in=rly_1,location_code__in=div_1).values('rly_unit_code')
            #     alldesig=models.Level_Desig.objects.filter(rly_unit_id__in=div).values('designation','empno')
            #     for i in alldesig:
            #         hq=list(m1.empmast.objects.filter(empno=i['empno']).values('empname','empmname','emplname'))
            #         if len(hq)>0:
            #             name=hq[0]['empname']
            #             if hq[0]['empmname'] is not None:
            #                 name=name+' '+hq[0]['empmname']
            #             if hq[0]['emplname'] is not None:
            #                 name=name+' '+hq[0]['emplname']
            #             hqwise.append({'empname':name,'empno':i['empno'], 'desig_longdesc':i['designation']})
        context={
           'hqwise':hqwise,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)

def division_by_rly1(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.getlist('rly_1[]')
        if rly_1 == []:
            division=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code')
        else:
            division=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION'),parent_location_code__in=rly_1).order_by('location_code').values('location_code').distinct('location_code'))
        l=[]
        for i in division:
            l.append(i['location_code'])
        context={
            'division':l,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)


# niyati 150622 end     

#vishnu  location searching function
def search_location(request):
    
    
    # if request.method== 'POST':
    #     person = request.POST['person']
    #     print(person)
        
    #     des_location=models.MyUser.objects.filter(username__icontains=person )
    #     print('des_location', des_location)
    #     return render(request,'keyword_location_search.html', {'des_location':des_location})
    # else:
    #     person = False
    # all_location=models.railwayLocationMaster.objects.all()
        
    #     print('HELLO')
        
    #     # all_location=models.railwayLocationMaster.objects.none()
    # else:
    #     all_unit=models.railwayLocationMaster.objects.filter(rly_unit_code__icontains=query)
    #     all_location_code=models.railwayLocationMaster.objects.filter(location_code__icontains=query)
    #     all_location_type=models.railwayLocationMaster.objects.filter(location_type__icontains=query)
    #     all_location=all_unit.union(all_location_code).union(all_location_type)
    # # if all_location.count()== 0:
    #     messages.warning(request, "No search result found. Please refine your query ")
    
    #searching filter data
    # insp = []
    # if request.method == 'POST':
    #     q=request.POST.get('location')
    #     q1=request.POST.get('location1')
    #     multiple_q=Q(Q(location_description__contains=q) | Q(parent_location_code__contains=q1))
    #     insp=models.railwayLocationMaster.objects.filter(multiple_q, location_type__in=['DIV','ZR']).values('location_code','location_type','last_update','rly_unit_code')
    #     print('ghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh', insp)
    # else:
    #     print('hehhhhhhhhhhhhhhhhhhhhhh')
        
    #Find railway location/Zone
    list1=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    
    list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name')
    list6=[]
    for i in list5:
        # print(i['department_name'],'_________')
        list6.append(i['department_name'])
    
    list7=models.Level_Desig.objects.all().values('designation')
    list8=[]
    for i in list7:
        # print(i['designation'],'_________')
        list8.append(i['designation'])

    if request.method== 'POST':
        query = request.POST['query']
        print(query)
        que=Q()
        for word in query.split():
            que &=Q(observation__icontains=word)
        
        des_location=m1.Item_details.objects.filter(que)
        # par_location=models.railwayLocationMaster.objects.filter()
        # all_location=des_location.union(par_location)
        # query=[]
        print('des_location', des_location)
        return render(request,'keyword_location_search.html', {'des_location':des_location})
    else:
        query = False
    
    
    #Find division
    # ins=[]
    # if request.method =="POST":
    #     s=request.POST.get('location')
    #     list3=models.railwayLocationMaster.objects.filter(location_type='DIV', parent_location_code=s).values('location_code', 'parent_location_code')
    #     list4=[]
    #     for i in list3:
    #         print(i['location_code'],'_________')
    #         list4.append(i['location_code'])
    #     print('dhhddddddddddddddddddd',ins)
    # else:
    #     print('hhhhhhhhhhhhhh',ins)
        
    #find all list data 
    # insp=models.Level_Desig.objects.filter(rly_unit__location_type__in=['DIV', 'ZR']).values('cat_id','designation','rly_unit__location_code','rly_unit__location_type','rly_unit__last_update','rly_unit__rly_unit_code','department_code__department_name')
    # insp=models.Level_Desig.objects.all().values('cat_id','rly_unit__location_type','designation','rly_unit__last_update','department_code__department_name')
    # print("insp",insp)
    
    design=m1.Item_details.objects.all().values('item_no','inspection_no__inspection_note_no','modified_on','observation','inspection_no__division','inspection_no__zone')
    
    context={'zone':list2,'division':list4,'dept':list6, 'desi':list8,  'design':design }
    return render(request, 'search_location.html', context)


def keyword_location_search(request):
    if request.method== 'POST':
        query = request.POST.get('query')
        que=Q()
        for word in query.split():
            que &=Q(observation__icontains=word)
        des_location=list(m1.Item_details.objects.filter(que).values('modified_by','inspection_no_id__inspection_note_no','observation','modified_on','inspection_no_id__dept'))
        print(des_location)
        # des_location=list(m1.Item_details.objects.filter().values('modified_on'))
        for i in range(len(des_location)):
            if des_location[i]['modified_on']!=None:
                x=des_location[i]['modified_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
                des_location[i].update({'modified_on':x})
        #des_location=m1.Item_details.objects.filter(Q(observation__icontains=query) |Q(item_no__icontains=query) |Q(inspection_no__division__icontains=query) |Q(inspection_no__zone__icontains=query) )
        # render(request,'keyword_location_search.html', {'des_location':des_location})
        context={'des_location':des_location, 'query':query}

        return render(request,'keyword_location_search.html',context )
    else:
        return render(request,'keyword_location_search.html')
        
    

def search_locat_ajax(request):
    try:
        if request.method== 'GET' and request.is_ajax():
            grou=request.GET.get("group")
            ins=list(models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=grou).values('location_code', 'rly_unit_code'))
            return JsonResponse({'ins':ins}, safe=False)
        return JsonResponse({'success':False}, status=400)
    except Exception as e:
        print(e)
        
    
def search_desig_ajax(request):
    try:
        if request.method== 'GET' and request.is_ajax():
            grou=request.GET.get("groupss")
            ins=list(models.Level_Desig.objects.filter(designation_code=grou).values('designation'))
            return JsonResponse({'ins':ins}, safe=False)
        return JsonResponse({'success':False}, status=400)
    except Exception as e:
        print(e)



def fetch_desig_ajax(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            location_code=request.GET.get("location_code")
            location_type=request.GET.get("location_type")
            formsss=models.railwayLocationMaster.objects.get(rly_unit_code=int(location_type))
            dept=request.GET.get("dept")
            list_dept=models.departMast.objects.get(department_name=dept)
            print(list_dept.department_name)
        
            inspected_on=request.GET.get('inspected_on')
            print(inspected_on)
            status=request.GET.get('status')
            print(status)
            
            mydata={}
            
            grou=(location_code, formsss.location_code, list_dept.department_name, inspected_on, status)
            print(grou,'tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')
            ins=list(m1.Inspection_details.objects.filter(zone=location_code, division=formsss.location_code, dept=list_dept.department_name ).values('inspection_no','inspection_note_no','dept','division','zone','created_on','inspected_on'))
                     
            #ins=list(m1.Inspection_details.objects.filter( Q(zone=location_code) | Q(division=formsss.location_code) | Q(dept=list_dept.department_name) ).values('inspection_no','inspection_note_no','dept','division','zone','created_on','inspected_on'))
            for i in range(len(ins)):
                if ins[i]['inspected_on']!=None:
                    x=ins[i]['inspected_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
                    ins[i].update({'inspected_on':x})
            #print(ins, 'inspection_no')
            
            # ins_no=list(m1.Inspection_details.objects.filter(zone=location_code, location=location_type,dept=dept,).values('inspection_no'))
            for i in ins:
                
                # ins_no=list(m1.Item_details.objects.filter(inspection_no=i['inspection_no']).values('observation','inspection_no_id__zone','inspection_no_id__dept', 'inspection_no_id__division', 'inspection_no_id__location','inspection_no_id__inspected_on','inspection_no_id__created_on','inspection_no_id__inspection_no','inspection_no_id__inspection_note_no'))
                # print(ins_no, 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
                mydata.update({'ins':ins,'grou':grou,'location_code':location_code, 'location_type':location_type,'dept':dept,})
            print(mydata,'444444444444444444444444444444444444444444444444444444')
            return JsonResponse(ins, safe=False)
        return JsonResponse({'success':False}, status=400)
    except Exception as e:
        print(e)




from django.template.loader import get_template
from xhtml2pdf import pisa

from xhtml2pdf import pisa

def search_location_detail(request, pk):
    info=list(m1.Inspection_details.objects.filter(inspection_no=pk).values().distinct())
    #convert date dd-mm-yyyy
    for i in range(len(info)):
        if info[i]['inspected_on']!=None:
            x=info[i]['inspected_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
            info[i].update({'inspected_on':x})
    
    # pdf generate code
    # inspectionDetails=m1.Inspection_details.objects.filter(inspection_no=pk)
    # itemDetails=m1.Item_details.objects.filter(inspection_no=inspectionDetails[0].inspection_no)
    
    # print(itemDetails[0].observation)
    

    obj={}
    total=1
    for m2 in info:
        #convert date dd-mm-yyyy
        # x=m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].inspected_on
        # x=x.strftime('%d'+'-'+'%m'+'-'+'%Y')
        # inspectionDetails=m1.Inspection_details.objects.filter(inspection_no=pk)
        # itemDetails=m1.Item_details.objects.filter(inspection_no=inspectionDetails[0].inspection_no)
        #print(itemDetails[0].observation)
    
        
        # print(itemDetails[0].modified_on)
        
        temdata = {str(total):{"inspection_no":m2['inspection_no'], 
                               'inspection_note_no':m2['inspection_note_no'],
                            #    'inspection_officer':m2['inspection_officer'],
                               'zone':m2['zone'],
                            #    'observation':itemDetails[0].observation,
                            #    'modified_on':itemDetails[0].modified_on,
                               'division':m2['division'],
                               'location':m2['location'],
                               'inspected_on':m2['inspected_on'],
                               'modified_on':m2['modified_on']}}
        print(temdata, 'gfggggggggggggggggggggggggggggggggg')
        
    
        
        obj.update(temdata)
        total=total+1
        # print(temdata,"********************") 
    
    # print(obj,'tyyytytytytytytytytyty')
    lent=len(obj)
    # print(lent, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    context={'info':info, 'obj': obj, 'lent':lent,}
    pdf=render_to_pdf('search_location_detail.html', context) 
    return HttpResponse(pdf, content_type='application/pdf')


def search_list_created_checklist(request):
    obj=m1.Inspection_Checklist.objects.filter().values('checklist_id', 'checklist_title','inspection_type','status','created_by','created_on','delete_flag')[::-1]
    # print(obj)
    for i in range(len(obj)):
        if obj[i]['created_on']!=None:
            x=obj[i]['created_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
            obj[i].update({'created_on':x})
            
    context={'obj':obj}
    template_name='search_list_created_checklist.html'
        
    return render(request, template_name, context)



from .forms import *
import  json



def search_createchecklist(request):
    if request.method =='POST':
        # import pdb
        # pdb.set_trace()
        checklist_title=request.POST.get('checklist_title')
        print(checklist_title)
        inspection_type=request.POST.get('inspection_type')
        print(inspection_type)
        activities=request.POST.getlist('activities')
        print(activities)
        status=request.POST.get('draft')
        print(status)
        # activities = ['test1','test2']
        # contex={'checklist_title','inspection_type'}
        
        createchecklist=m1.Inspection_Checklist(checklist_title=checklist_title, inspection_type=inspection_type, status=status)
        
        createchecklist.save()
        print(createchecklist)
        # inspection_Activity
        for i in range(len(activities)):
            inspection_Activity=m1.Inspection_Activity(activities=activities[i])
            inspection_Activity.checklist_id=Inspection_Checklist.objects.get(checklist_id=createchecklist.checklist_id)
            inspection_Activity.save()
        
        return redirect('/search_list_created_checklist/')
 
    return render(request, 'search_createchecklist.html', {"INSPECTION_TYPE":INSPECTION_TYPE })


def search_editchecklist(request, pk):   
    print('viiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii') 
    inspection_Checklist=m1.Inspection_Checklist.objects.get(checklist_id=pk)
    
    ass=m1.Inspection_Activity.objects.filter(checklist_id=int(inspection_Checklist.checklist_id)).values('activity_id','activities')
    pk_list = []
    for ct in ass:
        pk_list.append(ct)
        #print(pk_list, 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
    
    if pk:
        if request.method =='POST':
            checklist_title=request.POST.get('checklist_title')
            inspection_type=request.POST.get('inspection_type')
            activities=request.POST.getlist('activities')
            print(activities, 'chessssssssssssssssssssssssss')
            status=request.POST.get('draft')
            obj_update = m1.Inspection_Checklist(checklist_id=pk,
                                        checklist_title=checklist_title, 
                                        inspection_type=inspection_type, 
                                        status=status)
            obj_update.save()
            
            for i in range(len(activities)):
                inspection_Activity=m1.Inspection_Activity(activity_id=ass)
                inspection_Activity=m1.Inspection_Activity(activities=activities[i])
                inspection_Activity.checklist_id=Inspection_Checklist.objects.get(checklist_id=obj_update.checklist_id)
                inspection_Activity.save()
                
            # for i in range(len(activities)):
            #     print(pk_list[i],11111)
            #     inspection_Activity=models.Inspection_Activity(activity_id=child_table[i])
            #     inspection_Activity.activities=activities[i]
            #     inspection_Activity.checklist_id=inspection_Checklist
            #     inspection_Activity.save()
            
            #child_table=models.Inspection_Activity.objects.filter(checklist_id=int(inspection_Checklist.checklist_id))#.values('activity_id','activities')
            
            print('hriiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
            return redirect('/search_list_created_checklist/')
    return render(request, 'search_createchecklist.html',{'ass':ass, 'inspection_Checklist':inspection_Checklist, "INSPECTION_TYPE":INSPECTION_TYPE })



def checklistReportPdf(request, activity_id):
    info=list(m1.Inspection_Activity.objects.filter(checklist_id=activity_id).values().distinct())
    
    #convert date dd-mm-yyyy
    for i in range(len(info)):
        if info[i]['created_on']!=None:
            x=info[i]['created_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
            info[i].update({'created_on':x})
    
 
    obj={}
    total=1
    for m2 in info:
       
        temdata = {str(total):{"activity_id":m2['activity_id'], 
                               'activities':m2['activities'],
                            #    'inspection_officer':m2['inspection_officer'],
                               'created_on':m2['created_on'],
                            #    'observation':itemDetails[0].observation,
                            #    'modified_on':itemDetails[0].modified_on,
                               'created_on':m2['created_on']}}
        print(temdata, 'gfggggggggggggggggggggggggggggggggg')
        
    
        
        obj.update(temdata)
        total=total+1
        # print(temdata,"********************") 
    
    # print(obj,'tyyytytytytytytytytyty')
    lent=len(obj)
    # print(lent, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    context={'info':info, 'obj': obj, 'lent':lent,}
    
    template_src='checklistReportPdf.html'
    return render_to_pdf(template_src, context)



def search_delete_flag(request, pk):
    flag=m1.Inspection_Checklist.objects.get(checklist_id=pk)
    flag.delete_flag=True
    flag.save()
    return HttpResponseRedirect('/search_list_created_checklist/')  

def search_delete_enable_flag(request, pk):
    flag=m1.Inspection_Checklist.objects.get(checklist_id=pk)
    flag.delete_flag=False
    flag.save()
    return HttpResponseRedirect('/search_list_created_checklist/') 

def search_checklist_detail(request, pk):
    info=list(m1.Inspection_Checklist.objects.filter(checklist_id=pk).values().distinct())
    #convert date dd-mm-yyyy
    for i in range(len(info)):
        if info[i]['created_on']!=None:
            x=info[i]['created_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
            info[i].update({'created_on':x})
            
    obj={}
    total=1
    for m2 in info:

        
        temdata = {str(total):{"checklist_id":m2['checklist_id'], 
                               'checklist_title':m2['checklist_title'],
                               'created_on':m2['created_on'],
                               'created_by':m2['created_by'],
                               
                               'inspection_type':m2['modified_on']}}
        print(temdata, 'gfggggggggggggggggggggggggggggggggg')
        obj.update(temdata)
        total=total+1
        # print(temdata,"********************") 
    
    # print(obj,'tyyytytytytytytytytyty')
    lent=len(obj)
    # print(lent, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    context={'info':info, 'obj': obj, 'lent':lent,}
    pdf=render_to_pdf('search_checklist_detail.html', context) 
    return HttpResponse(pdf, content_type='application/pdf')


def search_checklist_views(request, pk):
    inspection_Checklist=m1.Inspection_Checklist.objects.get(checklist_id=pk)
    print(inspection_Checklist)
    ass=m1.Inspection_Activity.objects.filter(checklist_id=int(inspection_Checklist.checklist_id)).values('activities')
    print(ass, 'ddddddddddddddddddddddddddddd') 
    
    
    return render(request, 'search_checklist_views.html',{'ass':ass,'inspection_Checklist':inspection_Checklist, "INSPECTION_TYPE":INSPECTION_TYPE })
    



def search_checklist_template(request):
    obj=m1.Inspection_Checklist.objects.filter(status='Finalized').values('checklist_id', 'checklist_title','inspection_type','status','created_by','created_on','delete_flag')[::-1]
    # print(obj)
    for i in range(len(obj)):
        if obj[i]['created_on']!=None:
            x=obj[i]['created_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
            obj[i].update({'created_on':x})
    
            
    context={'obj':obj}
    template_name='search_checklist_template.html'
        
    return render(request, template_name, context)


def search_checklist_template_report(request, pk):
    inspection_Checklist=m1.Inspection_Checklist.objects.get(checklist_id=pk)
    print(inspection_Checklist)
    ass=m1.Inspection_Activity.objects.filter(checklist_id=int(inspection_Checklist.checklist_id)).values('activities')
    ass_count=m1.Inspection_Activity.objects.filter(checklist_id=int(inspection_Checklist.checklist_id)).count()+1
    print(ass, 'ddddddddddddddddddddddddddddd')   
    empdata=list(m1.empmast.objects.values('empname','empno', 'desig_longdesc').distinct())
    # empdata=list(m1.empmast.objects.filter(myuser_id=request.user).values('empname','empno', 'desig_longdesc').distinct())

    desig_longdesc = empdata[0]['desig_longdesc']
    # print('ttttttttttttttttttttttttttttttttttttttttttttttttttttttt', desig_longdesc)
    list1=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
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
    
    context={
        'Zone':list2 ,
        'division':list4,
        'marked_to':list5,
        'department':list6,
        'desig': desig_longdesc,
        'inspection_Checklist':inspection_Checklist,
        'ass':ass,
        'ass_count': ass_count,
    
        }
    
    return render(request, 'search_checklist_template_report.html',context)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def search_checklist_template_ajax(request):
    if request.method== 'POST' and request.is_ajax():
        ob=request.POST.get("obs_data")
        obs_good=request.POST.get('obs_good')
        obs_notes=request.POST.get('obs_notes')
        obs_award=request.POST.get('obs_award')
        date=request.POST.get('date')
        # railway saves
        from datetime import datetime
        rly=request.POST.get('zone')
        div=request.POST.get('division')
        dept=request.POST.get('department')
        loc=request.POST.get('location')
        insp_date=request.POST.get('inspection_date')
        title=request.POST.get('titleinsp')
        print(title,'111111111111111111111111')
        #inspection_no=request.POST.get('inspection_no')
        btnValues=request.POST.get('btnValues')
        
        # checklist_id=request.POST.get('checklist_id')
        if btnValues == 'Save as draft':
            inspect_date = datetime.strptime(insp_date, '%d-%m-%Y').strftime('%Y-%m-%d')
            print(inspect_date, 'ddddddddddddyyyyyyyyyyyyyyyyyyyyymmmmmmmmmmmmmmmmm')
            m1.Inspection_details.objects.create(inspection_title=title, zone=rly,division=div,dept=dept,location=loc,inspected_on=inspect_date,item_type="Chk")
            inspection_id=m1.Inspection_details.objects.all().last().inspection_no
        print(date, 'dddddddddddddddddddddddddddddddd')
        # ojb1 = m1.Inspection_Activity.objects.filter(checklist_id_id='checklist_id_id')
        # for i in ojb1:
            # obj2=m1.Inspection_Activity.objects.filter(checklist_id=i.checklist_id)
            # print(obj2) 
            
            # print(i)
            # m1.Item_details.objects.create(checklist_id=i.checklist_id)
        data = json.loads(ob)
        for i in data:
            print(i, 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
            date_change=datetime.strptime(i['targetdate'], '%d-%m-%Y').strftime('%Y-%m-%d')
            print(date_change)
            m1.Item_details.objects.create(observation=i['obser'], target_date=date_change, type='CL', status='Draft',inspection_no_id=inspection_id)
        m1.Item_details.objects.create(observation=obs_good, type='GW', status='Draft',inspection_no_id=inspection_id)
        m1.Item_details.objects.create(observation=obs_notes, type='OT', status='Draft', inspection_no_id=inspection_id)
        m1.Item_details.objects.create(observation=obs_award, type='A', status='Draft',inspection_no_id=inspection_id)
        print(title, rly,div,dept,loc)
        
        
        
        return JsonResponse({'success':True}, status=200)
    return JsonResponse({'success':False}, status=400)


@csrf_exempt
def search_checklist_template_submit_ajax(request):
    if request.method== 'POST' and request.is_ajax():
        ob=request.POST.get("obs_data")
        obs_good=request.POST.get('obs_good')
        obs_notes=request.POST.get('obs_notes')
        obs_award=request.POST.get('obs_award')
        date=request.POST.get('date')
        
        # railway saves
        from datetime import datetime
        rly=request.POST.get('zone')
        div=request.POST.get('division')
        dept=request.POST.get('department')
        print(dept, 'depart sssssssssssssssss')
        loc=request.POST.get('location')
        insp_date=request.POST.get('inspection_date')
        print(insp_date, 'date..............................not none--------------------')
        title=request.POST.get('titleinsp')
        print(title,'111111111111111111111111')
        #inspection_no=request.POST.get('inspection_no')
        btnValues=request.POST.get('btnValues')
        print(btnValues, 'BTN VALUR FSGGS JSJS')

        if btnValues == 'Submit':
            inspect_date = datetime.strptime(insp_date, '%d-%m-%Y').strftime('%Y-%m-%d')
            print(inspect_date, 'ddddddddddddyyyyyyyyyyyyyyyyyyyyymmmmmmmmmmmmmmmmm')
            m1.Inspection_details.objects.create(inspection_title=title, zone=rly,division=div,dept=dept,location=loc,inspected_on=inspect_date, status_flag=1,item_type="Chk")
            inspection_id=m1.Inspection_details.objects.all().last().inspection_no
            
        print(date, 'dddddddddddddddddddddddddddddddd')
        
        data = json.loads(ob)
        for i in data:
            print(i, 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
            date_change=datetime.strptime(i['targetdate'], '%d-%m-%Y').strftime('%Y-%m-%d')
            print(date_change)
            m1.Item_details.objects.create(observation=i['obser'], target_date=date_change, type='CL', status='Finalized',inspection_no_id=inspection_id)
        m1.Item_details.objects.create(observation=obs_good, type='GW', status='Finalized',inspection_no_id=inspection_id)
        m1.Item_details.objects.create(observation=obs_notes, type='OT', status='Finalized',inspection_no_id=inspection_id)
        m1.Item_details.objects.create(observation=obs_award, type='A', status='Finalized',inspection_no_id=inspection_id)
        print(title, rly,div,dept,loc)
        
        return JsonResponse({'success':True}, status=200)
    return JsonResponse({'success':False}, status=400)
    



def checklist_locat_ajax(request):
    if request.method == "GET" or request.is_ajax():
        rly=request.GET.get('rly')
        print(rly,'_________++++++++++++++++++++++________________')
          
        division=list(models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=rly).order_by('location_code').values('location_code').distinct('location_code'))
        l=[]
        for i in division:
            l.append(i['location_code'])
        print(l)    
        context={
            'division':l,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)


def checklist_autoFetchLocation_ajax(request):
    if request.method == 'GET' and request.is_ajax():
        list1=list(models.locationMaster.objects.values_list('city', flat=True).order_by('city').distinct('city'))
        # print(list1)
        return JsonResponse(list1, safe=False)
    return JsonResponse({'success': False})  





# def search_location_detail(request, pk):
   
#     info=list(m1.Item_details.objects.filter(item_no=pk).values().distinct())
#     # print(info,'shhhhhhhhhhhh')

    
#     #convert date dd-mm-yyyy
#     for i in range(len(info)):
#         if info[i]['modified_on']!=None:
#             x=info[i]['modified_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
#             info[i].update({'modified_on':x})
    
    
    
#     # pdf generate code

#     obj={}
#     total=1
#     for m2 in info:
#         #convert date dd-mm-yyyy
#         x=m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].inspected_on
#         x=x.strftime('%d'+'-'+'%m'+'-'+'%Y')
#         temdata = {str(total):{"item_no":m2['item_no'], 
#                                'inspection_note_no':m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].inspection_note_no,
#                                'inspection_officer':m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].inspection_officer,
#                                'zone':m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].zone,
#                                'location':m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].location,
#                                'division':m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].division,
#                                'inspected_on':x,
                               
#                                'observation':m2['observation'], 'modified_on':m2['modified_on']}}
#         # print(temdata, 'gfggggggggggggggggggggggggggggggggg')
        
    
        
#         obj.update(temdata)
#         total=total+1
#         # print(temdata,"********************") 
    
#     # print(obj,'tyyytytytytytytytytyty')
#     lent=len(obj)
#     # print(lent, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx')

#     context={'info':info, 'obj': obj, 'lent':lent,}
#     pdf=render_to_pdf('search_location_detail.html', context) 
#     return HttpResponse(pdf, content_type='application/pdf')
#     # return render(request, template_name, context)


# def fetch_desig_ajax(request):
#     try:
#         if request.method == 'GET' and request.is_ajax():
#             location_code=request.GET.get("location_code")
#             location_type=request.GET.get("location_type")
#             dept=request.GET.get("dept")
#             mydata={}
#             grou=(location_code, location_type, dept)
#             print(grou,'tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')
#             ins=list(m1.Inspection_details.objects.filter(zone=location_code).values('inspected_on'))
#             ins=list(m1.Inspection_details.objects.filter(zone=location_code).values('inspection_no','inspection_note_no','dept','division','zone','created_on','inspected_on'))
#             print(ins, 'inspection_no')
#             # ins_no=list(models.Inspection_details.objects.filter(zone=location_code, location=location_type,dept=dept,).values('inspection_no'))
#             for i in ins:
                
#                 ins_no=list(m1.Item_details.objects.filter(inspection_no=i['inspection_no']).values('observation','inspection_no_id__zone','inspection_no_id__dept', 'inspection_no_id__division', 'inspection_no_id__location','inspection_no_id__inspected_on','inspection_no_id__created_on','inspection_no_id__inspection_no','inspection_no_id__inspection_note_no'))
#                 print(ins_no, 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
#                 mydata.update({'ins':ins,'grou':grou,'location_code':location_code, 'location_type':location_type,'dept':dept,})
#             print(mydata)
#             return JsonResponse(ins, safe=False)
#         return JsonResponse({'success':False}, status=400)
#     except Exception as e:
#         print(e)


#end here vishnu

#bhart start
def view_inspection_draft(request):
    try:

        print("#########################")
        # result=list(m1.Item_details.objects.filter(status_flag=1).values('inspection_no_id','observation','item_title'))
        # result1=list(m1.Inspection_details.objects.filter(inspection_no=result[0]['inspection_no_id']).values('zone','dept','division'))
        # print(result,result1)
        context={
            # 'result':result,
            # 'zone':result1[0]['zone'],
            # 'dept':result1[0]['dept'],
            # 'division':result1[0]['division'],
        }
        return render(request, 'view_draft.html',context)
    except Exception as e:
        print("e==",e) 


#bharti end


def forgotPassword(request):
    try:
        if request.method == "POST":
            _email = request.POST.get('email').strip()

            try:
                userObj = user.objects.get(email=_email)
                #print(userObj)
            except Exception as e:
                messages.error(request, 'Please enter registed email.')
                return HttpResponseRedirect('/rkvy_forgotPassword')

            email_context = {
                "email": userObj.email,
                'domain': 'railkvydev.indianrailways.gov.in',
                'site_name': 'Kaushal Vikas',
                "uid": urlsafe_base64_encode(force_bytes(userObj.pk)),
                "user": userObj,
                'token': default_token_generator.make_token(userObj),
                'protocol': 'http',
            }
            email_template_name = "accounts/email_forgotPassword_body.txt"
            email_body = render_to_string(email_template_name, email_context)
            try:
                #print("trying to send mail")
                #print(userObj.email)
                try:
                    # send_mail("Verify Your Mail", email_body, 'crisdlwproject@gmail.com',
                    #          [ '{userObj.email}'], fail_silently=False)


                    #saud faisal (28-08-2021) -----
                    subject="Reset password for RKVY login"
                    To=userObj.email
                    email_body1='<p>'+email_body+'</p>'
                    MailSend(subject,email_body1,To)
                    #end here
                    return HttpResponse('Verification Email has been successfully sent.(see also spam folder)')
                except:
                    print("error on sending")
                    messages.error(
                        request, 'Verification Email failed. Please Try Again.')
            except:
                messages.error(
                    request, 'Something went wrong.')
            return HttpResponseRedirect('/forgotPassword')

        return render(request, "forgotPassword.html")
    except Exception as e: 
       print(e)


def passwordVerification(request):
    username=request.POST.get('username2')
    email2=user.objects.filter(username=username)[0].email
    print('email2')
    return render(request, "resetPassword.html",{'validLink': True,'email':email2, })
    
def forgotPasswordVerification(request):
    try:
        try:
            print('00000000')
            print(request.POST.get('email2'))
            userObj = user.objects.get(email= request.POST.get('email2'))
            print(userObj)
            
        except(TypeError, ValueError, OverflowError, user.DoesNotExist):
            print("%&^%&^%&^%&^@#%&^@#%&^@%#&@%#&")
            userObj = None

        if userObj is not None:
            print('1111')

            # return HttpResponseRedirect('/reset_password')
            if request.method == "POST":
                try:
                    _password = request.POST.get('new_password')
                    userObj.set_password(_password)
                    userObj.save()
                    
                    messages.success(request, "Password Updated Successfully")
                except Exception as e:
                    print(e)
                    messages.error(request, "Password Change Failed.")
                return HttpResponseRedirect('/login')

            return render(request, "resetPassword.html", {'validLink': True, })
        else:
            return HttpResponse('Email not registered')
    except Exception as e: 
        print(e)

# Aman start
def new_page(request):
    return render(request,'new_page.html')

def new_page2(request):
    return render(request,'new_page2.html')

def new_data(request):
    railway = request.GET.get('railway')
    s = request.GET.get('status')
    sd = request.GET.get('sd')
    ed = request.GET.get('ed')
    print(railway,s)
    data=[]
    if int(s)==0:
        print("yes")
        flag=0
        t = m1.Inspection_details.objects.filter(zone=railway,inspected_on__gte=sd,inspected_on__lte=ed,status_flag=1).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag','inspection_no')
        for i in t:
            if i['status_flag']!=None:
                temp={}
                temp['inno']=i['inspection_no']
                temp['ins_no']=i['inspection_note_no']
                temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
                temp['desig']=i['inspection_officer']
                t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
                temp['railway']=t1[0]['location_description']
                t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
                temp['division']=t1[0]['location_description']
                temp['dept']=i['dept']
                t1=m1.Item_details.objects.filter(inspection_no=i['inspection_no']).values()
                for k in t1:
                    if k['status_flag']==1:
                        flag=1
                    elif k['status_flag']==2:
                        flag=2
                        break
                    elif k['status_flag']==4:
                        flag=3
                if flag==1:
                    temp['status']="Pending Compliance"
                elif flag==2:
                    temp['status']="Partial Compliance"
                elif flag==3:
                    temp['status']="Closed"
                flag=0
                data.append(temp)
    elif int(s)==1:
        t = m1.Inspection_details.objects.filter(zone=railway,status_flag=s,inspected_on__gte=sd,inspected_on__lte=ed).values('inspection_no','inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Pending Compliance"
            data.append(temp)
    elif int(s)==2:
        t = m1.Inspection_details.objects.filter(zone=railway,status_flag=s,inspected_on__gte=sd,inspected_on__lte=ed).values('inspection_no','inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Partial Compliance"
            data.append(temp)
    elif int(s)==3:
        t = m1.Inspection_details.objects.filter(zone=railway,status_flag=s,inspected_on__gte=sd,inspected_on__lte=ed).values('inspection_no','inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Closed"
            data.append(temp)
    print(len(temp))
    context={'data':data}
    return JsonResponse(context,safe=False)

def new_data1(request):
    railway = request.GET.get('div')
    s = request.GET.get('status')
    sd = request.GET.get('sd')
    ed = request.GET.get('ed')
    print(railway,s)
    data=[]
    if int(s)==0:
        print("yes")
        flag=0
        t = m1.Inspection_details.objects.filter(division=railway,inspected_on__gte=sd,inspected_on__lte=ed).values('inspection_no','inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        print(t)
        for i in t:
            if i['status_flag']!=None:
                temp={}
                temp['inno']=i['inspection_no']
                temp['ins_no']=i['inspection_note_no']
                temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
                temp['desig']=i['inspection_officer']
                t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
                temp['railway']=t1[0]['location_description']
                t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
                temp['division']=t1[0]['location_description']
                temp['dept']=i['dept']
                t1=m1.Item_details.objects.filter(inspection_no=i['inspection_no']).values()
                for k in t1:
                    if k['status_flag']==1:
                        flag=1
                    elif k['status_flag']==2:
                        flag=2
                        break
                    elif k['status_flag']==4:
                        flag=3
                if flag==1:
                    temp['status']="Pending Compliance"
                elif flag==2:
                    temp['status']="Partial Compliance"
                elif flag==3:
                    temp['status']="Closed"
                flag=0
                data.append(temp)
    elif int(s)==1:
        t = m1.Inspection_details.objects.filter(division=railway,status_flag=s,inspected_on__gte=sd,inspected_on__lte=ed).values('inspection_no','inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Pending Compliance"
            data.append(temp)
    elif int(s)==2:
        t = m1.Inspection_details.objects.filter(division=railway,status_flag=s,inspected_on__gte=sd,inspected_on__lte=ed).values('inspection_no','inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Partial Compliance"
            data.append(temp)
    elif int(s)==3:
        t = m1.Inspection_details.objects.filter(division=railway,status_flag=s,inspected_on__gte=sd,inspected_on__lte=ed).values('inspection_no','inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Closed"
            data.append(temp)
    context={'data':data}
    return JsonResponse(context,safe=False)

def new_data2(request):
    railway = request.GET.get('dept')
    s = request.GET.get('status')
    sd = request.GET.get('sd')
    ed = request.GET.get('ed')
    print(railway,s)
    data=[]
    if int(s)==0:
        print("yes")
        flag=0
        t = m1.Inspection_details.objects.filter(dept=railway,inspected_on__gte=sd,inspected_on__lte=ed,status_flag=1).values()
        print(t)
        for i in t:
            if i['status_flag']!=None:
                temp={}
                temp['inno']=i['inspection_no']
                temp['ins_no']=i['inspection_note_no']
                temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
                temp['desig']=i['inspection_officer']
                t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
                temp['railway']=t1[0]['location_description']
                t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
                temp['division']=t1[0]['location_description']
                temp['dept']=i['dept']
                t1=m1.Item_details.objects.filter(inspection_no=i['inspection_no']).values()
                for k in t1:
                    if k['status_flag']==1:
                        flag=1
                    elif k['status_flag']==2:
                        flag=2
                        break
                    elif k['status_flag']==4:
                        flag=3
                if flag==1:
                    temp['status']="Pending Compliance"
                elif flag==2:
                    temp['status']="Partial Compliance"
                elif flag==3:
                    temp['status']="Closed"
                flag=0
                data.append(temp)
    elif int(s)==1:
        t = m1.Inspection_details.objects.filter(dept=railway,status_flag=s,inspected_on__gte=sd,inspected_on__lte=ed).values()
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Pending Compliance"
            data.append(temp)
    elif int(s)==2:
        t = m1.Inspection_details.objects.filter(dept=railway,status_flag=s,inspected_on__gte=sd,inspected_on__lte=ed).values()
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Partial Compliance"
            data.append(temp)
    elif int(s)==3:
        t = m1.Inspection_details.objects.filter(dept=railway,status_flag=s,inspected_on__gte=sd,inspected_on__lte=ed).values()
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Closed"
            data.append(temp)
    context={'data':data}
    return JsonResponse(context,safe=False)

def new_data3(request):
    railway = request.GET.get('desig')
    s = request.GET.get('status')
    sd = request.GET.get('sd')
    ed = request.GET.get('ed')
    print(railway,s)
    data=[]
    if int(s)==0:
        print("yes")
        flag=0
        t1 = models.Level_Desig.objects.filter(designation=railway).values('department_code')
        t = m1.Inspection_details.objects.filter(inspection_officer=t1[0]['department_code'],inspected_on__gte=sd,inspected_on__lte=ed,status_flag=1).values()
        print(t)
        for i in t:
            if i['status_flag']!=None:
                temp={}
                temp['inno']=i['inspection_no']
                temp['ins_no']=i['inspection_note_no']
                temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
                temp['desig']=railway
                t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
                temp['railway']=t1[0]['location_description']
                t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
                temp['division']=t1[0]['location_description']
                temp['dept']=i['dept']
                t1=m1.Item_details.objects.filter(inspection_no=i['inspection_no']).values()
                for k in t1:
                    if k['status_flag']==1:
                        flag=1
                    elif k['status_flag']==2:
                        flag=2
                        break
                    elif k['status_flag']==4:
                        flag=3
                if flag==1:
                    temp['status']="Pending Compliance"
                elif flag==2:
                    temp['status']="Partial Compliance"
                elif flag==3:
                    temp['status']="Closed"
                flag=0
                data.append(temp)
    elif int(s)==1:
        t1 = models.Level_Desig.objects.filter(designation=railway).values('department_code')
        t = m1.Inspection_details.objects.filter(inspection_officer=t1[0]['department_code'],inspected_on__gte=sd,inspected_on__lte=ed,status_flag=s).values()
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=railway
            t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Pending Compliance"
            data.append(temp)
    elif int(s)==2:
        t1 = models.Level_Desig.objects.filter(designation=railway).values('department_code')
        t = m1.Inspection_details.objects.filter(inspection_officer=t1[0]['department_code'],status_flag=s,inspected_on__gte=sd,inspected_on__lte=ed).values()
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=railway
            t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Partial Compliance"
            data.append(temp)
    elif int(s)==3:
        t1 = models.Level_Desig.objects.filter(designation=railway).values('department_code')
        t = m1.Inspection_details.objects.filter(inspection_officer=t1[0]['department_code'],status_flag=s,inspected_on__gte=sd,inspected_on__lte=ed).values()
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=railway
            t1=models.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=models.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Closed"
            data.append(temp)
    context={'data':data}
    return JsonResponse(context,safe=False)

def new_data20(request):
    railway = request.GET.get('railway')
    s = request.GET.get('status')
    sd = request.GET.get('sd')
    ed = request.GET.get('ed')
    print(railway,s)
    data=[]
    if int(s)==0:
        print("yes")
        t = m1.Item_details.objects.filter(inspection_no__zone=railway,inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed).values('item_no','observation','status_flag','target_date','inspection_no')
        print(t)
        for i in t:
            if i['status_flag']!=None:
                temp={}
                temp['inno']=i['inspection_no']
                temp['item_no']=i['item_no']
                temp['target']=i['target_date']
                temp['obs']=i['observation']
                t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
                temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
                t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
                temp['railway']=t2[0]['location_description']
                t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
                temp['division']=t3[0]['location_description']
                temp['dept']=t1[0]['dept']
                if i['status_flag']==1:
                    temp['status']="Pending Compliance"
                elif i['status_flag']==2:
                    temp['status']="Partial Compliance"
                elif i['status_flag']==3:
                    temp['status']="Closed"
                data.append(temp)
    elif int(s)==1:
        t = m1.Item_details.objects.filter(inspection_no__zone=railway,inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed,status_flag=s).values('item_no','observation','status_flag','target_date','inspection_no')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['item_no']=i['item_no']
            temp['target']=i['target_date']
            temp['obs']=i['observation']
            t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
            temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
            t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
            temp['railway']=t2[0]['location_description']
            t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
            temp['division']=t3[0]['location_description']
            temp['dept']=t1[0]['dept']
            temp['status']="Pending Compliance"
            data.append(temp)
    elif int(s)==2:
        t = m1.Item_details.objects.filter(inspection_no__zone=railway,inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed,status_flag=s).values('item_no','observation','status_flag','target_date','inspection_no')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['item_no']=i['item_no']
            temp['target']=i['target_date']
            temp['obs']=i['observation']
            t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
            temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
            t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
            temp['railway']=t2[0]['location_description']
            t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
            temp['division']=t3[0]['location_description']
            temp['dept']=t1[0]['dept']
            temp['status']="Partial Compliance"
            data.append(temp)
    elif int(s)==3:
        t = m1.Item_details.objects.filter(inspection_no__zone=railway,inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed,status_flag=s).values('item_no','observation','status_flag','target_date','inspection_no')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['item_no']=i['item_no']
            temp['target']=i['target_date']
            temp['obs']=i['observation']
            t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
            temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
            t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
            temp['railway']=t2[0]['location_description']
            t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
            temp['division']=t3[0]['location_description']
            temp['dept']=t1[0]['dept']
            data.append(temp)
    context={'data':data}
    return JsonResponse(context,safe=False)

def new_data21(request):
    railway = request.GET.get('railway')
    s = request.GET.get('status')
    sd = request.GET.get('sd')
    ed = request.GET.get('ed')
    print(railway,s)
    data=[]
    if int(s)==0:
        print("yes")
        t = m1.Item_details.objects.filter(inspection_no__division=railway,inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed).values('item_no','observation','status_flag','target_date','inspection_no')
        print(t)
        for i in t:
            if i['status_flag']!=None:
                temp={}
                temp['inno']=i['inspection_no']
                temp['item_no']=i['item_no']
                temp['target']=i['target_date']
                temp['obs']=i['observation']
                t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
                temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
                t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
                temp['railway']=t2[0]['location_description']
                t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
                temp['division']=t3[0]['location_description']
                temp['dept']=t1[0]['dept']
                if i['status_flag']==1:
                    temp['status']="Pending Compliance"
                elif i['status_flag']==2:
                    temp['status']="Partial Compliance"
                elif i['status_flag']==3:
                    temp['status']="Closed"
                data.append(temp)
    elif int(s)==1:
        t = m1.Item_details.objects.filter(inspection_no__division=railway,inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed,status_flag=s).values('item_no','observation','status_flag','target_date','inspection_no')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['item_no']=i['item_no']
            temp['target']=i['target_date']
            temp['obs']=i['observation']
            t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
            temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
            t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
            temp['railway']=t2[0]['location_description']
            t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
            temp['division']=t3[0]['location_description']
            temp['dept']=t1[0]['dept']
            temp['status']="Pending Compliance"
            data.append(temp)
    elif int(s)==2:
        t = m1.Item_details.objects.filter(inspection_no__division=railway,inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed,status_flag=s).values('item_no','observation','status_flag','target_date','inspection_no')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['item_no']=i['item_no']
            temp['target']=i['target_date']
            temp['obs']=i['observation']
            t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
            temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
            t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
            temp['railway']=t2[0]['location_description']
            t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
            temp['division']=t3[0]['location_description']
            temp['dept']=t1[0]['dept']
            temp['status']="Partial Compliance"
            data.append(temp)
    elif int(s)==3:
        t = m1.Item_details.objects.filter(inspection_no__zone=railway,inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed,status_flag=s).values('item_no','observation','status_flag','target_date','inspection_no')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['item_no']=i['item_no']
            temp['target']=i['target_date']
            temp['obs']=i['observation']
            t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
            temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
            t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
            temp['railway']=t2[0]['location_description']
            t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
            temp['division']=t3[0]['location_description']
            temp['dept']=t1[0]['dept']
            data.append(temp)
    context={'data':data}
    return JsonResponse(context,safe=False)

def new_data22(request):
    railway = request.GET.get('railway')
    s = request.GET.get('status')
    sd = request.GET.get('sd')
    ed = request.GET.get('ed')
    print(railway,s)
    data=[]
    if int(s)==0:
        print("yes")
        t = m1.Item_details.objects.filter(inspection_no__dept=railway,inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed).values('item_no','observation','status_flag','target_date','inspection_no')
        print(t)
        for i in t:
            if i['status_flag']!=None:
                temp={}
                temp['inno']=i['inspection_no']
                temp['item_no']=i['item_no']
                temp['target']=i['target_date']
                temp['obs']=i['observation']
                t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
                temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
                t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
                temp['railway']=t2[0]['location_description']
                t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
                temp['division']=t3[0]['location_description']
                temp['dept']=t1[0]['dept']
                if i['status_flag']==1:
                    temp['status']="Pending Compliance"
                elif i['status_flag']==2:
                    temp['status']="Partial Compliance"
                elif i['status_flag']==3:
                    temp['status']="Closed"
                data.append(temp)
    elif int(s)==1:
        t = m1.Item_details.objects.filter(inspection_no__dept=railway,inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed,status_flag=s).values('item_no','observation','status_flag','target_date','inspection_no')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['item_no']=i['item_no']
            temp['target']=i['target_date']
            temp['obs']=i['observation']
            t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
            temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
            t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
            temp['railway']=t2[0]['location_description']
            t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
            temp['division']=t3[0]['location_description']
            temp['dept']=t1[0]['dept']
            temp['status']="Pending Compliance"
            data.append(temp)
    elif int(s)==2:
        t = m1.Item_details.objects.filter(inspection_no__dept=railway,inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed,status_flag=s).values('item_no','observation','status_flag','target_date','inspection_no')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['item_no']=i['item_no']
            temp['target']=i['target_date']
            temp['obs']=i['observation']
            t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
            temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
            t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
            temp['railway']=t2[0]['location_description']
            t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
            temp['division']=t3[0]['location_description']
            temp['dept']=t1[0]['dept']
            temp['status']="Partial Compliance"
            data.append(temp)
    elif int(s)==3:
        t = m1.Item_details.objects.filter(inspection_no__dept=railway,inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed,status_flag=s).values('item_no','observation','status_flag','target_date','inspection_no')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['item_no']=i['item_no']
            temp['target']=i['target_date']
            temp['obs']=i['observation']
            t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
            temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
            t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
            temp['railway']=t2[0]['location_description']
            t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
            temp['division']=t3[0]['location_description']
            temp['dept']=t1[0]['dept']
            data.append(temp)
    context={'data':data}
    return JsonResponse(context,safe=False)

def new_data23(request):
    railway = request.GET.get('railway')
    s = request.GET.get('status')
    sd = request.GET.get('sd')
    ed = request.GET.get('ed')
    print(railway,s)
    data=[]
    t1 = models.Level_Desig.objects.filter(designation=railway).values('department_code')
    if int(s)==0:
        t = m1.Item_details.objects.filter(inspection_no__inspection_officer=t1[0]['department_code'],inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed).values('item_no','observation','status_flag','target_date','inspection_no')
        print(t)
        for i in t:
            if i['status_flag']!=None:
                temp={}
                temp['inno']=i['inspection_no']
                temp['item_no']=i['item_no']
                temp['target']=i['target_date']
                temp['obs']=i['observation']
                t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
                temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
                t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
                temp['railway']=t2[0]['location_description']
                t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
                temp['division']=t3[0]['location_description']
                temp['dept']=t1[0]['dept']
                if i['status_flag']==1:
                    temp['status']="Pending Compliance"
                elif i['status_flag']==2:
                    temp['status']="Partial Compliance"
                elif i['status_flag']==3:
                    temp['status']="Closed"
                data.append(temp)
    elif int(s)==1:
        t = m1.Item_details.objects.filter(inspection_no__inspection_officer=t1[0]['department_code'],inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed,status_flag=s).values('item_no','observation','status_flag','target_date','inspection_no')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['item_no']=i['item_no']
            temp['target']=i['target_date']
            temp['obs']=i['observation']
            t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
            temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
            t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
            temp['railway']=t2[0]['location_description']
            t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
            temp['division']=t3[0]['location_description']
            temp['dept']=t1[0]['dept']
            temp['status']="Pending Compliance"
            data.append(temp)
    elif int(s)==2:
        t = m1.Item_details.objects.filter(inspection_no__inspection_officer=t1[0]['department_code'],inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed,status_flag=s).values('item_no','observation','status_flag','target_date','inspection_no')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['item_no']=i['item_no']
            temp['target']=i['target_date']
            temp['obs']=i['observation']
            t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
            temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
            t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
            temp['railway']=t2[0]['location_description']
            t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
            temp['division']=t3[0]['location_description']
            temp['dept']=t1[0]['dept']
            temp['status']="Partial Compliance"
            data.append(temp)
    elif int(s)==3:
        t = m1.Item_details.objects.filter(inspection_no__inspection_officer=t1[0]['department_code'],inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed,status_flag=s).values('item_no','observation','status_flag','target_date','inspection_no')
        for i in t:
            temp={}
            temp['inno']=i['inspection_no']
            temp['item_no']=i['item_no']
            temp['target']=i['target_date']
            temp['obs']=i['observation']
            t1 = m1.Inspection_details.objects.filter(inspection_no=i['inspection_no']).values('zone','division','dept','inspected_on')
            temp['ins_date']=t1[0]['inspected_on'].strftime("%d-%b-%Y")
            t2=models.railwayLocationMaster.objects.filter(location_code=t1[0]['zone']).values('location_description')
            temp['railway']=t2[0]['location_description']
            t3=models.railwayLocationMaster.objects.filter(location_code=t1[0]['division']).values('location_description')
            temp['division']=t3[0]['location_description']
            temp['dept']=t1[0]['dept']
            data.append(temp)
    context={'data':data}
    return JsonResponse(context,safe=False)


def dashboard(request):
    return render(request,'dashboard.html')
# connection = psycopg2.connect("dbname=200622 user=postgres password=9911772843")
def get_data(request):
    sd = request.GET.get('sd')
    ed = request.GET.get('ed')
    data=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_description','location_code').order_by('location_description')
    data1=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_description','location_code').order_by('location_description')
    data2=models.departMast.objects.values('department_name').distinct().order_by('department_name')
    data3=models.Level_Desig.objects.values('department_code','designation').distinct()
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    for i in data:
        temp={}
        c1=0
        c2=0
        c3=0
        flag=0
        t = m1.Inspection_details.objects.filter(zone=i['location_code'],inspected_on__gte=sd,inspected_on__lte=ed,status_flag=1).values()
        temp['count']=t.count()  
        for j in t:
            t1=m1.Item_details.objects.filter(inspection_no=j['inspection_no']).values()
            for k in t1:
                if k['status_flag']==1:
                    flag=1
                elif k['status_flag']==2:
                    flag=2
                    break
                elif k['status_flag']==4:
                    flag=3
            if flag==1:
                c1+=1
            elif flag==2:
                c2+=1
            elif flag==3:
                c3+=1
            flag=0
        temp['c1']=c3
        temp['c2']=c2
        temp['c3']=c1  
        temp['loc']=i['location_description']
        temp['id']=i['location_code']
        list1.append(temp)
    for i in data1:
        temp={}
        c1=0
        c2=0
        c3=0
        flag=0
        t = m1.Inspection_details.objects.filter(division=i['location_code'],inspected_on__gte=sd,inspected_on__lte=ed,status_flag=1).values()
        temp['count']=t.count()  
        for j in t:
            t1=m1.Item_details.objects.filter(inspection_no=j['inspection_no']).values()
            for k in t1:
                if k['status_flag']==1:
                    flag=1
                elif k['status_flag']==2:
                    flag=2
                    break
                elif k['status_flag']==4:
                    flag=3
            if flag==1:
                c1+=1
            elif flag==2:
                c2+=1
            elif flag==3:
                c3+=1
            flag=0
        temp['c1']=c3
        temp['c2']=c2
        temp['c3']=c1  
        temp['loc']=i['location_description']
        temp['id']=i['location_code']
        list2.append(temp)
    for i in data2:
        temp={}
        c1=0
        c2=0
        c3=0
        flag=0
        t = m1.Inspection_details.objects.filter(dept=i['department_name'],inspected_on__gte=sd,inspected_on__lte=ed,status_flag=1).values()
        temp['count']=t.count()  
        for j in t:
            t1=m1.Item_details.objects.filter(inspection_no=j['inspection_no']).values()
            for k in t1:
                if k['status_flag']==1:
                    flag=1
                elif k['status_flag']==2:
                    flag=2
                    break
                elif k['status_flag']==4:
                    flag=3
            if flag==1:
                c1+=1
            elif flag==2:
                c2+=1
            elif flag==3:
                c3+=1
            flag=0
        temp['c1']=c3
        temp['c2']=c2
        temp['c3']=c1  
        temp['loc']=i['department_name']
        list3.append(temp)
    for i in data3:
        temp={}
        c1=0
        c2=0
        c3=0
        flag=0
        t = m1.Inspection_details.objects.filter(inspection_officer=i['department_code'],inspected_on__gte=sd,inspected_on__lte=ed,status_flag=1).values()
        temp['count']=t.count()  
        for j in t:
            t1=m1.Item_details.objects.filter(inspection_no=j['inspection_no']).values()
            for k in t1:
                if k['status_flag']==1:
                    flag=1
                elif k['status_flag']==2:
                    flag=2
                    break
                elif k['status_flag']==4:
                    flag=3
            if flag==1:
                c1+=1
            elif flag==2:
                c2+=1
            elif flag==3:
                c3+=1
            flag=0
        temp['c1']=c3
        temp['c2']=c2
        temp['c3']=c1  
        temp['loc']=i['designation']
        list4.append(temp)
    context={
        'list1':list1,
        'list2':list2,
        'list3':list3,
        'list4':list4,
    }
    return JsonResponse(context, safe = False)

def get_data2(request):
    sd = request.GET.get('sd2')
    ed = request.GET.get('ed2')
    data=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_description','location_code').order_by('location_description')
    data1=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_description','location_code').order_by('location_description')
    data2=models.departMast.objects.values('department_name').distinct().order_by('department_name')
    data3=models.Level_Desig.objects.values('designation','department_code').distinct()
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    for i in data:
        temp={}
        t = m1.Item_details.objects.filter(inspection_no__zone=i['location_code'],inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed).values('status_flag')
        temp['count']=t.exclude(status_flag__in=[None,0]).count()
        temp['c1']=t.filter(status_flag=3).count()
        temp['c2']=t.filter(status_flag=2).count()
        temp['c3']=t.filter(status_flag=1).count()
        temp['loc']=i['location_description']
        temp['id']=i['location_code']
        list1.append(temp)
    for i in data1:
        temp={}
        t = m1.Item_details.objects.filter(inspection_no__division=i['location_code'],inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed).values('inspection_no')
        temp['count']=t.exclude(status_flag__in=[None,0]).count()
        temp['c1']=t.filter(status_flag=3).count()
        temp['c2']=t.filter(status_flag=2).count()
        temp['c3']=t.filter(status_flag=1).count()
        temp['loc']=i['location_description']
        temp['id']=i['location_code']
        list2.append(temp)
    for i in data2:
        temp={}
        t = m1.Item_details.objects.filter(inspection_no__dept=i['department_name'],inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed).values('inspection_no')
        temp['count']=t.exclude(status_flag__in=[None,0]).count()
        temp['c1']=t.filter(status_flag=3).count()
        temp['c2']=t.filter(status_flag=2).count()
        temp['c3']=t.filter(status_flag=1).count()
        temp['loc']=i['department_name'] 
        list3.append(temp)
    for i in data3:
        temp={}
        t = m1.Item_details.objects.filter(inspection_no__inspection_officer=i['department_code'],inspection_no__status_flag=1,inspection_no__inspected_on__gte=sd,inspection_no__inspected_on__lte=ed).values('inspection_no')
        temp['count']=t.exclude(status_flag__in=[None,0]).count()
        temp['c1']=t.filter(status_flag=3).count()
        temp['c2']=t.filter(status_flag=2).count()
        temp['c3']=t.filter(status_flag=1).count()
        temp['loc']=i['designation'] 
        list4.append(temp)
    context={
        'list1':list1,
        'list2':list2,
        'list3':list3,
        'list4':list4,
    }
    return JsonResponse(context, safe = False)

from datetime import timedelta

# Prashansa 290822

def dash_details(request):
    railway=request.GET.get('data')
    case=request.GET.get('data1')
    typei=request.GET.get('data2')
    color=request.GET.get('data3')
    print(railway,case,typei,color)
    user=request.user
    print(user)
    das_desig=models.Level_Desig.objects.filter(Q(official_email_ID=user.email)|Q(official_email_ID=user)).values('designation_code','department') 
    
    result=[]
    insp_data=[]
    c=0

    if typei=='Insp':
        obj4=models.railwayLocationMaster.objects.filter(location_code=railway).values('location_description')
        
        
        loc_multi=m1.Insp_multi_location.objects.filter(item=railway).values_list('inspection_no', flat=True)
        
        if color=='all':
            
            if case=='Total':
                insp_data = m1.Inspection_details.objects.filter(~Q(status_flag=0),inspection_officer=das_desig[0]['designation_code'],inspection_no__in=loc_multi).values()
            elif case=='Pending':
                insp_data = m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig[0]['designation_code'],inspection_no__in=loc_multi).values()
            elif case=='Closed':
                insp_data = m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig[0]['designation_code'],inspection_no__in=loc_multi).values()

        elif color=='0-3':
            now = datetime.today()
            prev = now - timedelta(days=90)
            if case=='Total':
                insp_data = m1.Inspection_details.objects.filter(~Q(status_flag=0),inspection_officer=das_desig[0]['designation_code'],inspected_on__gte=prev,inspection_no__in=loc_multi).values()
            elif case=='Pending':
                insp_data = m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig[0]['designation_code'],inspected_on__gte=prev,inspection_no__in=loc_multi).values()
            elif case=='Closed':
                insp_data = m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig[0]['designation_code'],inspected_on__gte=prev,inspection_no__in=loc_multi).values()
        elif color=='3-6':
            now = datetime.today()
            prev = now - timedelta(days=90)		     
            six=now - timedelta(days=180)
            if case=='Total':
                insp_data = m1.Inspection_details.objects.filter(~Q(status_flag=0),inspection_officer=das_desig[0]['designation_code'],inspected_on__gte=prev,inspected_on__lte=six,inspection_no__in=loc_multi).values()
            elif case=='Pending':
                insp_data = m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig[0]['designation_code'],inspected_on__gte=prev,inspected_on__lte=six,inspection_no__in=loc_multi).values()
            elif case=='Closed':
                insp_data = m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig[0]['designation_code'],inspected_on__gte=prev,inspected_on__lte=six,inspection_no__in=loc_multi).values()

        elif color=='>6':
            now = datetime.today()
            prev = now - timedelta(days=180)
            if case=='Total':
                insp_data = m1.Inspection_details.objects.filter(~Q(status_flag=0),inspection_officer=das_desig[0]['designation_code'],inspected_on__lte=prev,inspection_no__in=loc_multi).values()
            elif case=='Pending':
                insp_data = m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig[0]['designation_code'],inspected_on__lte=prev,inspection_no__in=loc_multi).values()
            elif case=='Closed':
                insp_data = m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig[0]['designation_code'],inspected_on__lte=prev,inspection_no__in=loc_multi).values()
        
        for y in insp_data:
            location = m1.Insp_multi_location.objects.filter(inspection_no=y['inspection_no']).values()
            y.update({'multiple_loc': location})
        print(insp_data)


            
        
    

    elif typei=='Item':
        obj4=models.railwayLocationMaster.objects.filter(location_code=railway).values('location_description')
        if color=='all':
            if case=='Total':
                obj1 = m1.Inspection_details.objects.filter(~Q(status_flag=0),inspection_officer=das_desig[0]['designation_code']).values('inspection_no','inspection_note_no','inspected_on','status_flag')
            elif case=='Pending':
                obj1 = m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig[0]['designation_code']).values('inspection_no','inspection_note_no','inspected_on','status_flag')
            elif case=='Closed':
                obj1 = m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig[0]['designation_code']).values('inspection_no','inspection_note_no','inspected_on','status_flag')
        elif color=='0-3':
            now = datetime.today()
            prev = now - timedelta(days=90)
            if case=='Total':
                obj1 = m1.Inspection_details.objects.filter(~Q(status_flag=0),inspected_on__gte=prev,inspection_officer=das_desig[0]['designation_code']).values('inspection_no','inspection_note_no','inspected_on','status_flag')
            elif case=='Pending':
                obj1 = m1.Inspection_details.objects.filter(status_flag=1,inspected_on__gte=prev,inspection_officer=das_desig[0]['designation_code']).values('inspection_no','inspection_note_no','inspected_on','status_flag')
            elif case=='Closed':
                obj1 = m1.Inspection_details.objects.filter(status_flag=4,inspected_on__gte=prev,inspection_officer=das_desig[0]['designation_code']).values('inspection_no','inspection_note_no','inspected_on','status_flag')
        
        elif color=='3-6':
            now = datetime.today()
            prev = now - timedelta(days=90)		     
            six=now - timedelta(days=180)
            if case=='Total':
                obj1 = m1.Inspection_details.objects.filter(~Q(status_flag=0),inspected_on__lte=six,inspected_on__gte=prev,inspection_officer=das_desig[0]['designation_code']).values('inspection_no','inspection_note_no','inspected_on','status_flag')
            elif case=='Pending':
                obj1 = m1.Inspection_details.objects.filter(status_flag=1,inspected_on__lte=six,inspected_on__gte=prev,inspection_officer=das_desig[0]['designation_code']).values('inspection_no','inspection_note_no','inspected_on','status_flag')
            elif case=='Closed':
                obj1 = m1.Inspection_details.objects.filter(status_flag=4,inspected_on__lte=six,inspected_on__gte=prev,inspection_officer=das_desig[0]['designation_code']).values('inspection_no','inspection_note_no','inspected_on','status_flag')
        
        elif color=='>6':
            now = datetime.today()
            prev = now - timedelta(days=180)
            if case=='Total':
                obj1 = m1.Inspection_details.objects.filter(~Q(status_flag=0),inspected_on__lte=six,inspected_on__gte=prev,inspection_officer=das_desig[0]['designation_code']).values('inspection_no','inspection_note_no','inspected_on','status_flag')
            elif case=='Pending':
                obj1 = m1.Inspection_details.objects.filter(status_flag=1,inspected_on__lte=six,inspected_on__gte=prev,inspection_officer=das_desig[0]['designation_code']).values('inspection_no','inspection_note_no','inspected_on','status_flag')
            elif case=='Closed':
                obj1 = m1.Inspection_details.objects.filter(status_flag=4,inspected_on__lte=six,inspected_on__gte=prev,inspection_officer=das_desig[0]['designation_code']).values('inspection_no','inspection_note_no','inspected_on','status_flag')
        
            

                    
        for i in range(len(obj1)):
            print("detail..........",obj1[i]['inspection_no'])
            obj2=m1.Insp_multi_location.objects.filter(item=railway,type='HQ',inspection_no=obj1[i]['inspection_no']).values('inspection_no')
            print(obj2)
            if obj1[i]['status_flag']==1:
                status='Pending'
            elif obj1[i]['status_flag']==4:
                status='Closed'
            if obj2:
                obj3=m1.Item_details.objects.filter(~Q(status_flag=0),inspection_no=obj2[0]['inspection_no']).values('item_no','observation','des_id')
                print(obj3)
                
                if obj3:
                    for j in range(len(obj3)):
                        print(obj1[0]['inspection_no'],obj2[0]['inspection_no'],obj3[j]['item_no'])
                        result.append([{'sno':c+1},{'inspection_no_id':obj1[i]['inspection_no']},{'inspection_note_no':obj1[i]['inspection_note_no']},{'inspected_on':obj1[i]['inspected_on']},{'railway':railway},{'location_code':''},{'status_flag':obj1[i]['status_flag']},{'item_no':obj3[j]['des_id']},{'observation':obj3[j]['observation']}])
                        c+=1
            
    if typei!='Item':
        row={'result':result,'typei':typei,'railway':obj4,'insp_data':insp_data,'case':case}
    else:
        row={'result':result,'typei':typei,'status':status,'railway':obj4,'case':case}

    #print(row)
    return render(request,'dash_details.html',row)

def dash_home(request):
    now = datetime.today()
    prev = now - timedelta(days=90)
    six=now - timedelta(days=180)
    month='{:02d}'.format(now.month)
    day='{:02d}'.format(now.day)
    prevmonth = '{:02d}'.format(prev.month)
    prevday = '{:02d}'.format(prev.day)
    year = '{:02d}'.format(now.year)
    prevyear = '{:02d}'.format(prev.year)
    dt1 = year+'-'+month+'-'+day
    dt2 = prevyear+'-'+prevmonth+'-'+prevday
    t1=m1.Inspection_details.objects.filter(start_date__lte=dt2).values()
    c6= t1.filter(status_flag=1).count()
    c7= t1.filter(status_flag=2).count()
    c8= t1.filter(status_flag=3).count()
    c9 = t1.filter(status_flag=0).count()
    c10 = t1.filter(status_flag=None).count()
    t = m1.Inspection_details.objects.values()
    c1= t.filter(status_flag=1).count()
    c2= t.filter(status_flag=2).count()
    c3= t.filter(status_flag=3).count()
    c4 = t.filter(status_flag=0).count()
    c5 = t.filter(status_flag=None).count()
    draft = c5+c4
    final = c1+c2+c3
    partial = c2
    closed = c3
    dless = c10+c9
    dmore = draft-dless
    fless = c6+c7+c8
    fmore = final-fless
    pless = c7
    pmore = partial-pless
    cless = c8
    cmore = closed-cless


    #######################prashansa################# 


    #   for all  #
    user=request.user
    das_desig=models.Level_Desig.objects.filter(official_email_ID=user).values('designation_code')
    if das_desig.count()>0:
        das_desig=das_desig[0]['designation_code']
    else:
        das_desig=None

    das_desig2=models.Level_Desig.objects.filter(official_email_ID=user).values('d_level')
    if das_desig2.count()>0:
        das_desig2=das_desig2[0]['d_level']
    else:
        das_desig2=None

    # deti=m1.Inspection_details.objects.filter(status_flag=0,inspection_officer=das_desig).count()
    # detj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=0,inspection_officer=das_desig).values('inspection_no')).count()
    

    # totali=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).count()
    # totalj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).count()
    

    # pendi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig).count()
    # pendj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig).values('inspection_no')).count()
    
    # fulli=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig).count()
    # fullj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig).values('inspection_no')).count()
    
    # lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
    
    # zonalwiselst=[]
    # zonalwisedata=[]
    # tablea=[]
    # tableb=[]
    # for i in range(len(lstrlc)):
    #     location_code=lstrlc[i]['location_code']
    #     rly_unit_code=lstrlc[i]['rly_unit_code']
    #     das_desig1=models.Level_Desig.objects.filter((Q(d_level='AM')|Q(d_level='BM')|Q(d_level='PED')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code')

    #     gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
        
    #     gpendi=m1.Marked_Officers.objects.filter(status_flag=3, item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no'),status_flag=3).values('item_no'),marked_to__in=das_desig1).count()

    #     per=0
    #     if gpendi>0:
    #         per="{:.2f}".format((gpendi/gdeti)*100)

    #     zonalwiselst.append(location_code)
    #     zonalwisedata.append(per)

        
        
    #     ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()

    #     tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
    
    #     pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
        
    #     fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

    #     tablea.append({'type':location_code,'ti':(ti),'tj':(tj),'pi':(pi),'pj':(pj),'fi':(fi),'fj':(fj),'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
    
    # lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='HEAD QUATER')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
    
    # for i in range(len(lstrlc)):
    #     location_code=lstrlc[i]['location_code']
    #     rly_unit_code=lstrlc[i]['rly_unit_code']
    
    #     das_desig1=models.Level_Desig.objects.filter(rly_unit=rly_unit_code,designation_code__isnull=False,d_level='GM').values('designation_code').distinct()

    #     gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

    #     gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no'),status_flag=3).values('item_no'),marked_to__in=das_desig1).count()
        
    #     per=0
    #     if gpendi>0:
    #         per="{:.2f}".format((gpendi/gdeti)*100)
    #     zonalwiselst.append(location_code)
    #     zonalwisedata.append(per)
        
        
    #     ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
    
    #     pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
        
    #     fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

    #     tablea.append({'type':location_code,'ti':(ti),'tj':(tj),'pi':(pi),'pj':(pj),'fi':(fi),'fj':(fj),'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})


    # lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='PRODUCTION UNIT')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
    

    # pulst=[]
    # pudata=[]
    # for i in range(len(lstrlc)):
    #     location_code=lstrlc[i]['location_code']
    #     rly_unit_code=lstrlc[i]['rly_unit_code']
    
    #     das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()
        


    #     gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

    #     gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no'),status_flag=3).values('item_no'),marked_to__in=das_desig1).count()
        

    #     per=0
    #     if gpendi>0:
    #         per="{:.2f}".format((gpendi/gdeti)*100)
    #     pulst.append(location_code)
    #     pudata.append(per)


        
        
    #     ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
    
    #     pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
        
    #     fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

    #     tableb.append({'type':location_code,'ti':(ti),'tj':(tj),'pi':(pi),'pj':(pj),'fi':(fi),'fj':(fj),'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})




    # lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='INSTITUTE')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
    
    
    # for i in range(len(lstrlc)):
    #     location_code=lstrlc[i]['location_code']
    #     rly_unit_code=lstrlc[i]['rly_unit_code']
    
    #     das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()

    #     gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

    #     gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no'),status_flag=3).values('item_no'),marked_to__in=das_desig1).count()
    #     print('abcd',gpendi)

    #     per=0
    #     if gpendi>0:
    #         per="{:.2f}".format((gpendi/gdeti)*100)
    #     pulst.append(location_code)
    #     pudata.append(per)

        
        
    #     ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
    
    #     pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
        
    #     fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

    #     tableb.append({'type':location_code,'ti':(ti),'tj':(tj),'pi':(pi),'pj':(pj),'fi':(fi),'fj':(fj),'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
    
    # lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='PSU')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
    
    # for i in range(len(lstrlc)):
    #     location_code=lstrlc[i]['location_code']
    #     rly_unit_code=lstrlc[i]['rly_unit_code']
    
    #     das_desig1=models.Level_Desig.objects.filter(d_level='PSU',rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



    #     gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

    #     gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no'),status_flag=3).values('item_no'),marked_to__in=das_desig1).count()
        
    #     per=0
    #     if gpendi>0:
    #         per="{:.2f}".format((gpendi/gdeti)*100)
    #     pulst.append(location_code)
    #     pudata.append(per)

        
        
    #     ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
    
    #     pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
        
    #     fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
    #     fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

    #     tableb.append({'type':location_code,'ti':(ti),'tj':(tj),'pi':(pi),'pj':(pj),'fi':(fi),'fj':(fj),'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})

    
        


    # rlytotal=0
    # rlypend=0
    # rlycls=0
    # rlyins=''
    # das_desig1=models.Level_Desig.objects.filter(rly_unit__in=models.railwayLocationMaster.objects.filter(location_type_desc='HEAD QUATER').values('rly_unit_code'),designation_code__isnull=False,d_level='GM').values('designation_code').distinct()
    # rlytotal=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
    # rlycls=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
    # rlypend=rlytotal - rlycls
    # a=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).values('item_no')).values('inspection_no')
    # b=a.distinct().count()
    # c=a.count()
    # rlyins=str(b)+'/'+str(c)


    # putotal=0
    # rpupend=0
    # pucls=0
    # puins=''
    # das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit__in=models.railwayLocationMaster.objects.filter(Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='INSTITUTE')).values('rly_unit_code'),designation_code__isnull=False).values('designation_code').distinct()
    # putotal=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
    # pucls=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
    # pupend=putotal - pucls
    # a=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).values('item_no')).values('inspection_no')
    # b=a.distinct().count()
    # c=a.count()
    # puins=str(b)+'/'+str(c)
   

    
    tablea=[]
    tableb=[]
        
    tabled=[]


    deti=m1.Inspection_details.objects.filter(status_flag=0,inspection_officer=das_desig).count()
    detj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=0,inspection_officer=das_desig).values('inspection_no')).count()
    

    totali=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).count()
    totalj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).count()
    

    pendi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig).count()
    pendj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig).values('inspection_no')).count()
    
    fulli=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig).count()
    fullj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig).values('inspection_no')).count()
    
    treplyi=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),marked_to_id=das_desig).values('item_no')).values('inspection_no')).count()
    treplyj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),marked_to_id=das_desig).values('item_no')).values('inspection_no'))).count()


    repliedi=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=3).values('item_no')).values('inspection_no')).count()
    repliedj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=3).values('item_no')).values('inspection_no'))).count()


    pendingi=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=1).values('item_no')).values('inspection_no')).count()
    pendingj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=1).values('item_no')).values('inspection_no'))).count()

    if totali!=0 and totalj!=0:
        if (totali-pendi)==0:
            pmy=0
        if (totalj-pendj)==0:
            pitem=0
        else:
            pmy="{:.0f}".format(((totali-pendi)/totali)*100)
            pitem="{:.0f}".format(((totalj-pendj)/totalj)*100)
    elif totali==0 or totalj==0:
            pmy=0
            pitem=0

    if treplyi!=0 and treplyj!=0:
        if (treplyi-pendingi)==0:
            replyi=0
        if (treplyj-pendingj)==0:
            replyj=0
        else:
            replyi="{:.0f}".format(((treplyi-pendingi)/treplyi)*100)
            replyj="{:.0f}".format(((treplyj-pendingj)/treplyj)*100)
    elif treplyi==0 or treplyj==0:
            replyi=0
            replyj=0

    table=list(models.railwayLocationMaster.objects.filter(parent_location_code__in=models.railwayLocationMaster.objects.filter(rly_unit_code__in=models.Level_Desig.objects.filter(designation_code=das_desig).values('rly_unit_id')).values('location_code')).values('location_code','rly_unit_code'))

    for i in range(len(table)):
        location_code = table[i]['location_code']
        rly_unit_code=table[i]['rly_unit_code']

        ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer__in=models.Level_Desig.objects.filter(rly_unit_id=rly_unit_code).values('designation_code')).count()
        tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer__in=models.Level_Desig.objects.filter(rly_unit_id=rly_unit_code).values('designation_code')).values('inspection_no')).count()
    
        pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer__in=models.Level_Desig.objects.filter(rly_unit_id=rly_unit_code).values('designation_code')).count()
        pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer__in=models.Level_Desig.objects.filter(rly_unit_id=rly_unit_code).values('designation_code')).values('inspection_no')).count()
        
        fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer__in=models.Level_Desig.objects.filter(rly_unit_id=rly_unit_code).values('designation_code')).count()
        fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer__in=models.Level_Desig.objects.filter(rly_unit_id=rly_unit_code).values('designation_code')).values('inspection_no')).count()
        
        tabled.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
        

    lstrlc=list(models.Level_Desig.objects.filter(d_level='DRM',designation_code__isnull=False,rly_unit__in=models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code__in=models.railwayLocationMaster.objects.filter(rly_unit_code__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('location_code')).values('rly_unit_code')).values('designation','designation_code').distinct().order_by('designation_code'))
    
    drmwiselst=[]
    drmwisedata=[]

    for i in range(len(lstrlc)):
        designation= lstrlc[i]['designation']
        designationcode= lstrlc[i]['designation_code']

        das_desig1=models.Level_Desig.objects.filter(designation_code=designationcode).values('designation_code')

        gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
   
        gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

        per=0
        if gpendi>0:
            per="{:.2f}".format((gpendi/gdeti)*100)

        drmwiselst.append(designation)
        drmwisedata.append(per)

    lstrlc=list(models.Level_Desig.objects.filter(d_level='PHOD',designation_code__isnull=False,rly_unit__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('designation','designation_code').distinct().order_by('designation_code'))

    phodwiselst=[]
    phodwisedata=[]

    for i in range(len(lstrlc)):
        designation=lstrlc[i]['designation']
        designationcode= lstrlc[i]['designation_code']

        das_desig1=models.Level_Desig.objects.filter(designation_code=designationcode).values('designation_code')
        # print('abcde',das_desig1)
      
        gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
        # print('gdeti',gdeti)    

        gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
        # print('gpendi',gpendi)  

        per=0
        if gpendi>0:
            per="{:.2f}".format((gpendi/gdeti)*100)

        phodwiselst.append(designation)
        phodwisedata.append(per)

    lstrlc=list(models.railwayLocationMaster.objects.filter(location_type_desc='RAILWAY BOARD').values('location_code','rly_unit_code').distinct().order_by('location_code'))
    zonalwiselst=[]
    zonalwisedata=[]
    zonalwiselstrb=[]
    zonalwisedatarb=[]
    zonalwiselstzone=[]
    zonalwisedatazone=[]
    for i in range(len(lstrlc)):
        location_code=lstrlc[i]['location_code']
        rly_unit_code=lstrlc[i]['rly_unit_code']
    
        das_desig1=models.Level_Desig.objects.filter((Q(d_level='AM')|Q(d_level='BM')|Q(d_level='PED')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code')

        gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

        gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no'),status_flag=3).values('item_no'),marked_to__in=das_desig1).count()
        
        per=0
        if gpendi>0:
            per="{:.2f}".format((gpendi/gdeti)*100)
        zonalwiselst.append(location_code)
        zonalwisedata.append(per)
        zonalwiselstrb.append(location_code)
        zonalwisedatarb.append(per)
        ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()

        tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
    
        pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
        
        fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
        
        if (ti!=0 and tj!=0) or ((ti-pi)!=0 or (tj-pj!=0)):
            pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
            pc_item="{:.0f}".format(((tj-pj)/tj)*100)
            print(pc_insp,pc_item)
        else:
            pc_insp=0
            pc_item=0
        tablea.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'pmy':pmy,'pitem':pitem,'replyi':replyi,'replyj':replyj,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
    
    lstrlc=list(models.railwayLocationMaster.objects.filter(location_type_desc='HEAD QUATER').values('location_code','rly_unit_code').distinct().order_by('location_code'))
    for i in range(len(lstrlc)):
        location_code=lstrlc[i]['location_code']
        rly_unit_code=lstrlc[i]['rly_unit_code']
    
        das_desig1=models.Level_Desig.objects.filter(rly_unit=rly_unit_code,designation_code__isnull=False,d_level='GM').values('designation_code').distinct()

        gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

        gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
        
        per=0
        if gpendi>0:
            per="{:.2f}".format((gpendi/gdeti)*100)
        zonalwiselst.append(location_code)
        zonalwisedata.append(per)
        zonalwiselstzone.append(location_code)
        zonalwisedatazone.append(per)
        ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()

        tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
    
        pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
        
        fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
        
        if ti!=0 and tj!=0:
            if (ti-pi)==0:
                pc_insp=0
            if (tj-pj)==0:
                pc_item=0
            else:
                pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                #print(pc_insp,pc_item)
        elif ti==0 or tj==0:
            pc_insp=0
            pc_item=0
        tablea.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'pmy':pmy,'pitem':pitem,'replyi':replyi,'replyj':replyj,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
    
    lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='PRODUCTION UNIT')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
    pulst=[]
    pudata=[]
    pulstpu=[]
    pudatapu=[]
    pulstcti=[]
    pudatacti=[]
    pulstpsu=[]
    pudatapsu=[]
    for i in range(len(lstrlc)):
        location_code=lstrlc[i]['location_code']
        rly_unit_code=lstrlc[i]['rly_unit_code']
    
        das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



        gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

        gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
        
        per=0
        if gpendi>0:
            per="{:.2f}".format((gpendi/gdeti)*100)
        pulst.append(location_code)
        pudata.append(per)
        pulstpu.append(location_code)
        pudatapu.append(per)
        ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
    
        pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
        
        fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

        if ti!=0 and tj!=0:
            if (ti-pi)==0:
                pc_insp=0
            if (tj-pj)==0:
                pc_item=0
            else:
                pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                pc_item="{:.0f}".format(((tj-pj)/tj)*100)
        elif ti==0 or tj==0:
            pc_insp=0
            pc_item=0
        
        tableb.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})

    lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='INSTITUTE')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
    for i in range(len(lstrlc)):
        location_code=lstrlc[i]['location_code']
        rly_unit_code=lstrlc[i]['rly_unit_code']
    
        das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



        gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

        gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
        
        per=0
        if gpendi>0:
            per="{:.2f}".format((gpendi/gdeti)*100)
        pulst.append(location_code)
        pudata.append(per)
        pulstcti.append(location_code)
        pudatacti.append(per)
        ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
    
        pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
        
        fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

        if ti!=0 and tj!=0:
            if (ti-pi)==0:
                pc_insp=0
            if (tj-pj)==0:
                pc_item=0
            else:
                pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                pc_item="{:.0f}".format(((tj-pj)/tj)*100)
        elif ti==0 or tj==0:
            pc_insp=0
            pc_item=0
        
        tableb.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})

    lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='PSU')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
    for i in range(len(lstrlc)):
        location_code=lstrlc[i]['location_code']
        rly_unit_code=lstrlc[i]['rly_unit_code']
    
        das_desig1=models.Level_Desig.objects.filter(d_level='PSU',rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



        gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

        gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
        
        per=0
        if gpendi>0:
            per="{:.2f}".format((gpendi/gdeti)*100)
        pulst.append(location_code)
        pudata.append(per)
        pulstpsu.append(location_code)
        pudatapsu.append(per)
        ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
    
        pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
        
        fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
        fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

        if ti!=0 and tj!=0:
            if (ti-pi)==0:
                pc_insp=0
            if (tj-pj)==0:
                pc_item=0
            else:
                pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                pc_item="{:.0f}".format(((tj-pj)/tj)*100)
        elif ti==0 or tj==0:
            pc_insp=0
            pc_item=0
        
        tableb.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})

    rlytotal=0
    rlypend=0
    rlycls=0
    rlyins=''
    das_desig1=models.Level_Desig.objects.filter(rly_unit__in=models.railwayLocationMaster.objects.filter(location_type_desc='HEAD QUATER').values('rly_unit_code'),designation_code__isnull=False,d_level='GM').values('designation_code').distinct()
    rlytotal=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
    rlycls=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
    rlypend=rlytotal - rlycls
    a=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).values('item_no')).values('inspection_no')
    b=a.distinct().count()
    c=a.count()
    rlyins=str(b)+'/'+str(c)


    putotal=0
    rpupend=0
    pucls=0
    puins=''
    das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit__in=models.railwayLocationMaster.objects.filter(Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='INSTITUTE')).values('rly_unit_code'),designation_code__isnull=False).values('designation_code').distinct()
    putotal=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
    pucls=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
    pupend=putotal - pucls
    a=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).values('item_no')).values('inspection_no')
    b=a.distinct().count()
    c=a.count()
    puins=str(b)+'/'+str(c)
    color='all'
    daterange='15-08-22 - '+str(now.strftime('%d-%m-%y'))
    if request.method == 'POST':
        submitvalue=request.POST.get('submit')

    ###### for 0-3 months ########
        if submitvalue=='sum2':
            color='0-3'
            daterange=str(prev.strftime('%d-%m-%y'))+' - '+str(now.strftime('%d-%m-%y'))
            tablea=[]
            tableb=[]

            tabled=[]

            deti=m1.Inspection_details.objects.filter(status_flag=0,inspection_officer=das_desig,inspected_on__gte=prev).count()
            detj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=0,inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).count()
            

            totali=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).count()
            totalj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).count()
            

            pendi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__gte=prev).count()
            pendj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).count()
            
            fulli=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev).count()
            fullj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).count()
            

            repliedi=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=3).values('item_no')).values('inspection_no')).count()
            repliedj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=3).values('item_no')).values('inspection_no'))).count()


            pendingi=m1.Inspection_details.objects.filter(status_flag=1,inspected_on__gte=prev,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=1).values('item_no')).values('inspection_no')).count()
            pendingj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=1,inspected_on__gte=prev,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=1).values('item_no')).values('inspection_no'))).count()

            table=list(models.railwayLocationMaster.objects.filter(parent_location_code__in=models.railwayLocationMaster.objects.filter(rly_unit_code__in=models.Level_Desig.objects.filter(designation_code=das_desig).values('rly_unit_id')).values('location_code')).values('location_code'))
            # print('table',table)

            for i in range(len(table)):
                location_code = table[i]['location_code']
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                tabled.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
    
            lstrlc=list(models.Level_Desig.objects.filter(d_level='DRM',designation_code__isnull=False,rly_unit__in=models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code__in=models.railwayLocationMaster.objects.filter(rly_unit_code__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('location_code')).values('rly_unit_code')).values('designation'))
            drmwiselst=[]
            drmwisedata=[]
    
            for i in range(len(lstrlc)):
                designation= lstrlc[i]['designation']
    
                das_desig1=models.Level_Desig.objects.filter(d_level='DRM',designation_code__isnull=False,rly_unit__in=models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code__in=models.railwayLocationMaster.objects.filter(rly_unit_code__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('location_code')).values('rly_unit_code')).values('designation_code')
    
                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspected_on__gte=prev,inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                 
                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspected_on__gte=prev,inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
        
                drmwiselst.append(designation)
                drmwisedata.append(per)
        
            lstrlc=list(models.Level_Desig.objects.filter(d_level='PHOD',designation_code__isnull=False,rly_unit__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('designation').distinct().order_by('designation'))
        
            phodwiselst=[]
            phodwisedata=[]
        
            for i in range(len(lstrlc)):
                designation=lstrlc[i]['designation']
        
                das_desig1=models.Level_Desig.objects.filter(d_level='PHOD',designation_code__isnull=False,rly_unit__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('designation_code')
              
                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspected_on__gte=prev,inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
           
                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspected_on__gte=prev,inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
         
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)

                phodwiselst.append(designation)
                phodwisedata.append(per)

            lstrlc=list(models.railwayLocationMaster.objects.filter(location_type_desc='RAILWAY BOARD').values('location_code','rly_unit_code').distinct().order_by('location_code'))
            zonalwiselst=[]
            zonalwisedata=[]
            
            zonalwiselstrb=[]
            zonalwisedatarb=[]
            zonalwiselstzone=[]
            zonalwisedatazone=[]
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter((Q(d_level='AM')|Q(d_level='BM')|Q(d_level='PED')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code')

                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no'),status_flag=3).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                zonalwiselst.append(location_code)
                zonalwisedata.append(per)

                zonalwiselstrb.append(location_code)
                zonalwisedatarb.append(per)
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()

                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                tablea.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'pmy':pmy,'pitem':pitem,'replyi':replyi,'replyj':replyj,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
            
            lstrlc=list(models.railwayLocationMaster.objects.filter(location_type_desc='HEAD QUATER').values('location_code','rly_unit_code').distinct().order_by('location_code'))
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter(rly_unit=rly_unit_code,designation_code__isnull=False,d_level='GM').values('designation_code').distinct()

                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                zonalwiselst.append(location_code)
                zonalwisedata.append(per)
                
                zonalwiselstzone.append(location_code)
                zonalwisedatazone.append(per)
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()

                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                tablea.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'pmy':pmy,'pitem':pitem,'replyi':replyi,'replyj':replyj,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
            
            lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='PRODUCTION UNIT')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
            pulst=[]
            pudata=[]
            
            pulstpu=[]
            pudatapu=[]
            pulstcti=[]
            pudatacti=[]
            pulstpsu=[]
            pudatapsu=[]
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                pulst.append(location_code)
                pudata.append(per)
                
                pulstpu.append(location_code)
                pudatapu.append(per)
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                
                tableb.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})

            lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='INSTITUTE')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                pulst.append(location_code)
                pudata.append(per)
                pulstcti.append(location_code)
                pudatacti.append(per)
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                
                tableb.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})

            lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='PSU')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter(d_level='PSU',rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                pulst.append(location_code)
                pudata.append(per)
                
                pulstpsu.append(location_code)
                pudatapsu.append(per)
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                
                tableb.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})

            rlytotal=0
            rlypend=0
            rlycls=0
            rlyins=''
            das_desig1=models.Level_Desig.objects.filter(rly_unit__in=models.railwayLocationMaster.objects.filter(location_type_desc='HEAD QUATER').values('rly_unit_code'),designation_code__isnull=False,d_level='GM').values('designation_code').distinct()
            rlytotal=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            rlycls=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            rlypend=rlytotal - rlycls
            a=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).values('item_no')).values('inspection_no')
            b=a.distinct().count()
            c=a.count()
            rlyins=str(b)+'/'+str(c)


            putotal=0
            rpupend=0
            pucls=0
            puins=''
            das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit__in=models.railwayLocationMaster.objects.filter(Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='INSTITUTE')).values('rly_unit_code'),designation_code__isnull=False).values('designation_code').distinct()
            putotal=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            pucls=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            pupend=putotal - pucls
            a=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).values('item_no')).values('inspection_no')
            b=a.distinct().count()
            c=a.count()
            puins=str(b)+'/'+str(c)


            ######elif sum4 -- greater than 6 months ########

        elif submitvalue=='sum4':
            tablea=[]
            tableb=[]

            tabled=[]

            prev = now - timedelta(days=180)
            color='>6'
            daterange=str(prev.strftime('%d-%m-%y'))+' - '+str(now.strftime('%d-%m-%y'))

            deti=m1.Inspection_details.objects.filter(status_flag=0,inspection_officer=das_desig,inspected_on__lte=prev).count()
            detj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=0,inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).count()
            

            totali=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).count()
            totalj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).count()
            

            pendi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__lte=prev).count()
            pendj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).count()
            
            fulli=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=prev).count()
            fullj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).count()
            
            repliedi=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=3).values('item_no')).values('inspection_no')).count()
            repliedj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=3).values('item_no')).values('inspection_no'))).count()

            pendingi=m1.Inspection_details.objects.filter(status_flag=1,inspected_on__lte=prev,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=1).values('item_no')).values('inspection_no')).count()
            pendingj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=1,inspected_on__lte=prev,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=1).values('item_no')).values('inspection_no'))).count()

            table=list(models.railwayLocationMaster.objects.filter(parent_location_code__in=models.railwayLocationMaster.objects.filter(rly_unit_code__in=models.Level_Desig.objects.filter(designation_code=das_desig).values('rly_unit_id')).values('location_code')).values('location_code'))
            # print('table',table)

            for i in range(len(table)):
                location_code = table[i]['location_code']
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                tabled.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
    

            lstrlc=list(models.Level_Desig.objects.filter(d_level='DRM',designation_code__isnull=False,rly_unit__in=models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code__in=models.railwayLocationMaster.objects.filter(rly_unit_code__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('location_code')).values('rly_unit_code')).values('designation'))

            drmwiselst=[]
            drmwisedata=[]
        
            for i in range(len(lstrlc)):
                designation= lstrlc[i]['designation']
        
                das_desig1=models.Level_Desig.objects.filter(d_level='DRM',designation_code__isnull=False,rly_unit__in=models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code__in=models.railwayLocationMaster.objects.filter(rly_unit_code__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('location_code')).values('rly_unit_code')).values('designation_code')
        
                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspected_on__lte=prev,inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                     
                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspected_on__lte=prev,inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
        
                drmwiselst.append(designation)
                drmwisedata.append(per)
        
            lstrlc=list(models.Level_Desig.objects.filter(d_level='PHOD',designation_code__isnull=False,rly_unit__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('designation').distinct().order_by('designation'))
        
            phodwiselst=[]
            phodwisedata=[]
        
            for i in range(len(lstrlc)):
                designation=lstrlc[i]['designation']
        
                das_desig1=models.Level_Desig.objects.filter(d_level='PHOD',designation_code__isnull=False,rly_unit__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('designation_code')
              
                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspected_on__lte=prev,inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
           
                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspected_on__lte=prev,inspection_officer=das_desig).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
         
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)

                phodwiselst.append(designation)
                phodwisedata.append(per)

            lstrlc=list(models.railwayLocationMaster.objects.filter(location_type_desc='RAILWAY BOARD').values('location_code','rly_unit_code').distinct().order_by('location_code'))
            zonalwiselst=[]
            zonalwisedata=[]
            
            zonalwiselstrb=[]
            zonalwisedatarb=[]
            zonalwiselstzone=[]
            zonalwisedatazone=[]
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter((Q(d_level='AM')|Q(d_level='BM')|Q(d_level='PED')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code')

                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                zonalwiselst.append(location_code)
                zonalwisedata.append(per)
                
                zonalwiselstrb.append(location_code)
                zonalwisedatarb.append(per)
                
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()

                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                tablea.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'pmy':pmy,'pitem':pitem,'replyi':replyi,'replyj':replyj,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
            
            lstrlc=list(models.railwayLocationMaster.objects.filter(location_type_desc='HEAD QUATER').values('location_code','rly_unit_code').distinct().order_by('location_code'))
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter(rly_unit=rly_unit_code,designation_code__isnull=False,d_level='GM').values('designation_code').distinct()

                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                zonalwiselst.append(location_code)
                zonalwisedata.append(per)
                zonalwiselstzone.append(location_code)
                zonalwisedatazone.append(per)
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()

                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                tablea.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'pmy':pmy,'pitem':pitem,'replyi':replyi,'replyj':replyj,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
            
            lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='PRODUCTION UNIT')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
            pulst=[]
            pudata=[]
            
            pulstpu=[]
            pudatapu=[]
            pulstcti=[]
            pudatacti=[]
            pulstpsu=[]
            pudatapsu=[]
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                pulst.append(location_code)
                pudata.append(per)
                
                pulstpu.append(location_code)
                pudatapu.append(per)
                
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

                tableb.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})

            lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='INSTITUTE')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
            
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                pulst.append(location_code)
                pudata.append(per)
                
                pulstcti.append(location_code)
                pudatacti.append(per)

                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                
                tableb.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})

            lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='PSU')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
            
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter(d_level='PSU',rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                pulst.append(location_code)
                pudata.append(per)
                
                pulstpsu.append(location_code)
                pudatapsu.append(per)

                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                
                tableb.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})


            rlytotal=0
            rlypend=0
            rlycls=0
            rlyins=''
            das_desig1=models.Level_Desig.objects.filter(rly_unit__in=models.railwayLocationMaster.objects.filter(location_type_desc='HEAD QUATER').values('rly_unit_code'),designation_code__isnull=False,d_level='GM').values('designation_code').distinct()
            rlytotal=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            rlycls=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            rlypend=rlytotal - rlycls
            a=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).values('item_no')).values('inspection_no')
            b=a.distinct().count()
            c=a.count()
            rlyins=str(b)+'/'+str(c)


            putotal=0
            rpupend=0
            pucls=0
            puins=''
            das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit__in=models.railwayLocationMaster.objects.filter(Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='INSTITUTE')).values('rly_unit_code'),designation_code__isnull=False).values('designation_code').distinct()
            putotal=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            pucls=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            pupend=putotal - pucls
            a=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=prev).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).values('item_no')).values('inspection_no')
            b=a.distinct().count()
            c=a.count()
            puins=str(b)+'/'+str(c)
        
#elif sum 3########


        elif submitvalue=='sum3':
            tablea=[]
            tableb=[]

            tabled=[]

            prev = now - timedelta(days=90)
            six=now - timedelta(days=180)
            color='3-6'
            daterange=str(six.strftime('%d-%m-%y'))+' - '+str(prev.strftime('%d-%m-%y'))
        
            deti=m1.Inspection_details.objects.filter(status_flag=0,inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).count()
            detj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=0,inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).count()
            

            totali=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).count()
            totalj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).count()
            

            pendi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).count()
            pendj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).count()
        
            fulli=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).count()
            fullj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).count()
            
            repliedi=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=3).values('item_no')).values('inspection_no')).count()
            repliedj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=1,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=3).values('item_no')).values('inspection_no'))).count()

            pendingi=m1.Inspection_details.objects.filter(status_flag=1,inspected_on__gte=prev,inspected_on__lte=six,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=1).values('item_no')).values('inspection_no')).count()
            pendingj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=1,inspected_on__gte=prev,inspected_on__lte=six,inspection_no__in=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(marked_to_id=das_desig,status_flag=1).values('item_no')).values('inspection_no'))).count()

            lstrlc=list(models.Level_Desig.objects.filter(d_level='DRM',designation_code__isnull=False,rly_unit__in=models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code__in=models.railwayLocationMaster.objects.filter(rly_unit_code__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('location_code')).values('rly_unit_code')).values('designation'))

            drmwiselst=[]
            drmwisedata=[]
        
            for i in range(len(lstrlc)):
                designation= lstrlc[i]['designation']
        
                das_desig1=models.Level_Desig.objects.filter(d_level='DRM',designation_code__isnull=False,rly_unit__in=models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code__in=models.railwayLocationMaster.objects.filter(rly_unit_code__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('location_code')).values('rly_unit_code')).values('designation_code')
        
                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                     
                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
        
                drmwiselst.append(designation)
                drmwisedata.append(per)
        
            lstrlc=list(models.Level_Desig.objects.filter(d_level='PHOD',designation_code__isnull=False,rly_unit__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('designation').distinct().order_by('designation'))
        
            phodwiselst=[]
            phodwisedata=[]
        
            for i in range(len(lstrlc)):
                designation=lstrlc[i]['designation']
        
                das_desig1=models.Level_Desig.objects.filter(d_level='PHOD',designation_code__isnull=False,rly_unit__in=models.Level_Desig.objects.filter(official_email_ID=user).values('rly_unit_id')).values('designation_code')
              
                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
           
                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
         
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)

                phodwiselst.append(designation)
                phodwisedata.append(per)

            lstrlc=list(models.railwayLocationMaster.objects.filter(location_type_desc='RAILWAY BOARD').values('location_code','rly_unit_code').distinct().order_by('location_code'))
            zonalwiselst=[]
            zonalwisedata=[]
            zonalwiselstrb=[]
            zonalwisedatarb=[]
            zonalwiselstzone=[]
            zonalwisedatazone=[]
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter((Q(d_level='AM')|Q(d_level='BM')|Q(d_level='PED')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code')

                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                zonalwiselst.append(location_code)
                zonalwisedata.append(per)    
                zonalwiselstrb.append(location_code)
                zonalwisedatarb.append(per) 
           
                
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()

                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                tablea.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'pmy':pmy,'pitem':pitem,'replyi':replyi,'replyj':replyj,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
            
            lstrlc=list(models.railwayLocationMaster.objects.filter(location_type_desc='HEAD QUATER').values('location_code','rly_unit_code').distinct().order_by('location_code'))
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter(rly_unit=rly_unit_code,designation_code__isnull=False,d_level='GM').values('designation_code').distinct()

                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no'),status_flag=3).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                zonalwiselst.append(location_code)
                zonalwisedata.append(per)
                
                zonalwiselstzone.append(location_code)
                zonalwisedatazone.append(per)
                
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()

                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                tablea.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'pmy':pmy,'pitem':pitem,'replyi':replyi,'replyj':replyj,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})
            
            lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='PRODUCTION UNIT')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
            pulst=[]
            pudata=[]
            pulstpu=[]
            pudatapu=[]
            pulstcti=[]
            pudatacti=[]
            pulstpsu=[]
            pudatapsu=[]
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                pulst.append(location_code)
                pudata.append(per)
                pulstpu.append(location_code)
                pudatapu.append(per)

                
                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                
                tableb.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})

        




            lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='INSTITUTE')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
            
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                pulst.append(location_code)
                pudata.append(per)
                
                pulstcti.append(location_code)
                pudatacti.append(per)

                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                
                tableb.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})

        




            lstrlc=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='PSU')).values('location_code','rly_unit_code').distinct().order_by('location_code'))
            
            for i in range(len(lstrlc)):
                location_code=lstrlc[i]['location_code']
                rly_unit_code=lstrlc[i]['rly_unit_code']
            
                das_desig1=models.Level_Desig.objects.filter(d_level='PSU',rly_unit=rly_unit_code,designation_code__isnull=False).values('designation_code').distinct()



                gdeti=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()

                gpendi=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
                
                per=0
                if gpendi>0:
                    per="{:.2f}".format((gpendi/gdeti)*100)
                pulst.append(location_code)
                pudata.append(per)
                
                pulstpsu.append(location_code)
                pudatapsu.append(per)

                ti=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                tj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
            
                pi=m1.Inspection_details.objects.filter(status_flag=1,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                pj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=2)|Q(status_flag=3)),inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()
                
                fi=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).count()
                fj=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter(status_flag=4,inspection_officer=das_desig,inspected_on__lte=six,inspected_on__gte=prev,inspection_no__in=m1.Insp_multi_location.objects.filter(type='HQ',item=location_code).values('inspection_no')).values('inspection_no')).count()

                if ti!=0 and tj!=0:
                    if (ti-pi)==0:
                        pc_insp=0
                    if (tj-pj)==0:
                        pc_item=0
                    else:
                        pc_insp="{:.0f}".format(((ti-pi)/ti)*100)
                        pc_item="{:.0f}".format(((tj-pj)/tj)*100)
                elif ti==0 or tj==0:
                    pc_insp=0
                    pc_item=0
                
                tableb.append({'type':location_code,'ti':ti,'tj':tj,'pi':pi,'pj':pj,'fi':fi,'fj':fj,'pc_insp':pc_insp,'pc_item':pc_item,'total':str(ti)+'/'+str(tj),'pend':str(pi)+'/'+str(pj),'closed':str(fi)+'/'+str(fj)})

        





            rlytotal=0
            rlypend=0
            rlycls=0
            rlyins=''
            das_desig1=models.Level_Desig.objects.filter(rly_unit__in=models.railwayLocationMaster.objects.filter(location_type_desc='HEAD QUATER').values('rly_unit_code'),designation_code__isnull=False,d_level='GM').values('designation_code').distinct()
            rlytotal=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            rlycls=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            rlypend=rlytotal - rlycls
            a=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).values('item_no')).values('inspection_no')
            b=a.distinct().count()
            c=a.count()
            rlyins=str(b)+'/'+str(c)


            putotal=0
            rpupend=0
            pucls=0
            puins=''
            das_desig1=models.Level_Desig.objects.filter((Q(d_level='GM_PU')|Q(d_level='DG_CTI')),rly_unit__in=models.railwayLocationMaster.objects.filter(Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='INSTITUTE')).values('rly_unit_code'),designation_code__isnull=False).values('designation_code').distinct()
            putotal=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            pucls=m1.Marked_Officers.objects.filter(status_flag=3,item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).count()
            pupend=putotal - pucls
            a=m1.Item_details.objects.filter(item_no__in=m1.Marked_Officers.objects.filter(item_no__in=m1.Item_details.objects.filter(inspection_no__in=m1.Inspection_details.objects.filter((Q(status_flag=1)|Q(status_flag=4)),inspection_officer=das_desig,inspected_on__gte=prev,inspected_on__lte=six).values('inspection_no')).values('item_no'),marked_to__in=das_desig1).values('item_no')).values('inspection_no')
            b=a.distinct().count()
            c=a.count()
            puins=str(b)+'/'+str(c)

    tablea=sorted(tablea, key = lambda item: (item['ti'],item['type']))
    tableb=sorted(tableb, key = lambda item: (item['ti'],item['type']))
    tablec=tablea+tableb
    tablec=sorted(tablec, key = lambda item: (item['ti'],item['tj']),reverse=True)
    
    tablep=tabled
    tablep=sorted(tablep, key = lambda item: (item['ti'],item['tj']),reverse=True)

    context ={
        'daterange':daterange,
        'color':color,
        'pulst':pulst,
        'pudata':pudata,
        'deti':deti,
        'detj':detj,
        'totali':totali,
        'totalj':totalj,
        'pendi':pendi,
        'pendj':pendj,
        'fulli':fulli,
        'fullj':fullj,
        'zonalwiselst':zonalwiselst,
        'zonalwisedata':zonalwisedata,
        'rlytotal':rlytotal,
        'rlypend':rlypend,
        'rlycls':rlycls,
        'rlyins':rlyins,
        'putotal':putotal,
        'rpupend':rpupend,
        'pucls':pucls,
        'puins':puins,
        'tablea':tablea,
        'tableb':tableb,
        'tablec':tablec,
        'tabled':tabled,
        'tablep':tablep,
        'draft':draft,
        'final':final,
        'partial':partial,
        'closed':closed,
        'dless':dless,
        'fless':fless,
        'pless':pless,
        'cless':cless,
        'dmore':dmore,
        'fmore':fmore,
        'pmore':pmore,
        'cmore':cmore,
        'pmy':pmy,
        'pitem':pitem,
        'replyi':replyi,
        'replyj':replyj,

        'pulstpu':pulstpu,
        'pudatapu':pudatapu,
        'pulstcti':pulstcti,
        'pudatacti':pudatacti,
        'pulstpsu':pulstpsu,
        'pudatapsu':pudatapsu,
        'zonalwiselstrb':zonalwiselstrb,
        'zonalwisedatarb':zonalwisedatarb,
        'zonalwiselstzone':zonalwiselstzone,
        'zonalwisedatazone':zonalwisedatazone,

        'das_desig2':das_desig2,
        'drmwiselst':drmwiselst,
        'drmwisedata':drmwisedata,
        'phodwiselst':phodwiselst,
        'phodwisedata':phodwisedata,
        'pendingi':pendingi,
        'pendingj':pendingj,
        'repliedi':repliedi,
        'repliedj':repliedj,

    }
    return render(request, 'dash_home.html',context)




def chartdata(request):
    down = int(request.GET.get('down'))
    up = int(request.GET.get('up'))
    mn = request.GET.get('month')
    print(down,up,mn)
    now = datetime.today()
    month='{:02d}'.format(now.month)
    year = '{:02d}'.format(now.year)
    year1 = year[2:4]
    mon=[]
    mon1=[]
    if down>0:
        mn1=datetime.strptime(mn[0:3], '%b').month
        month = str(int(mn1)-1)
        year1=mn[4:6]
        year = '20'+year1
    elif up>0:
        mn1=datetime.strptime(mn[0:3], '%b').month
        month = str(int(mn1)-1)
        year1=str(int(mn[4:6])+1)
        year = '20'+year1
        print(month) 
    j=12
    if int(month)>=6:
        for i in range(0,6):
            temp = datetime.strptime(str(int(month)-i), "%m").strftime("%b")+'-'+year1
            mon1.append('{:02d}'.format(int(month)-i)+'-'+year)
            mon.append(temp)
    else:
        for i in range(0,6):
            if int(month)-i>0:
                temp = datetime.strptime(str(int(month)-i), "%m").strftime("%b")+'-'+year1
                mon1.append('{:02d}'.format(int(month)-i)+'-'+year)
                mon.append(temp)
            else:
                temp = datetime.strptime(str(j), "%m").strftime("%b")+'-'+str(int(year1)-1)
                mon1.append('{:02d}'.format(j)+'-'+str(int(year)-1))
                mon.append(temp)
                j-=1  
    mon = mon[::-1]
    mon1 = mon1[::-1]
    print(mon1)
    count=[]
    count1=[]
    for k in mon1:
        k1 = k[0:2]
        k2 = k[3:7]
        print(k1,k2)
        t = m1.Inspection_details.objects.filter(inspected_on__month=k1,inspected_on__year=k2).values()
        c1= t.filter(status_flag=1).count()
        c2= t.filter(status_flag=2).count()
        c3= t.filter(status_flag=3).count()
        c4 = t.filter(status_flag=0).count()
        c5 = t.filter(status_flag=None).count()
        draft = c5+c4
        final = c1+c2+c3
        count1.append(final)
        count.append(draft)
    context={
        'count':count,
        'mon':mon,
        'count1':count1,
        'mon1':mon1,
    }
    return JsonResponse(context,safe=False)
def piedata(request):
    t = m1.Inspection_details.objects.values()
    c1= t.filter(status_flag=1).count()
    c2= t.filter(status_flag=2).count()
    c3= t.filter(status_flag=3).count()
    c4 = t.filter(status_flag=0).count()
    c5 = t.filter(status_flag=None).count()
    dta={}
    draft = c5+c4
    final = c1+c2+c3
    partial = c2
    closed = c3
    pending = c1
    dta['0']=closed
    dta['1']=pending
    dta['2']=partial
    print(dta)
    data8=[]
    data9=[]
    temp=[]
    temp.append("closed")
    temp.append((float(c3)/float(c1+c2+c3))*100)
    data8.append(temp)
    temp=[]
    temp.append("Pending Compliance")
    temp.append(40) #(float(c1)/float(c1+c2+c3))*100
    data8.append(temp)
    temp=[]
    temp.append("Partial Compliance")
    temp.append(60) #(float(c2)/float(c1+c2+c3))*100
    data8.append(temp)
    t = m1.Item_details.objects.values()
    c1= t.filter(status_flag=1).count()
    c2= t.filter(status_flag=2).count()
    c3= t.filter(status_flag=3).count()
    c4 = t.filter(status_flag=0).count()
    c5 = t.filter(status_flag=None).count()
    draft2 = c5+c4
    final2 = c1+c2+c3
    partial2 = c2
    closed2 = c3
    pending2 = c1
    temp=[]
    temp.append('closed')
    temp.append(0)#(float(c3)/float(c1+c2+c3))*100)
    data9.append(temp)
    temp=[]
    temp.append('Pending Compliances')
    temp.append(70)#(float(c1)/float(c1+c2+c3))*100)
    data9.append(temp)
    temp=[]
    temp.append('Partial Compliances')
    temp.append(30)#(float(c2)/float(c1+c2+c3))*100)
    data9.append(temp)
    context ={
        'closed':closed,
        'pending':pending,
        'partial':partial,
        'closed2':closed2,
        'pending2':pending2,
        'partial2':partial2,
        'data8':data8,
        'data9':data9,
        'dta':dta
    }
    return JsonResponse(context,safe=False)
    # AMAN end

#tarun



def inspectionReportReply(request, insp_id):

    ins_title=m1.Inspection_details.objects.filter(inspection_no=insp_id).values()
    item_details1= list(m1.Item_details.objects.filter(inspection_no_id=insp_id).exclude(type='SSH').values().order_by('item_no'))
    
    
    multi_loc = m1.Insp_multi_location.objects.filter(inspection_no_id=insp_id).values()

    
    for j in item_details1:
        # mrkoffi = {}
        if j['type'] == 'SH':
            mark=m1.Marked_Officers.objects.filter(item_no=j['item_no']).values('marked_to__designation', 'marked_to__empno_id','compliance','reply_on', 'viewed_on' ,'marked_no', 'status_flag','created_on', 'status').order_by('marked_no')
            print(mark, '11111111')
            for a in mark:
                dt1 = datetime.today() - a['created_on']

                a.update({'days': dt1.days})
            
            # desig_longdesc1 =''
            # marked_officers1 = ''
            # for x in mark:
            #     #marked=m1.empmast.objects.filter(myuser_id=x['myuser_id_id'])
            #     marked=models.Level_Desig.objects.filter(designation_code=x['marked_to_id'])
            #     print('^^^^^^^^^', marked)
            #     if marked[0].designation:
            #         desig_longdesc1 += marked[0].designation    
            #     marked_officers1 += marked[0].empno_id
            #     print('uuuuuuuuuu', marked[0].designation)
                
            #     mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': desig_longdesc1})
            j.update({'mrkoffi': mark})

        elif j['type'] == 'H':
            mark=m1.Marked_Officers.objects.filter(item_no=j['item_no'])
            print(mark, '00000000')
    #         print('***********', mark)
            if mark.exists():
                all_h = mark.values('marked_to__designation','created_on', 'marked_to__empno_id','compliance','reply_on',  'viewed_on','marked_no', 'status_flag', 'status').order_by('marked_no')
                for a in all_h:
                    dt1 = datetime.today() - a['created_on']

                    a.update({'days': dt1})
                j.update({'mrkoffi': all_h, 'chk_cts':'YES'})

            else:
                j.update({'chk_cts':'NO'})
    #             
    # 
    # if mark[0].marked_to is not None: 
    #                 print('---------', j['item_no'])
    #                 # mrkoffi = {}
    #                 desig_longdesc1 =''
    #                 marked_officers1 = ''
    #                 for x in mark.values():
    #                     # print('xxxxxxxxx', x['myuser_id_id'])
                        
    #                     des = models.Level_Desig.objects.filter(designation_code=x['marked_to_id'])
    #                     desig_longdesc1 += des[0].designation+','
    #                     marked_officers1 += des[0].empno_id+','
                    
                        
                    
    #                 mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': desig_longdesc1})
                    
            #         j.update({'mrkoffi': mrkoffi, 'chk_cts':'YES'})
            #     else:
            #         j.update({'mrkoffi': '', 'chk_cts':'YES'})
            # else:
            
            
            # j.update({'chk_cts':'NO'})
        

    # ins_detail[0].update({'item_details1': item_details1})
    # print('00000000', ins_detail)
    print('$$$$$$$$$$', item_details1)
    # print('mmmmmmmmmmm', mark)
    empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    
    if empnox:
        empno = empnox[0].designation_code
        desig = empnox[0].designation
    context={
        'ins_title':ins_title,
        'item_details1': item_details1,
        
        'insp_number': insp_id,
        'multi_loc': multi_loc,
        'desig': desig,
        }  
        
    return render(request, 'inspectionReportReply.html', context)

def received_compliance_checklist(request):
    empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    if empnox:
        empno = empnox[0].designation_code
        # mydata=list(m1.Inspection_details.objects.filter(status_flag=1).values('inspection_no','inspection_note_no', 'inspection_title','zone','inspected_on','division','dept','location','report_path').order_by('-inspection_no'))
        # print(mydata)
        list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code')
        list4=[]
        for i in list3:
            list4.append(i['location_code'])    
        list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code')
        list2=[]
        for i in list1:
            list2.append(i['location_code'])
            
        list5=list(models.departMast.objects.all().values('department_name')) 
        item=[] 
        # print(list5)

        # obj1 = m1.Marked_Officers.objects.filter(status_flag=2, item_no__inspection_no__created_by=request.user).values('item_no__inspection_no').distinct()
        obj1 = m1.Marked_Officers.objects.filter(status_flag=2,item_no__inspection_no__inspection_officer=empno).values('item_no__inspection_no').distinct()
        
        mydata1 =[]
        for i in obj1:
            insp = i['item_no__inspection_no']
            mydata = list(m1.Inspection_details.objects.filter(inspection_no=insp).values())
            location = list(m1.Insp_multi_location.objects.filter(inspection_no=insp).values())
            for j in mydata:
                j.update({'location_item': location})
            
            
            
            mydata1.extend(mydata)
            print('iiiiiiiiiiiii',  mydata)
                    
        context={
            'Zone':list2 ,
                'division':list4,
                'department':list5,
                'item':item,
                'mydata': mydata1,
            }

        if request.method == 'POST':
            print('@@@@@@@@@@@@@')
            rly=request.POST.get('zone')
            div=request.POST.get('division')
            dept=request.POST.get('department')
            loc=request.POST.get('loc')
            start_date=request.POST.get('start')
            end_date=request.POST.get('txtDate2')
            get_designation=request.POST.get('get_designation')
            print(rly,div,dept,loc,start_date,end_date,get_designation,"~~~~~~~~~")
            
            
            # mydata=m1.Inspection_details.objects.filter(zone=rly,division=div,dept=dept).values('inspection_no','inspection_note_no', 'inspection_title','inspected_on', 'zone','division','dept','location','report_path').order_by('-inspection_no')
            mydata1 =[]
            for i in obj1:
                insp = i['item_no__inspection_no']
                mydata = list(m1.Inspection_details.objects.filter(inspection_no=insp, zone=rly,division=div,dept=dept).values())
                mydata1.extend(mydata)
                print('iiiiiiiiiiiii',  mydata)

            context={
                'Zone':list2 ,
                'division':list4,
                'department':list5,
                'item':item,
                'mydata': mydata1,
            }
            
            return render(request,"received_compliance_checklist.html",context)
        
        return render(request,"received_compliance_checklist.html",context)
    else:
        messages.error(request, 'You are not authorize to see inspection. Please contact to admin')
        return render(request,"received_compliance_checklist.html")



def inspectionReportPdf(request, insp_id):
    ins_detail=list(m1.Inspection_details.objects.filter(inspection_no=insp_id).values())
    item_details1= list(m1.Item_details.objects.filter(inspection_no_id=insp_id).values().order_by('item_no'))
    loc= m1.Insp_multi_location.objects.filter(inspection_no=insp_id, type='LOC').values_list('item', flat=True)
    loc_str = ''
    for x in loc:
        loc_str += x +','
    ins_detail[0].update({'location': loc_str })
    empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    if empnox:
        empno = empnox[0].empno_id
        desig = empnox[0].designation
        empname=m1.empmast.objects.filter(empno=empno)[0]

        
    

        # empno=m1.MyUser.objects.filter(username=request.user)[0].username
        # desig=models.Level_Desig.objects.filter(empno_id=empno)[0]
        # print('=================', empname)
        for j in item_details1:
            if j['type'] == 'SH':
                mark=m1.Marked_Officers.objects.filter(item_no=j['item_no']).values()
                print('---------', j['item_no'])
                mrkoffi = {}
                desig_longdesc1 =''
                marked_officers1 = ''
                for x in mark:
                    print('xxxxxxxxx', x['myuser_id_id'])
                    # marked=m1.empmast.objects.filter(myuser_id=x['myuser_id_id'])
                    marked=models.Level_Desig.objects.filter(designation_code=x['marked_to_id'])
                    print('yyyyyyyy', marked[0].designation)
                    if  marked[0].designation:
                        desig_longdesc1 += marked[0].designation+', '
                    marked_officers1 += marked[0].empno_id+','
                # desig_long = desig_longdesc1.rstrip(' ,')
                # print('========', desig_long, '========')
                # mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': desig_long})
                if marked_officers1 != '':
                    testdesig=desig_longdesc1.split(',')
                    testempno=marked_officers1.split(',')
                    testdesig.pop()
                    testempno.pop()
                    testmarkofficer=''
                    lstdict=[]
                    alldesig = models.Level_Desig.objects.filter(empno__in=testempno).values('d_level').distinct('d_level')
                    
                    for i in alldesig:
                        if i['d_level'] == 'GM':
                            lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(empno__in=testempno).count()
                            if lst1 == 0:
                                lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level']).values('empno','designation').order_by('designation'))
                                if testmarkofficer != '':
                                    testmarkofficer+=','
                                testmarkofficer=testmarkofficer+"All GM's/ZR"
                                # testempno=set(testempno)
                                # part=set(map(lambda d: d['partno'], part))
                                interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                testempno=list(map(lambda d: d['empno'], lst2))
                                testdesig=list(map(lambda d: d['designation'], lst2))
                                lstdict.append({"desig":"All GM's/ZR","empno":list(interkey)})

                        elif i['d_level'] == 'BM':
                            lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(empno__in=testempno).count()
                            if lst1 == 0:
                                lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level']).values('empno','designation').order_by('designation'))
                                if testmarkofficer != '':
                                    testmarkofficer+=','
                                testmarkofficer=testmarkofficer+"All Board Member's"
                                # testempno=set(testempno)
                                # part=set(map(lambda d: d['partno'], part))
                                interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                testempno=list(map(lambda d: d['empno'], lst2))
                                testdesig=list(map(lambda d: d['designation'], lst2))
                                lstdict.append({"desig":"All Board Member's","empno":list(interkey)})


                        elif i['d_level'] == 'PHOD':
                            lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(empno__in=testempno).count()
                            if lst1 == 0:
                                lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level']).values('empno','designation').order_by('designation'))
                                if testmarkofficer != '':
                                    testmarkofficer+=','
                                testmarkofficer=testmarkofficer+"All PHOD's"
                                # testempno=set(testempno)
                                # part=set(map(lambda d: d['partno'], part))
                                interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                testempno=list(map(lambda d: d['empno'], lst2))
                                testdesig=list(map(lambda d: d['designation'], lst2))
                                lstdict.append({"desig":"All PHOD's","empno":list(interkey)})
                            else:
                                hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
                                for ii in hq:
                                    rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
                                    if models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exists():
                                        lst3=models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exclude(empno__in=testempno).count()
                                        if lst3 == 0:
                                            lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('empno','designation').order_by('designation'))
                                            if testmarkofficer != '':
                                                testmarkofficer+=','
                                            testmarkofficer=testmarkofficer+"All PHOD's"+ii['parent_location_code']
                                            # testempno=set(testempno)
                                            # part=set(map(lambda d: d['partno'], part))
                                            interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                            testempno=list(map(lambda d: d['empno'], lst2))
                                            testdesig=list(map(lambda d: d['designation'], lst2))
                                            lstdict.append({"desig":"All PHOD's/"+ii['parent_location_code'],"empno":list(interkey)})



                        elif i['d_level'] == 'DRM':
                            lst1=models.Level_Desig.objects.filter(d_level=i['d_level'],empno__isnull=False).exclude(empno__in=testempno).count()
                            if lst1 == 0:
                                lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level']).values('empno','designation').order_by('designation'))
                                if testmarkofficer != '':
                                    testmarkofficer+=','
                                testmarkofficer=testmarkofficer+"All DRM's"
                                # testempno=set(testempno)
                                # part=set(map(lambda d: d['partno'], part))
                                interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                testempno=list(map(lambda d: d['empno'], lst2))
                                testdesig=list(map(lambda d: d['designation'], lst2))
                                lstdict.append({"desig":"All DRM's","empno":list(interkey)})
                            else:
                                hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
                                for ii in hq:
                                    rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
                                    if models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exists():
                                        lst3=models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit,empno__isnull=False).exclude(empno__in=testempno).count()
                                        if lst3 == 0:
                                            lst2=list(models.Level_Desig.objects.filter(empno__in=testempno).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('empno','designation').order_by('designation'))
                                            if testmarkofficer != '':
                                                testmarkofficer+=','
                                            testmarkofficer=testmarkofficer+"All DRM's/"+ii['parent_location_code']
                                            # testempno=set(testempno)
                                            # part=set(map(lambda d: d['partno'], part))
                                            interkey=set(testempno)-set(map(lambda d: d['empno'], lst2))
                                            testempno=list(map(lambda d: d['empno'], lst2))
                                            testdesig=list(map(lambda d: d['designation'], lst2))
                                            lstdict.append({"desig":"All DRM's/"+ii['parent_location_code'],"empno":list(interkey)})


                    
                    for i in range(len(testdesig)):
                        if testmarkofficer != '':
                            testmarkofficer+=','
                        testmarkofficer=testmarkofficer+testdesig[i]
                        lstdict.append({"desig":testdesig[i],"empno":[testempno[i]]})

        
                mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': testmarkofficer,'custom_key':json.dumps(lstdict)})
            
                j.update({'mrkoffi': mrkoffi})
                print('mmmmmmmm', desig_longdesc1)
            elif j['type'] == 'H':
                mark=m1.Marked_Officers.objects.filter(item_no=j['item_no'])
                print(mark, '00000000')
        #         print('***********', mark)
                if mark.exists():
                    all_h = mark.values('marked_to__designation', 'marked_to__empno_id','compliance','reply_on' ,'marked_no', 'status_flag').order_by('marked_no')
                    
                    j.update({'mrkoffi': all_h, 'chk_cts':'YES'})

                else:
                    j.update({'chk_cts':'NO'})


        from datetime import datetime
        today_date = datetime.today()
        ins_detail[0].update({'item_details1': item_details1})
        print('00000000', ins_detail)
        print('00000000', today_date)
        inspection_note_no=m1.Inspection_details.objects.filter(inspection_no=insp_id)[0].inspection_note_no
        copyto1=[]
        if(m1.Insp_mail_details.objects.filter(inspection_no=insp_id, area='Copy To')):
            copyto1 = list(m1.Insp_mail_details.objects.filter(inspection_no=insp_id, area='Copy To').values('send_to', 'send_desig'))
            # print(copyto1[0]['send_to'],'copytocopyto')
            # # if(models.Level_Desig.objects.filter(empno_id__in=copyto1)):
            # d = copyto1[0]['send_to'].split(',')
            # copyto = models.Level_Desig.objects.filter(empno_id__in = d).values('designation')
            # print(copyto,'copytocopyto')
        context={
            'ins_detail':ins_detail,
            'today_date': today_date,
            'inspection_note_no': inspection_note_no,
            'empname': empname,
            'copyto': copyto1,
            'desig':desig,
            }
        template_src='inspectionReportPdf.html'
        return render_to_pdf(template_src, context)
    else:
        return HttpResponse('PDF not found 404')

  

def reciveCompReportReply(request, insp_id):

    ins_title=m1.Inspection_details.objects.filter(inspection_no=insp_id).values()
    item_details1= list(m1.Item_details.objects.filter(inspection_no_id=insp_id).exclude(type='SSH').values().order_by('item_no'))
    
    
    multi_loc = m1.Insp_multi_location.objects.filter(inspection_no_id=insp_id).values()

    
    for j in item_details1:
        mrkoffi = {}
        if j['type'] == 'SH':
            mark=m1.Marked_Officers.objects.filter(item_no=j['item_no']).values('marked_to__designation', 'marked_to__empno_id','compliance','reply_on' ,'marked_no', 'status_flag', 'status').order_by('marked_no')
            print(mark, '11111111')
            
            # desig_longdesc1 =''
            # marked_officers1 = ''
            # for x in mark:
            #     #marked=m1.empmast.objects.filter(myuser_id=x['myuser_id_id'])
            #     marked=models.Level_Desig.objects.filter(designation_code=x['marked_to_id'])
            #     print('^^^^^^^^^', marked)
            #     if marked[0].designation:
            #         desig_longdesc1 += marked[0].designation    
            #     marked_officers1 += marked[0].empno_id
            #     print('uuuuuuuuuu', marked[0].designation)
                
            #     mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': desig_longdesc1})
            j.update({'mrkoffi': mark})

        elif j['type'] == 'H':
            mark=m1.Marked_Officers.objects.filter(item_no=j['item_no'])
            print(mark, '00000000')
    #         print('***********', mark)
            if mark.exists():
                all_h = mark.values('marked_to__designation', 'marked_to__empno_id','compliance','reply_on' ,'marked_no', 'status_flag', 'status').order_by('marked_no')
                
                j.update({'mrkoffi': all_h, 'chk_cts':'YES'})

            else:
                j.update({'chk_cts':'NO'})
    #             
    # 
    # if mark[0].marked_to is not None: 
    #                 print('---------', j['item_no'])
    #                 # mrkoffi = {}
    #                 desig_longdesc1 =''
    #                 marked_officers1 = ''
    #                 for x in mark.values():
    #                     # print('xxxxxxxxx', x['myuser_id_id'])
                        
    #                     des = models.Level_Desig.objects.filter(designation_code=x['marked_to_id'])
    #                     desig_longdesc1 += des[0].designation+','
    #                     marked_officers1 += des[0].empno_id+','
                    
                        
                    
    #                 mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': desig_longdesc1})
                    
            #         j.update({'mrkoffi': mrkoffi, 'chk_cts':'YES'})
            #     else:
            #         j.update({'mrkoffi': '', 'chk_cts':'YES'})
            # else:
            
            
            # j.update({'chk_cts':'NO'})
        

    # ins_detail[0].update({'item_details1': item_details1})
    # print('00000000', ins_detail)
    print('$$$$$$$$$$', item_details1)
    # print('mmmmmmmmmmm', mark)
    empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    
    if empnox:
        empno = empnox[0].designation_code
        desig = empnox[0].designation
    context={
        'ins_title':ins_title,
        'item_details1': item_details1,
        
        'insp_number': insp_id,
        'multi_loc': multi_loc,
        'desig': desig,
        }  
        
    return render(request, 'reciveCompReportReply.html', context)


def actionBtnFunction_ajax(request):
    if request.method == 'GET' or request.is_ajax:
        insp_id = request.GET.get('insp_number')
        mark_officer_id = request.GET.get('mark_officer_id')
        item_details1= list(m1.Item_details.objects.filter(inspection_no_id=insp_id).values())


        obj = list(m1.Marked_Officers.objects.filter(marked_no=mark_officer_id).values())
        m1.Marked_Officers.objects.filter()
        m1.Insp_mail_details.objects.filter()
        rem_obj = list(m1.Officers_Remark.objects.filter(marked_no=mark_officer_id, status_flag=0).values())
        context = {
            'obj': obj,
            'rem_obj': rem_obj,
        }
        return JsonResponse(context, safe=False)
    return JsonResponse({'success': False}, status=400)



def save_mark_reply_ajax(request):
    if request.method == 'GET' or request.is_ajax:
        # action_option = request.GET.get('action_option')
        mark_id = request.GET.get('mark_num')
        remark_id = request.GET.get('remark_id')
        insp_number = request.GET.get('insp_number')
        
        # item_details1= list(m1.Item_details.objects.filter(inspection_no_id=insp_id).values())
        obj = m1.Marked_Officers.objects.filter(marked_no=mark_id)

        # obj1 = m1.MyUser.objects.filter(id=obj[0].myuser_id_id)
        # print(obj[0].myuser_id_id,'5555555555555555555555')
        # m1.Marked_Officers.objects.filter()
        # m1.Insp_mail_details.objects.filter()
        #===================================
        # models.Level_Desig.objects.filter()
        # if action_option == 'Accept':
        #     # m1.Officers_Remark.objects.create(status='Accept', marked_no=obj)
        #     m1.Marked_Officers.objects.filter(marked_no=mark_id).update(status_flag=3)
        #     pass
        if m1.Officers_Remark.objects.filter(marked_no=mark_id).exists():
            m1.Officers_Remark.objects.filter(marked_no=mark_id).update(status_flag=1)

        
        m1.Officers_Remark.objects.create(remark=remark_id, marked_desig_id=obj[0].marked_to, status='Reject',reply_on=obj[0].reply_on, marked_no=obj[0],reply_received=obj[0].compliance,rejected_on=datetime.now())
        m1.Marked_Officers.objects.filter(marked_no=mark_id).update(status_flag=1, status='R')
        # m1.Item_details.objects.filter()
        

        print(insp_number)
        #this condition for close case filnal
        # x = m1.Marked_Officers.objects.filter(~Q(status_flag=3), item_no__inspection_no=insp_number)
        # if x.count() == 0:
        #     m1.Inspection_details.objects.filter(inspection_no=insp_number).update(status_flag=4)
        #     print('yyyyyyyyyyyyyyy')
        # print(x.count(), '0000000000000000000000000')

        
        return JsonResponse({'success': 'save'}, safe=False)
    return JsonResponse({'success': False}, status=400)

def accept_mark_reply_ajax(request):
    if request.method == 'GET' or request.is_ajax:
        mark_id = request.GET.get('mark_num')
        insp_number = request.GET.get('insp_number')
 
        m1.Marked_Officers.objects.filter(marked_no=mark_id).update(status_flag=3)

        x = m1.Marked_Officers.objects.filter(~Q(status_flag=3), item_no__inspection_no=insp_number)
        if x.count() == 0:
            m1.Inspection_details.objects.filter(inspection_no=insp_number).update(status_flag=4)
            print('yyyyyyyyyyyyyyy')
        
        return JsonResponse({'success': 'save'}, safe=False)
    return JsonResponse({'success': False}, status=400)




def inspReminderSend_ajax(request):
    if request.method == 'GET' or request.is_ajax:
        insp_id = request.GET.get('insp_number')
        title=list(m1.Inspection_details.objects.filter(inspection_no=insp_id, ).values('inspection_title'))
        ins_detail1=list(m1.Item_details.objects.filter(inspection_no=insp_id, type='SH').values('item_no'))
        officer = []
        send_to = ''
        send_desig = ''
        for i in ins_detail1:
            mrk = m1.Marked_Officers.objects.filter(item_no=i['item_no']).values('marked_to__designation', 'marked_to__empno', 'marked_to__official_email_ID')
            for j in mrk:
                # print('!!!!!!!!!!!!!!!!!', j)
                officer.append(j['marked_to__official_email_ID'])
                if j['marked_to__empno']:
                    send_to += j['marked_to__empno'] + ','
                if j['marked_to__designation']:
                    send_desig += j['marked_to__designation'] + ','
        #     marked=m1.empmast.objects.filter(myuser_id=mrk[0]['myuser_id_id'])
        #     if marked:
        #         if marked[0].email not in officer:
        #             officer.append(marked[0].email)
        #             send_to += marked[0].empno + ','
        #             if marked[0].desig_longdesc:
        #                 send_desig += marked[0].desig_longdesc + ','
        # print('ssssssssss', officer)
        # print('rrrrrrrrrrrrr', send_to)
        # print('ttttttttttttt', send_desig)
        try:

            To=officer

            subject="Inspection Reminder"
            # To=['ecegcttarun@gmail.com','kr.abhijeet6235@gmail.com']

            inspection_title = title[0]['inspection_title']
            context = {'title': inspection_title, 'subject': subject}
                
            InspSendMail(subject, To, context)

            m1.Insp_mail_details.objects.create(subject=subject, body=inspection_title,area='Reminder', inspection_no_id=insp_id, send_to=send_to,send_desig=send_desig)
            messages.success(request, 'Reminder has been send')
            
        except:
            print("error on sending")
            messages.error(
                request, 'Email send failed. Please Try Again.')  

        return JsonResponse({'data': 'data'}, safe=False)
    return JsonResponse({'success': False}, status=400)





def close_compliance_checklist(request):

    # mydata=list(m1.Inspection_details.objects.filter(status='Close').values('inspection_no','inspection_note_no', 'inspection_title','zone','inspected_on','division','dept','location','report_path').order_by('-inspection_no'))
    empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    if empnox:
        empno = empnox[0].designation_code
    
        mydata=list(m1.Inspection_details.objects.filter(status_flag=4, inspection_officer=empno).values().order_by('-inspection_no'))
        
        for i in mydata:
            location = list(m1.Insp_multi_location.objects.filter(inspection_no=i['inspection_no']).values())
            print(location)
            
            insp = m1.Marked_Officers.objects.filter(item_no__inspection_no=i['inspection_no'])
            over_all = insp.count()
            remaning = insp.filter(status_flag=3).count()
            if over_all != 0:
                persentage  = (remaning/over_all)*100
                persentage = round(persentage)
            else:
                persentage = 0
            i.update({'location_item': location, 'persentage': persentage})
        print(mydata)
        
        list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code')
        list4=[]
        for i in list3:
            list4.append(i['location_code'])    
        list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code')
        list2=[]
        for i in list1:
            list2.append(i['location_code'])
            
        list5=list(models.departMast.objects.all().values('department_name')) 
        item=[] 
        # print(list5)
                    
        context={
            'Zone':list2 ,
                'division':list4,
                'department':list5,
                'item':item,
                'mydata': mydata,
            }

        if request.method == 'POST':
            print('@@@@@@@@@@@@@')
            rly=request.POST.get('zone')
            div=request.POST.get('division')
            dept=request.POST.get('department')
            loc=request.POST.get('loc')
            start_date=request.POST.get('start')
            end_date=request.POST.get('txtDate2')
            get_designation=request.POST.get('get_designation')
            print(rly,div,dept,loc,start_date,end_date,get_designation,"~~~~~~~~~")
            
            
            mydata=m1.Inspection_details.objects.filter(status_flag=4).values('inspection_no','inspection_note_no', 'inspection_title','inspected_on','report_path').order_by('-inspection_no')
            
            context={
                'Zone':list2 ,
                'division':list4,
                'department':list5,
                'item':item,
                'mydata': mydata,
            }
            
            return render(request,"close_compliance_checklist.html",context)
        
        return render(request,"close_compliance_checklist.html",context)
    else:
        messages.error(request, 'You are not authorize to see inspection. Please contact to admin')
        return render(request,"close_compliance_checklist.html")



def corrigendum_compliance_checklist(request):

    empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    if empnox:
        empno = empnox[0].designation_code

        list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code')
        list4=[]
        for i in list3:
            list4.append(i['location_code'])    
        list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_code')
        list2=[]
        for i in list1:
            list2.append(i['location_code'])
            
        list5=list(models.departMast.objects.all().values('department_name')) 
        item=[] 
        # print(list5)

        obj1 = m1.Marked_Officers.objects.filter(status_flag=4, item_no__inspection_no__inspection_officer=empno).values_list('item_no__inspection_no', flat=True).distinct()
        print('obj1', obj1)
        mydata =[]
        # for i in obj1:
        #     insp = i['item_no__inspection_no']
        mydata = list(m1.Inspection_details.objects.filter(inspection_no__in=obj1).values())
        
        for j in mydata:
            insp = j['inspection_no']
            location = list(m1.Insp_multi_location.objects.filter(inspection_no=insp).values())
            j.update({'location_item': location})
                    
        context={
            'Zone':list2 ,
                'division':list4,
                'department':list5,
                'item':item,
                'mydata': mydata,
            }
        print(mydata)
        if request.method == 'POST':
            print('@@@@@@@@@@@@@')
            rly=request.POST.get('zone')
            div=request.POST.get('division')
            dept=request.POST.get('department')
            loc=request.POST.get('loc')
            start_date=request.POST.get('start')
            end_date=request.POST.get('txtDate2')
            get_designation=request.POST.get('get_designation')
            print(rly,div,dept,loc,start_date,end_date,get_designation,"~~~~~~~~~")
            
            
            # mydata=m1.Inspection_details.objects.filter(zone=rly,division=div,dept=dept).values('inspection_no','inspection_note_no', 'inspection_title','inspected_on', 'zone','division','dept','location','report_path').order_by('-inspection_no')
            mydata1 =[]
            for i in obj1:
                insp = i['item_no__inspection_no']
                mydata = list(m1.Inspection_details.objects.filter(inspection_no=insp, zone=rly,division=div,dept=dept).values())
                mydata1.extend(mydata)
                print('iiiiiiiiiiiii',  mydata)

            context={
                'Zone':list2 ,
                'division':list4,
                'department':list5,
                'item':item,
                'mydata': mydata1,
            }
            
            return render(request,"corrigendum_compliance_checklist.html",context)
        
        return render(request,"corrigendum_compliance_checklist.html",context)
    else:
        messages.error(request, 'You are not authorize to see inspection. Please contact to admin')
        return render(request,"corrigendum_compliance_checklist.html")



def corrigendumReportReply(request, insp_id):

    ins_title=list(m1.Inspection_details.objects.filter(inspection_no=insp_id).values())
    item_details1= list(m1.Item_details.objects.filter(inspection_no_id=insp_id).values().order_by('item_no'))
    # inspection_done = m1.Inspection_details.objects.filter(inspection_no=insp_id).values('created_by__empname')
    # print('inspection_done', inspection_done)
    multi_loc = m1.Insp_multi_location.objects.filter(inspection_no_id=insp_id).values()
    for j in item_details1:
        
        if j['type'] == 'SH':
            mark=m1.Marked_Officers.objects.filter(item_no=j['item_no']).values()
            # print('mmmmmmmmmmm', mark)
            # print('---------', j['item_no'])
            # mrkoffi = {}
            # desig_longdesc1 =''
            # marked_officers1 = []
            # for x in mark:
            #     print('xxxxxxxxx', x['myuser_id_id'])
                
            #     marked=m1.empmast.objects.filter(myuser_id=x['myuser_id_id'])
            #     # print('yyyyyyyy', marked[0].desig_longdesc)
            #     if marked[0].desig_longdesc:
            #         desig_longdesc1 += marked[0].desig_longdesc+','
            #     else:
            #         desig_longdesc1 =''
            #     marked_officers1.append(marked[0].empno)

            # # print('kkkkkkkkkkkkkkk', desig_longdesc1)
            # mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': desig_longdesc1})
            
            for x in mark:
                #marked=m1.empmast.objects.filter(myuser_id=x['myuser_id_id'])
                marked=models.Level_Desig.objects.filter(designation_code=x['marked_to_id'])
                desig_longdesc1 ='NA'
                if marked[0].designation:
                    desig_longdesc1 = marked[0].designation    
                marked_officers1 = marked[0].empno
                print('uuuuuuuuuu', marked[0].designation)
                x.update({'marked_officers': marked_officers1, 'desig_longdesc': desig_longdesc1})
            j.update({'mrkoffi': mark})
            
        
    ins_title[0].update({'item_details1': item_details1})
    # print('00000000', ins_title)
    print('00000000', ins_title)
    # print('mmmmmmmmmmm', mark)
    empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
    desig =''
    zone =models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    division =models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
    department =models.departMast.objects.all().values('department_name')
    alldesig =models.Level_Desig.objects.values('designation').distinct().order_by('designation')
    if empnox:
        empno = empnox[0].designation_code
        desig = empnox[0].designation
    context={
        'ins_title':ins_title,
       'item_details1': item_details1,
        'insp_number': insp_id,
        'multi_loc': multi_loc,
        'desig': desig,
        'zone': zone,
        'division': division,
        'department': department,
        'alldesig': alldesig

        }  
        
    return render(request, 'corrigendumReportReply.html', context)








def saveCorrigendumOff(request):
    if request.method == 'GET' or request.is_ajax:
        empid = request.GET.get('empid')
        offid = request.GET.get('offid')
        
        emp = m1.empmast.objects.filter(empno=empid)
        obj = m1.Marked_Officers.objects.filter(marked_no=offid)
        
        m1.Marked_Officers.objects.filter(marked_no=offid).update(
            status='R',
            myuser_id=emp[0].myuser_id,
            # marked_to_id=obj[0].marked_to,
            # item_no=obj[0].item_no
            status_flag=1
             
             )
        print('[[[[[[[[[[[[[[[[[[[[[[[[[[[')
        return JsonResponse({'data': 'saved'}, safe=False)
    return JsonResponse({'success': False}, status=400)


# def update_email(request):
#     obj = m1.empmast.objects.values()
#     for i in range(len(obj)):
#         email = 'cris'+str(i).zfill(4)+'@cris.itpi'
#         # obx = models.Level_Desig.objects.filter(empno_id=i['username'], official_email_ID__isnull=True).values('official_email_ID')
#         m1.empmast.objects.filter(empno=obj[i]['empno']).update(email=email)
#         # obx = models.Level_Desig.objects.filter(empno_id=i['username'], official_email_ID__isnull=True).values('official_email_ID')
#         # if obx:
#         #     print(i['email'])
#         #     print(obx)
#         #     models.Level_Desig.objects.filter(empno_id=i['username'], official_email_ID__isnull=True).update(official_email_ID=i['email'])
#         # # if models.Level_Desig.objects.filter(empno_id=i['username'])[0].official_email_ID:
#         #     continue
#         # else:
#         #     obx.update(official_email_ID=i['email'])

#     return HttpResponse('success')
