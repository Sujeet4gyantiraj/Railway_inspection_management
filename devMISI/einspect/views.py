#API methods for Models Screen
import imp
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt   #csrf allows other domains to access our page
from rest_framework.parsers import JSONParser  #to pas s incoming data to the models
from django.http.response import JsonResponse
from einspect.models import *
from myadmin.models import *
from inspects.models import *
from einspect.serializer import *
from django.core.files.storage import default_storage

# Create your views here.

@csrf_exempt
def station_masterAPI(request,id=0):  
    #Create 
    if request.method=='GET':
        station_masters=station_master.objects.all()
        station_masters_serializer=station_masterSerializer(station_masters,many=True)
        return JsonResponse(station_masters_serializer.data,safe=False)
    #retrive
    elif request.method=='POST':
        station_masters_data=JSONParser().parse(request)
        station_masters_serializer=station_masterSerializer(data=station_masters_data)
        if station_masters_serializer.is_valid():
            station_masters_serializer.save()
            return JsonResponse('Data Added Successfully!!',safe=False)
        return JsonResponse('Data Addition Unsuccessfully!!',safe=False)
    #Update an existing Record
    elif request.method=='PUT':
        station_master_data=JSONParser().parse(request)
        #get data based on primary key
        station_masters=station_master.objects.get(stnshortcode=station_master_data['stnshortcode'])
        #map that data in serializer
        station_masters_serializer=station_masterSerializer(station_masters,data=station_master_data)
        if station_masters_serializer.is_valid():
            station_masters_serializer.save()
            return JsonResponse('Data Updation Successfully!!',safe=False) #success message for sucessfull updation
        return JsonResponse('Data Updation Unsuccessfully!!',safe=False)
    #delete an existing record
    elif request.method=='DELETE':
         #for deletion we send the pk to search the database
         station_masters=station_master.objects.get(stnshortcode=id) 
         station_masters.delete()
         return JsonResponse('Deletion is Successfull!!',safe=False)

@csrf_exempt
def stationcat_masterAPI(request,id=0):  
    #Create 
    if request.method=='GET':
        stationcat_masters=stationcat_master.objects.all()
        stationcat_masters_serializer=stationcat_masterSerializer(stationcat_masters,many=True)
        return JsonResponse(stationcat_masters_serializer.data,safe=False)
    #retrive
    elif request.method=='POST':
        stationcat_masters_data=JSONParser().parse(request)
        stationcat_master_serializer=stationcat_masterSerializer(data=stationcat_masters_data)
        if stationcat_master_serializer.is_valid():
            stationcat_master_serializer.save()
            return JsonResponse('Data Added Successfully!!',safe=False)
        return JsonResponse('Data Addition Unsuccessfully!!',safe=False)
    #Update an existing Record
    elif request.method=='PUT':
        stationcat_masters_data=JSONParser().parse(request)
        #get data based on primary key
        stationcat_masters=stationcat_master.objects.get(stnid=stationcat_masters_data['stnid'])
        #map that data in serializer
        stationcat_masters_serializer=stationcat_masterSerializer(stationcat_masters,data=stationcat_masters_data)
        if stationcat_masters_serializer.is_valid():
            stationcat_masters_serializer.save()
            return JsonResponse('Data Updation Successfully!!',safe=False) #success message for sucessfull updation
        return JsonResponse('Data Updation Unsuccessfully!!',safe=False)

    #delete an existing record
    elif request.method=='DELETE':
         #for deletion we send the pk to search the database
         stationcat_masters=stationcat_master.objects.get(stnid=id) 
         stationcat_masters.delete()
         return JsonResponse('Deletion is Successfull!!',safe=False)

@csrf_exempt
def train_masterAPI(request,id=0):  
    #Create 
    if request.method=='GET':
        train_masters=train_master.objects.all()
        train_masters_serializer=train_masterSerializer(train_masters,many=True)
        return JsonResponse(train_masters_serializer.data,safe=False)

