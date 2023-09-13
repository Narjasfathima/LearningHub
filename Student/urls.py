from django.urls import path
from .views import *



urlpatterns=[
    path('studreg',StudentregView.as_view(),name='reg_stud'),
    path('sprofile',StudProfileView.as_view(),name='s_profile'),
    path('edtprofile/<int:id>',StudEditProfileView.as_view(),name='edt_sprofile'),

    path('courselist',CourseListView.as_view(),name='course_list'),
    path('courseview/<int:cid>',CourseView.as_view(),name='course_view'),
    path('coursepurcahse/<int:cid>',PurchaseCourseView.as_view(),name='course_purchase'),
    path('purchasepay/<int:id>',pay_purchase_view,name='purchase_pay'),

    path('boughtcourselist',BoughtCourseListView.as_view(),name='bcourse_list'),
    path('ctutorials/<int:id>',CourseTutorialListView.as_view(),name='ctuto_list'),
    path('storetutid/<int:id>',stud_store_tutid_session,name='s_tut_id'),
    path('studtuthome',stud_tutorial_home_view,name='stud_tut_home'),
    
    path('studnotelist',StudNoteListView.as_view(),name='stud_note_list'),
    
    path('studassignlist',StudAssignmentListView.as_view(),name='stud_assign_list'),
    path('addassfile/<int:id>',AddAssignmentFileView.as_view(),name='add_ass_file'),
    
    path('studtestlist',StudTestListView.as_view(),name='stud_test_list'),
    path('testpaper/<int:id>',AttendTestView.as_view(),name='test_paper'),

    
    path('rooms',RoomListView.as_view(),name='stud_rooms'),
    path('room/<slug:slug>/',RoomView.as_view(), name='stud_room'),

]