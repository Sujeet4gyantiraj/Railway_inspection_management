# from rest_framework import serializers
# from myadmin.models import *
# from einspect.models import *
# from inspects.models import *

# class station_masterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=station_master
#         fields=('stnshortcode','rly_id_id','lastmodified_by','created_by',
#         'station_name','created_on','lastmodified_on','delete_flag')

# class stationcat_masterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=stationcat_master
#         fields=('stnid','stn_category','lastmodified_by','created_by',
#         'created_on','lastmodified_on','delete_flag')

# class runningroom_masterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=runningroom_master
#         fields=('rrid','rr_name','rr_code','stnshortcode','created_by','lastmodified_by',
#         'created_on','lastmodified_on','delete_flag')

# class train_masterSerializer(serializers.ModelSerializer):
#    class Meta:
#     model= train_master
#     fields=('tnid','train_no', 'train_name','tn_category', 'stnsource_code','stndest_code', 'total_coach', 
#      'lastmodified_by', 'created_by', 'created_on','lastmodified_on','delete_flag')

# class questionare_masterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=questionare_master
#         fields=('qid','instypeid_id','activity','choicetype','delete_flag','doption','roption1','roption2','created_by','lastmodified_by', 'created_on','lastmodified_on')

# class inspectiontype_masterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= inspectiontype_master
#         fields=('instypeid', 'name','shortcode','entity','img_path','parent_id', 'statuschecklist',
#            'lastmodified_by','created_by','created_on', 'lastmodified_on','delete_flag') 


# class  einspection_item_detailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= einspection_item_detail
#         fields=('eitemid','einspno', 'qid','status','value','remarks', 'target_date', 
#         'qtype','created_by', 'lastmodified_by', 'created_on','lastmodified_on', 'delete_flag')


# class section_masterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=section_master
#         fields=('secid','section_code','section_name','railway_code','division_id','secstart_code','secend_code', 'route',
#                 'section_length', 'lastmodified_by','created_by','created_on','lastmodified_on','delete_flag'
#                 )


# class einspection_detailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=einspection_details
#         fields=('einspno','instypeid','inspection_officer_id','inspected_on','inspection_title','designation',
#                 'inspection_note_no','status','dept','report_path','rly_id_id','startstn','endstn','entitydetails',
#                 'entityid','rostetrdetail_id','lastmodified_by','created_by','created_on','lastmodified_on','delete_flag'
#                 )


# class einsp_markedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=einsp_marked
#         fields=('id','eitemid','marked_to','marked_emp_id','compliance','compliance_recieved_on',
#                 'status_flag','revert','reverted_on','lastmodified_by','created_by',
#                 'created_on','lastmodified_on','delete_flag'
#                 )

# class einsp_roasterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = einsp_roster
#         fields = ('erosterid','fromdate','todate','status','rly_id_id','lastmodified_by',
#         'created_by','created_on','lastmodified_on','delete_flag')


# class roster_detailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = roster_detail
#         fields = ('rostdetailid','roster_id','inspection_officer_id','doi','inspectiontype_id',
#         'inspectionof','section','startstn','endstn','status','lastmodified_by','created_by','created_on',
#         'lastmodified_on','delete_flag')

# class  railwayLocationMasterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=railwayLocationMaster
#         fields=('rly_unit_code',
#                 'location_code',
#                 'location_type',
#                 'location_description',
#                 'parent_location_code',
#                 'last_update',
#                 'modified_by',
#                 'station_code',
#                 'rstype',
#                 'location_type_desc'
#                 )

# class  empmastSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=empmast
#         fields=('hrms_id','empno','empname','empmname','emplname','birthdate','appointmentdate','superannuation_date',
#                 'gender','email','contactno','railwaygroup','pc7_level','billunit','service_status','desig_longdesc',
#                 'desig_id','station_des','dept_desc','subdepartment','currentzone','currentunitdivision','rl_type',
#                 'myuser_id','role','rly_id','profile_modified_by','profile_modified_on'
#                 )



# class choicetype_masterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=choicetype_master
#         fields=('cid','input_type')

# class radio_optionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=radio_options
#         fields=('rid','rscore','rlabel')

# class dropdown_optionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=dropdown_options
#         fields=('did','dmaster')

# class level_desigSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Level_Desig
#         fields = ( 'designation_code' ,  'designation' , 'department' , 'effectdate' , 'parent_desig_code' , 'department_code' ,'rly_unit' , 'pc7_levelmin' , 'pc7_levelmax'  , 'modified_by' , 'desig_user' , 'status', 'empno', 'd_level'
#         )


