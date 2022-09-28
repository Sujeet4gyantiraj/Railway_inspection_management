from django.urls import path, re_path
from django.conf import settings
from einspect.models import *
from myadmin.models import *
from einspect import views as v1
from inspects import views as v2
from myadmin import views as v3
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[   
    re_path(r'^empmast/$', v1.empmastAPI),
    re_path(r'^empmast/([0-9]+)$',v1.empmastAPI),

    re_path(r'^inspectiontype_master/$', v1.inspectiontype_masterAPI),
    re_path(r'^inspectiontype_master/([0-9]+)$',v1.inspectiontype_masterAPI),

    re_path(r'^questiontype_master/$', v1.inspectiontype_childData_masterAPI),
    re_path(r'^questiontype_master/([0-9]+)$',v1.inspectiontype_childData_masterAPI),

    re_path(r'^questionare_master/$', v1.questionare_masterAPI),
    re_path(r'^questionare_master/([0-9]+)$',v1.questionare_masterAPI),

    re_path(r'^train_master/$', v1.train_masterAPI),
    re_path(r'^train_master/([0-9]+)$',v1.train_masterAPI),

    re_path(r'^station_master/$', v1.station_masterAPI),
    re_path(r'^station_master/([0-9]+)$',v1.station_masterAPI),

    re_path(r'^section_master/$', v1.section_masterAPI),
    re_path(r'^section_master/([0-9]+)$',v1.section_masterAPI),

    re_path(r'^runningRoom_master/$', v1.runningRoom_masterAPI),
    re_path(r'^runningRoom_master/([0-9]+)$',v1.runningRoom_masterAPI),

    re_path(r'^designation_master/$', v1.designation_masterAPI),
    re_path(r'^designation_master/([0-9]+)$',v1.designation_masterAPI),

    re_path(r'^saveFile$', v1.saveFile),

    re_path(r'^choicetype_master/$', v1.choicetype_masterAPI),
    re_path(r'^choicetype_master/([0-9]+)$',v1.choicetype_masterAPI),

    re_path(r'^radio_options_masters/$', v1.radio_options_masterAPI),
    re_path(r'^radio_options_masters/([0-9]+)$',v1.radio_options_masterAPI),

    re_path(r'^dropdown_options_master/$', v1.dropdown_options_masterAPI),
    re_path(r'^dropdown_options_master/([0-9]+)$',v1.dropdown_options_masterAPI),

    re_path(r'^radio_options_masterByID/$', v1.radio_options_masterByIDAPI),
    re_path(r'^radio_options_masterByID/([0-9]+)$',v1.radio_options_masterByIDAPI),
    
    re_path(r'^einspectionResponses/$', v1.einspectionItemDetailAPI),
    re_path(r'^einspectionResponses/([0-9]+)$',v1.einspectionItemDetailAPI),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

   