@csrf_exempt
def station_masterAPI(request,id=0):  
    #Create 
    if request.method=='GET':
        station_masters=station_master.objects.all()
        station_masters_serializer=station_masterSerializer(station_masters,many=True)
        return JsonResponse(station_masters_serializer.data,safe=False)

@csrf_exempt
def section_masterAPI(request,id=0):  
    #Create 
    if request.method=='GET':
        section_masters=section_master.objects.all()
        section_masters_serializer=section_masterSerializer(section_masters,many=True)
        return JsonResponse(section_masters_serializer.data,safe=False)

@csrf_exempt
def runningRoom_masterAPI(request,id=0):  
    #Create 
    if request.method=='GET':
        runningroom_masters=runningroom_master.objects.all()
        runningroom_masters_serializer=runningroom_masterSerializer(runningroom_masters,many=True)
        return JsonResponse(runningroom_masters_serializer.data,safe=False)

@csrf_exempt
def designation_masterAPI(request,id=0):  
    #Create 
    if request.method=='GET':
        level_desig_masters=Level_Desig.objects.all()
        level_desig_masters_serializer=level_desigSerializer(level_desig_masters,many=True)
        return JsonResponse(level_desig_masters_serializer.data,safe=False)

  

@csrf_exempt
def train_masterAPI(request,id=0):  
    #Create 
    if request.method=='GET':
        train_masters=train_master.objects.all()
        train_masters_serializer=train_masterSerializer(train_masters,many=True)
        return JsonResponse(train_masters_serializer.data,safe=False)
    #retrive
    elif request.method=='POST':
        train_masters_data=JSONParser().parse(request)
        train_master_serializer=train_masterSerializer(data=train_masters_data)
        if train_master_serializer.is_valid():
            train_master_serializer.save()
            return JsonResponse('Data Added Successfully!!',safe=False)
        return JsonResponse('Data Addition Unsuccessfully!!',safe=False)
    #Update an existing Record
    elif request.method=='PUT':
        train_masters_data=JSONParser().parse(request)
        #get data based on primary key
        train_masters=train_master.objects.get(tnid=train_masters_data['tnid'])
        #map that data in serializer
        train_masters_serializer=train_masterSerializer(train_masters,data=train_masters_data)
        if train_masters_serializer.is_valid():
            train_masters_serializer.save()
            return JsonResponse('Data Updation Successfully!!',safe=False) #success message for sucessfull updation
        return JsonResponse('Data Updation Unsuccessfully!!',safe=False)

    #delete an existing record
    elif request.method=='DELETE':
         #for deletion we send the pk to search the database
         train_masters=train_master.objects.get(tnid=id) 
         train_masters.delete()
         return JsonResponse('Deletion is Successfull!!',safe=False)

@csrf_exempt
def empmastAPI(request,id=0):  
    #Create 
    if request.method=='GET':
        empmasts=empmast.objects.all()
        empmasts_serializer=empmastSerializer(empmasts,many=True)
        return JsonResponse(empmasts_serializer.data,safe=False)
    #retrive
    elif request.method=='POST':
        empmasts_data=JSONParser().parse(request)
        empmast_serializer=empmastSerializer(data=empmasts_data)
        if empmast_serializer.is_valid():
            empmast_serializer.save()
            return JsonResponse('Data Added Successfully!!',safe=False)
        return JsonResponse('Data Addition Unsuccessfully!!',safe=False)
    #Update an existing Record
    elif request.method=='PUT':
        empmasts_data=JSONParser().parse(request)
        #get data based on primary key
        empmasts=empmast.objects.get(empno=empmasts_data['empno'])
        #map that data in serializer
        empmasts_serializer=empmastSerializer(empmasts,data=empmasts_data)
        if empmasts_serializer.is_valid():
            empmasts_serializer.save()
            return JsonResponse('Data Updation Successfully!!',safe=False) #success message for sucessfull updation
        return JsonResponse('Data Updation Unsuccessfully!!',safe=False)

    #delete an existing record
    elif request.method=='DELETE':
         #for deletion we send the pk to search the database
         empmasts=empmast.objects.get(empno=id) 
         empmast.delete()
         return JsonResponse('Deletion is Successfull!!',safe=False)

