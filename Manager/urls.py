from django.urls import path
from .views import *

# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns=[
    path('signup',SignUpView.as_view(),name='signup'),
    path('logout',LogOutView.as_view(),name='logout'),

    path('changepwd', change_password, name='change_password'),

    path('password-reset/', PasswordResetView.as_view(template_name='password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),


    path('manhome',ManagerHomeView.as_view(),name='man_home'),
    path('userhome',UserHomeView.as_view(),name='user_home'),
    path('studhome',StudentHomeView.as_view(),name='stud_home'),
    path('teachhome',TeacherHomeView.as_view(),name='teach_home'),

    path('teachlist',TeacherListView.as_view(),name='teach_list'),
    path('teachverifylist',TeacherVerifyListView.as_view(),name='teachverify_list'),
    path('acceptteach/<int:id>',accept_teacher,name='accept_teach'),
    path('rejectteach/<int:id>',reject_teacher,name='reject_teach'),
    path('resumeteach/<int:id>',resume_teacher,name='resume_teach'),
    path('dltteach/<int:id>/<int:uid>',delete_teacher,name='dlt_teach'),

    path('addcont',AddContentView.as_view(),name='add_content'),
    path('contlist',ContentListView.as_view(),name='content_list'),
    path('edtcont/<int:id>',EditContentView.as_view(),name='edt_cont'),
    path('dltcont/<int:id>',delete_contentView,name='dlt_cont'),

    path('adddoc',AddDocView.as_view(),name='add_doc'),
    path('doclist',DocListView.as_view(),name='doc_list'),
    path('edtdoc/<int:id>',EditDocView.as_view(),name='edt_doc'),
    path('dltdoc/<int:id>',delete_docView,name='dlt_doc'),

    path('addevent',AddEventView.as_view(),name='add_event'),
    path('eventlist',EventListView.as_view(),name='event_list'),
    path('edtevent/<int:id>',EditEventView.as_view(),name='edt_event'),
    path('dltevent/<int:id>',delete_eventView,name='dlt_event'),
    path('eventcalender',UserEventListView.as_view(),name='event_calender'),

    
    path('usercontview',UserContentListView.as_view(),name='user_contv'),
    
    path('userdocview',UserDocListView.as_view(),name='user_docv'),
    
    path('qateachview',QaTeacherListView.as_view(),name='qa_teachv'),
    path('qaquestview/<int:id>',QaQuestView.as_view(),name='qa_questv'),
    path('addquestqa/<int:id>',AddQuestQaView.as_view(),name='qa_add_quest'),
    path('dltquestqa/<int:id>',delete_questqaView,name='qa_dlt_quest'),
    path('viewansqa/<int:id>',AnswerQaView.as_view(),name='qa_ansv'),

    
    path('coursevallist',CourseValidateListView.as_view(),name='val_course_listv'),
    path('coursevalview/<int:cid>',CourseValidateView.as_view(),name='val_coursev'),
    path('coursereject/<int:cid>',reject_courseview,name='reject_coursev'),
    path('courseaccept/<int:cid>',accept_courseview,name='accept_coursev'),
    path('coursesale/<int:cid>',on_sale_courseview,name='sale_coursev'),
    path('coursesuspend/<int:cid>',on_suspend_courseview,name='suspend_coursev'),
    path('coursetut/<int:cid>',wtut_courseview,name='wtut_coursev'),
    path('courselist',CourseListView.as_view(),name='course_listv'),
    path('coursedlt/<int:cid>',delete_courseview,name='dlt_coursev'),
    path('courseview',UserCourseListView.as_view(),name='course_view'),

   


]