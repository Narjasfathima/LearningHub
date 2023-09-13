from django.urls import path
from .views import *



urlpatterns=[
    path('checkteachreg',check_teacher_reg,name='c_teach_reg'),
    path('teachreg',TeacherregView.as_view(),name='reg_teach'),
    path('viewprofile',ProfileView.as_view(),name='view_profile'),
    path('editprofile/<int:id>',EditProfileView.as_view(),name='edt_profile'),

    
    path('qaquestview',QaListView.as_view(),name='qa_teach_questv'),
    path('qaansview/<int:id>',QaTeacherAnswerView.as_view(),name='qa_teach_ansv'),

    path('addcourse',AddCourseView.as_view(),name='add_course'),
    path('courselist',CourseListView.as_view(),name='t_course_list'),
    path('storecid/<int:id>',store_cid_session,name='session_cid'),
    
    path('coursehome',course_home_view,name='tc_home'),
    path('addtutorial',AddTutorialView.as_view(),name='add_tut'),
    path('edittutorial',EditTutorialView.as_view(),name='edit_tut'),
    path('dlttutorial/<int:id>',delete_tutorialView,name='dlt_tut'),

    path('viewtutorial',TutorialListView.as_view(),name='view_tut'),
    path('storetutid/<int:id>',store_tutid_session,name='session_tutid'),

    path('tuthome',tutorial_home_view,name='tut_home'),
    
    path('addassign',AddAssignmentView.as_view(),name='add_ass'),
    path('viewassign',AssignmentListView.as_view(),name='t_ass_list'),
    path('editassign/<int:id>',EditAssignmentView.as_view(),name='edit_ass'),
    path('deleteassign/<int:id>',delete_assignmentView,name='dlt_ass'),
    path('validateassign',ValidateAssignmentListView.as_view(),name='validate_ass'),
    path('studassign/<int:id>',StudentAssignmentView.as_view(),name='stud_ass'),
    path('acceptassign/<int:id>',accept_assignmentView,name='accept_ass'),
    path('rejectassign/<int:id>',reject_assignmentView,name='reject_ass'),

    path('addnote',AddNoteView.as_view(),name='add_note'),
    path('viewnote',NoteListView.as_view(),name='t_note_list'),
    path('editnote/<int:id>',EditNoteView.as_view(),name='edit_note'),
    path('deletenote/<int:id>',delete_noteView,name='dlt_note'),
    
    path('addtest',AddTestView.as_view(),name='add_test'),
    path('addquestion',AddQuestionView.as_view(),name='add_question'),
    
    path('testlist',TestListView.as_view(),name='t_test_list'),
    path('viewtestquest<int:id>',Test_QuestionView.as_view(),name='tq_view'),

    path('edittest',EditTestView.as_view(),name='edit_test'),
    path('editquest',EditQuestionsView.as_view(),name='edit_question'),
    path('dlttq/<int:id>',dlt_testquest_view,name='dlt_tq'),

    
    path('checktest',CheckTestListView.as_view(),name='check_testl'),
    path('checktestmark/<int:id>',CheckTestMarkView.as_view(),name='check_testm'),

    path('rooms',RoomListView.as_view(),name='teach_rooms'),
    path('room/<slug:slug>/',RoomView.as_view(), name='teach_room'),
]