@csrf_exempt
def inspectiontype_masterAPI(request,id=0):  
  
    if request.method=='GET':
        inspectiontype_masters=inspectiontype_master.objects.filter(parent_id__isnull=True,delete_flag=False).order_by('instypeid')
        inspectiontype_masters_serializer=inspectiontype_masterSerializer(inspectiontype_masters,many=True)
        return JsonResponse(inspectiontype_masters_serializer.data,safe=False)   
   
    elif request.method=='POST':
        inspectiontype_masters_data=JSONParser().parse(request)
        inspectiontype_masters_serializer=inspectiontype_masterSerializer(data=inspectiontype_masters_data)
        if inspectiontype_masters_serializer.is_valid():
            inspectiontype_masters_serializer.save()
            return JsonResponse('Data Added Successfully!!',safe=False)
        return JsonResponse('Failed to Add.!',safe=False)
 
    elif request.method=='PUT':
        inspectiontype_masters_data=JSONParser().parse(request)
        inspectiontype_masters=inspectiontype_master.objects.get(instypeid=inspectiontype_masters_data['instypeid'])
        inspectiontype_masters_serializer=inspectiontype_masterSerializer(inspectiontype_masters,data=inspectiontype_masters_data)
        if inspectiontype_masters_serializer.is_valid():
            inspectiontype_masters_serializer.save()
            print(inspectiontype_masters_data)
            return JsonResponse('Data Updation Successfully!!',safe=False) 
        return JsonResponse('Failed to Update',safe=False)

    elif request.method=='DELETE':
            #for deletion we send the pk to search the database
        inspectiontype_master.objects.filter(instypeid = id).update(delete_flag= True)    
        inspectiontype_masters=inspectiontype_master.objects.filter(delete_flag = False).values()
        return JsonResponse('Category disabling is Successfull!!',safe=False)


@csrf_exempt
def inspectiontype_childData_masterAPI(request,id=0):  
    #Create 
    if request.method=='GET':        
        questiontype_masters=inspectiontype_master.objects.filter(parent_id = id,delete_flag = False).order_by('instypeid').values()
        questiontype_masters_serializer=inspectiontype_masterSerializer(questiontype_masters,many=True)
        return JsonResponse(questiontype_masters_serializer.data,safe=False)

    #Delete an existing record
    elif request.method=='DELETE':
            #for deletion we send the pk to search the database
        inspectiontype_master.objects.filter(instypeid = id).update(delete_flag= True)    
        questiontype_masters=inspectiontype_master.objects.filter(delete_flag = False).values()
        return JsonResponse('Category disabling is Successfull!!',safe=False)

@csrf_exempt
def questionare_masterAPI(request,id=0):  
  
    if request.method=='GET':
        questionare_masters=questionare_master.objects.filter(instypeid_id=id,delete_flag=False).order_by('qid')
        questionare_masters_serializer=questionare_masterSerializer(questionare_masters,many=True)
        return JsonResponse(questionare_masters_serializer.data,safe=False)   

    elif request.method=='POST':
        questionare_masters_data=JSONParser().parse(request)
        questionare_masters_serializer=questionare_masterSerializer(data=questionare_masters_data)
        if questionare_masters_serializer.is_valid():
            questionare_masters_serializer.save()
            return JsonResponse('Data Added Successfully!!',safe=False)
        return JsonResponse('Failed to Add.!',safe=False)
 
    elif request.method=='PUT':
        questionare_masters_data=JSONParser().parse(request)
        questionare_masters=questionare_master.objects.get(qid=questionare_masters_data['qid'])
        questionare_masters_serializer=questionare_masterSerializer(questionare_masters,data=questionare_masters_data)
        if questionare_masters_serializer.is_valid():
            questionare_masters_serializer.save()
            print(questionare_masters_data)
            return JsonResponse('Data Updation Successfully!!',safe=False) 
        return JsonResponse('Failed to Update',safe=False)

    elif request.method=='DELETE':
            #for deletion we send the pk to search the database
        questionare_master.objects.filter(qid = id).update(delete_flag= True)    
        questionare_masters=questionare_master.objects.filter(delete_flag = False).values()
        return JsonResponse('Category disabling is Successfull!!',safe=False)

@csrf_exempt
def einspectionItemDetailAPI(request,id=0):    
    if request.method=='GET':
        einspection_Item_Details=einspection_item_detail.objects.values()
        einspection_Item_Details_serializer=einspection_item_detailSerializer(einspection_Item_Details,many=True)
        return JsonResponse(einspection_Item_Details_serializer.data,safe=False)   

    elif request.method=='POST':
        einspection_Item_Details_data=JSONParser().parse(request)
        einspection_Item_Details_serializer=einspection_item_detailSerializer(data=einspection_Item_Details_data)
        if einspection_Item_Details_serializer.is_valid():
            einspection_Item_Details_serializer.save()
            return JsonResponse('Data Added Successfully!!',safe=False)
        return JsonResponse('Failed to Add.!',safe=False)

    elif request.method=='PUT':
        einspection_Item_Details_data=JSONParser().parse(request)
        einspection_Item_Details=einspection_Item_Detail.objects.get(qid=einspection_Item_Details_data['qid'])
        einspection_Item_Details_serializer=einspection_item_detailSerializer(einspection_Item_Details,data=einspection_Item_Details_data)
        if einspection_item_detailSerializer.is_valid():
            einspection_item_detailSerializer.save()
            print(einspection_item_detail_data)
            return JsonResponse('Data Updation Successfully!!',safe=False) 
        return JsonResponse('Failed to Update',safe=False)

    elif request.method=='DELETE':
            #for deletion we send the pk to search the database
        einspection_Item_Detail.objects.filter(qid = id).update(delete_flag= True)    
        einspection_Item_Details=einspection_Item_Detail.objects.filter(delete_flag = False).values()
        return JsonResponse('Category disabling is Successfull!!',safe=False)

@csrf_exempt
def saveFile(request): 
    file = request.FILES['UploadedFile']
    file_name = default_storage.save(file.name,file)
    return JsonResponse(file_name,safe=False)


@csrf_exempt
def choicetype_masterAPI(request,id=0):  
    #Create 
    if request.method=='GET':        
        choicetype_masters=choicetype_master.objects.order_by('cid').values()
        choicetype_masters_serializer=choicetype_masterSerializer(choicetype_masters,many=True)
        return JsonResponse(choicetype_masters_serializer.data,safe=False)

@csrf_exempt
def radio_options_masterAPI(request,id=0):  
    #Create 
    if request.method=='GET':        
        radio_options_masters=radio_options.objects.filter(rscore=id).values()
        radio_options_masters_serializer=radio_optionSerializer(radio_options_masters,many=True)
        return JsonResponse(radio_options_masters_serializer.data,safe=False)

@csrf_exempt
def radio_options_masterByIDAPI(request,id=0):  
    #Create 
    if request.method=='GET':        
        radio_options_masters=radio_options.objects.filter(rid=id).values()
        radio_options_masters_serializer=radio_optionSerializer(radio_options_masters,many=True)
        return JsonResponse(radio_options_masters_serializer.data,safe=False)


@csrf_exempt
def dropdown_options_masterAPI(request,id=0):  
    #Create 
    if request.method=='GET':        
        dropdown_options_masters=dropdown_options.objects.values()
        dropdown_options_masters_serializer=dropdown_optionSerializer(dropdown_options_masters,many=True)
        return JsonResponse(dropdown_options_masters_serializer.data,safe=False)
