from django.forms.models import BaseModelForm
from django.http import HttpResponse

from django.shortcuts import render,redirect

from django.views.generic import View,CreateView,FormView,TemplateView,ListView,DetailView

from .forms import *

from django.urls import reverse_lazy

from django.contrib import messages

from django.contrib.auth import login,authenticate,logout

# DECORATOR
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from Student.views import studreg_required

from django.db.models import Q


from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# DECORATOR 1
def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"Please Login First!!")
            return redirect('login')
    return inner


# DECORATOR 2
def teachreg_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_teacher:
            # messages.success(request,"Welcome Teacher Home!!")
            return fn(request,*args,**kwargs)
        else:            
            return redirect('reg_teach')
    return inner


# DECORATOR 3
def check_is_answer(fn):
    def inner(request,*args,**kwargs):
        qid=kwargs.get('id')
        res=QuestAnswer.objects.get(id=qid)
        if res.is_answer:
            return fn(request,*args,**kwargs)
        else: 
            tid=request.session.get('teach_id')
            teach=Teacher.objects.get(id=tid)
            res=QuestAnswer.objects.filter(user=request.user,teacher=teach)
            res1=res.order_by('-datetime')
            return render(request,"qa_quest_view.html",{"question":res1}) 
    return inner


decs=[never_cache,signin_required,teachreg_required]
decs1=[never_cache,signin_required,studreg_required]
decs2=[never_cache,signin_required]
decs3=[check_is_answer,signin_required]


# Create your views here.


# SIGN-UP
@method_decorator([never_cache],name="dispatch")
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        form_ob=SignUpForm()
        return render(request,"signup.html",{"form":form_ob})
    def post(self,request,*args,**kwargs):
        form_data=SignUpForm(data=request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('signin')
        return render(request,"signup.html",{"form":form_data})


# SIGN-IN
@method_decorator([never_cache],name="dispatch")
class SignInView(FormView):
    template_name="signin.html"
    form_class=SignInForm

    def post(self,request,*args,**kwargs):
        form_data=SignInForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get("username")
            pwd=form_data.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            print(user)
            # manager=authenticate(request,username=uname,password=pwd,is_manager=1)
            if user is not None:
                if user.is_manager:
                    login(request,user)
                    messages.success(request,"Login succesfull!!")
                    return redirect('man_home')
                else:
                    login(request,user)
                    messages.success(request,"Login succesfull!!")
                    return redirect('user_home')
                        
            else:
                messages.error(request,"Failed")
                print("error")
                return redirect('signin')
        return render(request,"signin.html",{"form":form_data})


# CHANGE PASSWORD
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form })


# MANAGER HOME 
@method_decorator(decs2,name="dispatch")
class ManagerHomeView(TemplateView):
    template_name="manager_home.html"

from datetime import date  

# USER HOME
@method_decorator(decs2,name="dispatch")
class UserHomeView(View):
    def get(self,request,*args,**kwargs):
        current_date=timezone.now().date()
        # parsed_date = date.fromisoformat(current_date)
        form_ob=EventCalender.objects.filter(date__gte=current_date)
        return render(request,"user_home.html",{"form":form_ob})

# STUDENT HOME
@method_decorator(decs1,name="dispatch")
class StudentHomeView(View):
    # template_name="stud_home.html"
    def get(self,request,*args,**kwargs):
        if 'stud_id' in self.request.session:
            del self.request.session['stud_id']

        stud=Student.objects.get(user=self.request.user)        
        self.request.session['stud_id']=stud.id
        return render(request,"stud_home.html")

# TEACHER HOME
@method_decorator(decs,name="dispatch")
class TeacherHomeView(TemplateView):
    template_name="teacher_home.html"


# logout
@method_decorator(decs2,name="dispatch")
class LogOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('signin')
    

# AUTHERIZED TEACHER LIST VIEW
@method_decorator(decs2,name="dispatch")
class TeacherListView(ListView):
    template_name="teacher_list.html"
    queryset=Teacher.objects.all()
    context_object_name="teacher"

    def get_queryset(self):
        return Teacher.objects.filter(user__is_teacher=True)
    

# AUTHENTICATE TEACHER LIST VIEW
@method_decorator(decs2,name="dispatch")
class TeacherVerifyListView(ListView):
    template_name="teacher_verify_list.html"
    queryset=Teacher.objects.all()
    context_object_name="teacher"

    
decs2
def accept_teacher(request,*args,**kwargs):
    id=kwargs.get("id")
    res=CustomUser.objects.get(id=id)
    res.is_teacher=True
    res.save()
    teach=Teacher.objects.get(user=res)
     
    # ********************EMAIL*******************************
    subject = 'Accept Teacher Registration'
    content = """
            Dear {tutor_name},

            I hope this message finds you well. I want to express my gratitude for your dedication and commitment to our educational platform. 
            We are excited to have you on board to create an enriching learning experience for our students.
            
            As your registration has been accepted, it's time to move forward with developing a course. 
            
            We appreciate your prompt attention to this matter, as it will allow us to provide the best possible educational experience for our students. 
            If you have any questions or need assistance with any aspect of content development, please do not hesitate to reach out to us.

            Thank you once again for being a part of our educational community. 
            We look forward to the exceptional content you will create for our students

            

            Best regards,
            Manager 
            Learning Hub
    """.format(tutor_name=teach.first_name+" "+teach.last_name)

    from_email = settings.EMAIL_HOST_USER  # Use the sender's email address configured in settings.py
    recipient_list = [teach.email]  # Replace with the recipient's email address

    send_mail(subject, content, from_email, recipient_list)

    # ************************************************************

    return redirect('teachverify_list')

decs2
def reject_teacher(request,*args,**kwargs):
    id=kwargs.get("id")
    res=Teacher.objects.get(id=id)
    res.is_suspend=True
    res.save()
     
    # ********************EMAIL*******************************
    subject = 'Suspend Teacher Registration'
    content = """
            Dear {tutor_name},

            I hope this message finds you well. I wanted to reach out and inform you that, as part of our commitment to delivering high-quality education,
            we have temporarily suspended your registration

            We appreciate your prompt attention to this matter, as it will allow us to provide the best possible educational experience for our students. 
            If you have any questions or need assistance with any aspect of content development, please do not hesitate to reach out to us.

            Thank you once again for being a part of our educational community. 
            We look forward to the exceptional content you will create for our students

            

            Best regards,
            Manager 
            Learning Hub
    """.format(tutor_name=res.first_name+" "+res.last_name)

    from_email = settings.EMAIL_HOST_USER  # Use the sender's email address configured in settings.py
    recipient_list = [res.email]  # Replace with the recipient's email address

    send_mail(subject, content, from_email, recipient_list)

    # ************************************************************

    return redirect('teach_list')

decs2
def resume_teacher(request,*args,**kwargs):
    id=kwargs.get("id")
    res=Teacher.objects.get(id=id)
    res.is_suspend=False
    res.save()
      
    # ********************EMAIL*******************************
    subject = 'Resume Teacher Registration'
    content = """
    Dear {tutor_name},

        I hope this message finds you well. I want to express my gratitude for your dedication and commitment to our educational platform. 
        We are excited to have you on board to create an enriching learning experience for our students.

        As your registration has been accepted, it's time to move forward with developing a course. 

        We appreciate your prompt attention to this matter, as it will allow us to provide the best possible educational experience for our students. 
        If you have any questions or need assistance with any aspect of content development, please do not hesitate to reach out to us.

        Thank you once again for being a part of our educational community. 
        We look forward to the exceptional content you will create for our students

    

        Best regards,
        Manager 
        Learning Hub
    """.format(tutor_name=res.first_name+" "+res.last_name)

    from_email = settings.EMAIL_HOST_USER  # Use the sender's email address configured in settings.py
    recipient_list = [res.email]  # Replace with the recipient's email address

    send_mail(subject, content, from_email, recipient_list)

    # ************************************************************

    return redirect('teachverify_list')

decs2
def delete_teacher(request,*args,**kwargs):
    uid=kwargs.get("uid")
    id=kwargs.get("id")    
    res=Teacher.objects.get(id=id)
    res.delete()
    res1=CustomUser.objects.get(id=uid)
    res1.is_teacher=False
    res1.save()


    # ********************EMAIL*******************************
    subject = 'Reject Teacher Registration '
    content = """
        Dear {tutor_name},

        We appreciate your efforts and the course proposal you submitted to us. However, 
        we regret to inform you that your registration has been rejected due to concerns.

        If you have any questions or need assistance, please do not hesitate to reach out to us.


        Best regards,
        Manager 
        Learning Hub
    """.format(tutor_name=res.instructor.first_name+" "+res.instructor.last_name)

    from_email = settings.EMAIL_HOST_USER  # Use the sender's email address configured in settings.py
    recipient_list = [res.instructor.user.email]  # Replace with the recipient's email address

    send_mail(subject, content, from_email, recipient_list)

    # ************************************************************

    return redirect('teach_list')


# CONTENT

@method_decorator(decs2,name="dispatch")
class AddContentView(CreateView):
    form_class=ContentModelForm
    template_name="add_content.html"
    success_url=reverse_lazy('content_list')

    def form_valid(self, form):
        messages.success(self.request,"Content uploaded successfully!!")
        return super().form_valid(form)
    

@method_decorator(decs2,name="dispatch")
class ContentListView(ListView):
    template_name="view_content.html"
    queryset=Content.objects.all()
    context_object_name="content"

    def get_queryset(self):
        return Content.objects.order_by('-datetime')


@method_decorator(decs2,name="dispatch")   
class EditContentView(View):
    def get(self,request,*args,**kwargs):
        cid=kwargs.get('id')
        res=Content.objects.get(id=cid)
        form_ob=ContentModelForm(instance=res)
        return render(request,"edit_content.html",{"form":form_ob})
    
    def post(self,request,*args,**kwargs):
        cid=kwargs.get('id')
        res=Content.objects.get(id=cid)
        form_data=ContentModelForm(data=request.POST,instance=res,files=request.FILES)
        if form_data.is_valid():
            form_data.save()
            return redirect("content_list")
        return render(request,"edit_content.html",{"form":form_data})


decs2
def delete_contentView(request,*args,**kwargs):
    vid=kwargs.get('id')
    res=Content.objects.get(id=vid)
    res.delete()
    messages.success(request,"Content deleted successfully!!")
    return redirect('content_list')


# USER CONTENT VIEW

@method_decorator(decs2,name="dispatch") 
class UserContentListView(ListView):
    template_name="user_contview.html"
    queryset=Content.objects.all()
    context_object_name="content"

    def get_queryset(self):
        return Content.objects.order_by('-datetime')


# DOCUMENT
@method_decorator(decs2,name="dispatch") 
class AddDocView(CreateView):
    form_class=DocumentModelForm
    template_name="add_doc.html"
    success_url=reverse_lazy('doc_list')

    def form_valid(self, form):
        messages.success(self.request,"Document uploaded successfully!!")
        return super().form_valid(form)


@method_decorator(decs2,name="dispatch") 
class DocListView(ListView):
    template_name="view_doc.html"
    queryset=DocumentFile.objects.all()
    context_object_name="document"


@method_decorator(decs2,name="dispatch") 
class EditDocView(View):
    def get(self,request,*args,**kwargs):
        did=kwargs.get('id')
        res=DocumentFile.objects.get(id=did)
        form_ob=DocumentModelForm(instance=res)
        return render(request,"edit_doc.html",{"form":form_ob})
    
    def post(self,request,*args,**kwargs):
        did=kwargs.get('id')
        res=DocumentFile.objects.get(id=did)
        form_data=DocumentModelForm(data=request.POST,instance=res,files=request.FILES)
        if form_data.is_valid():
            form_data.save()
            return redirect("doc_list")
        return render(request,"edit_doc.html",{"form":form_data})


decs2
def delete_docView(request,*args,**kwargs):
    did=kwargs.get('id')
    res=DocumentFile.objects.get(id=did)
    res.delete()
    messages.success(request,"Document deleted successfully!!")
    return redirect('doc_list')

# USER DOCUMENT VIEW
@method_decorator(decs2,name="dispatch") 
class UserDocListView(ListView):
    template_name="user_docview.html"
    queryset=DocumentFile.objects.all()
    context_object_name="document"


# EVENT CALENDER
@method_decorator(decs2,name="dispatch") 
class AddEventView(View):
    def get(self,request,*args,**kwargs):
        form_ob=EventModelForm()
        return render(request,"add_event.html",{"form":form_ob})
    
    def post(self,request,*args,**kwargs):
        form_data=EventModelForm(data=request.POST,files=request.FILES)
        if form_data.is_valid():
            ob=form_data.save()   
            res=CustomUser.objects.all() 
            # ********************EMAIL*******************************
            subject = ' New Event'
            content = """
            Dear LearningHub User,

           I hope this message finds you well. We are excited to announce a new event organized by Learning Hub, 
           and we would like to extend a special invitation to you to participate.

           Thank you for considering our invitation. We look forward to the possibility of having you as a featured tutor at our event
           and collaborating with you to make it a memorable and educational experience for all.

           Should you have any questions or require further information, please do not hesitate to reach out.

            

            Warm regards
            Manager 
            Learning Hub
            """.format(event_title=ob.event_title,date=ob.date)

            from_email = settings.EMAIL_HOST_USER  # Use the sender's email address configured in settings.py
            
            for i in res:          
                recipient_list = [i.email]  # Replace with the recipient's email address

                send_mail(subject, content, from_email, recipient_list)

            # ************************************************************

            return redirect("event_list")
        return render(request,"edit_event.html",{"form":form_data})
    

    
    
@method_decorator(decs2,name="dispatch") 
class EventListView(ListView):
    template_name="view_event.html"
    queryset=EventCalender.objects.all()
    context_object_name="event"

    def get_queryset(self):
        return EventCalender.objects.order_by('-date')


@method_decorator(decs2,name="dispatch") 
class EditEventView(View):
    def get(self,request,*args,**kwargs):
        eid=kwargs.get('id')
        res=EventCalender.objects.get(id=eid)
        form_ob=EventModelForm(instance=res)
        return render(request,"edit_event.html",{"form":form_ob})
    
    def post(self,request,*args,**kwargs):
        eid=kwargs.get('id')
        res=EventCalender.objects.get(id=eid)
        form_data=EventModelForm(data=request.POST,instance=res,files=request.FILES)
        if form_data.is_valid():
            form_data.save()
            return redirect("event_list")
        return render(request,"edit_event.html",{"form":form_data})


decs2   
def delete_eventView(request,*args,**kwargs):
    eid=kwargs.get('id')
    res=EventCalender.objects.get(id=eid)
    res.delete()
    messages.success(request,"Event deleted successfully!!")
    return redirect('event_list')


@method_decorator(decs2,name="dispatch") 
class UserEventListView(ListView):
    template_name="event_calender.html"
    queryset=EventCalender.objects.all()
    context_object_name="event"

    def get_queryset(self):
        return EventCalender.objects.order_by('-date')

# ASK AN EXPERT
@method_decorator(decs2,name="dispatch") 
class QaTeacherListView(ListView):
    template_name="qa_teacher_view.html"
    queryset=Teacher.objects.all()
    context_object_name="teacher"

    def get_queryset(self):
        return Teacher.objects.filter(user__is_teacher=True).exclude(user=self.request.user)
    

@method_decorator([signin_required],name="dispatch") 
class QaQuestView(View):
    def get(self,request,*args,**kwargs):
        if 'teach_id' in request.session:
            request.session.pop('teach_id',None)
        
        tid=kwargs.get('id')
        request.session['teach_id']=tid

        teach=Teacher.objects.get(id=tid)
        res=QuestAnswer.objects.filter(user=self.request.user,teacher=teach)
        res1=res.order_by('-datetime')
        return render(request,"qa_quest_view.html",{"question":res1})


@method_decorator([signin_required],name="dispatch") 
class AddQuestQaView(CreateView):
    form_class=QuestAnswerModelForm
    template_name="qa_add_quest.html"
    success_url=reverse_lazy('qa_questv')

    def post(self,request,*args,**kwargs):
        tid=kwargs.get('id')
        teach=Teacher.objects.get(id=tid)
        print(teach)
        form_data=QuestAnswerModelForm(data=request.POST)
        if form_data.is_valid():
            instance = form_data.save(commit=False)
            instance.teacher = teach  # Set the teacher for the instance
            instance.user = self.request.user
            instance.save()  
            messages.success(self.request,"New Query added...")
            return redirect("qa_teachv")
        return render(request,"qa_quest_view.html",{"form":form_data})


decs2   
def delete_questqaView(request,*args,**kwargs):
    qid=kwargs.get('id')
    res=QuestAnswer.objects.get(id=qid)
    teach=res.teacher
    res.delete()
    messages.success(request,"Query deleted..")
    res=QuestAnswer.objects.filter(user=request.user,teacher=teach)
    res1=res.order_by('-datetime')
    return render(request,"qa_quest_view.html",{"question":res1})


@method_decorator(decs3,name="dispatch")
class AnswerQaView(View):
    def get(self,request,*args,**kwargs):
        qid=kwargs.get('id')
        quest=QuestAnswer.objects.get(id=qid)
        return render(request,"qa_ans_view.html",{"form":quest})

# COURSE VALIDATION

@method_decorator(decs2,name="dispatch") 
class CourseValidateListView(ListView):
    template_name="course_validate_list.html"
    queryset=Course.objects.all()
    context_object_name="course"

    def get_queryset(self):
        return Course.objects.filter(Q(status='pending') | Q(status='accept'))

@method_decorator([signin_required],name="dispatch")   
class CourseValidateView(DetailView):
    template_name="course_validate_view.html"
    queryset=Course.objects.all()
    pk_url_kwarg="cid"
    context_object_name="course"

decs2
def reject_courseview(request,*args,**kwargs):
    cid=kwargs.get('cid')
    res=Course.objects.get(id=cid)
    res.delete()

    # ********************EMAIL*******************************
    subject = 'Course Rejection - Syllabus Update Required'
    content = """
    Dear {tutor_name},

    We appreciate your efforts and the course proposal you submitted to us. However, 
    we regret to inform you that your course has been rejected due to concerns with the syllabus content.

    

    Best regards,
    Manager 
    Learning Hub
    """.format(tutor_name=res.instructor.first_name+" "+res.instructor.last_name)

    from_email = settings.EMAIL_HOST_USER  # Use the sender's email address configured in settings.py
    recipient_list = [res.instructor.user.email]  # Replace with the recipient's email address

    send_mail(subject, content, from_email, recipient_list)

    # ************************************************************
    messages.success(request,"One course rejected...")
    return redirect('val_course_listv')

decs2
def accept_courseview(request,*args,**kwargs):
    cid=kwargs.get('cid')
    res=Course.objects.get(id=cid)
    res.status="accept"
    res.save()
         
    # ********************EMAIL*******************************
    subject = 'Course Accept - Course Content Development - Action Required'
    content = """
    Dear {tutor_name},

    I hope this message finds you well. I want to express my gratitude for your dedication and commitment to our educational platform. 
    We are excited to have you on board to create an enriching learning experience for our students.
    
    As your course "{crs_name}" has been accepted, it's time to move forward with developing the content. 
    To ensure a seamless learning journey for our students, we kindly request that you provide the following materials for each tutorial:

        *   Notes
        *   Assignments
        *   Tes Paper

    We appreciate your prompt attention to this matter, as it will allow us to provide the best possible educational experience for our students. 
    If you have any questions or need assistance with any aspect of content development, please do not hesitate to reach out to us.

    Thank you once again for being a part of our educational community. 
    We look forward to the exceptional content you will create for our students

    

    Best regards,
    Manager 
    Learning Hub
    """.format(tutor_name=res.instructor.first_name+" "+res.instructor.last_name,crs_name=res.course_name)

    from_email = settings.EMAIL_HOST_USER  # Use the sender's email address configured in settings.py
    recipient_list = [res.instructor.user.email]  # Replace with the recipient's email address

    send_mail(subject, content, from_email, recipient_list)

    # ************************************************************

    messages.success(request,"One course accepted...")
    return redirect('val_course_listv')

decs2
def on_sale_courseview(request,*args,**kwargs):
    cid=kwargs.get('cid')
    res=Course.objects.get(id=cid)
    res.status="on sale"
    res.save()

     
    # ********************EMAIL*******************************
    subject = 'Your Course Is Now Available for Purchase'
    content = """
    Dear {tutor_name},

   I hope this message finds you well. We're excited to inform you that your course, "{crs_name}," is now available for purchase on our platform. 
   Congratulations on reaching this milestone!

    As students begin to enroll in your course, it's important to create a positive and engaging learning environment. We kindly request that you:

        *   Engage with Students: Please be attentive to student inquiries and respond promptly to their messages. 
            Your interaction and guidance are essential in providing an enriching learning experience.

        *   Provide Clarifications: If students have questions or need clarification on course material, assignments, 
            or any aspect of the course, respond kindly and provide the support they need to succeed.

        *   Foster Discussion: Encourage discussions and collaboration among students. 
            A lively and interactive course environment can greatly enhance the learning process.

        *   Offer Feedback: When grading assignments or assessments, provide constructive feedback that-
            helps students improve their understanding and skills.

    Remember that your active involvement plays a significant role in ensuring the success of your course and the satisfaction of your students.

    

    Thank you for your dedication to our platform and your commitment to delivering quality education. 
    We're confident that your course will make a positive impact on our students' learning journeys.

    Should you have any questions or require any assistance, please don't hesitate to reach out to us. We're here to support you every step of the way.

    

    Best regards,
    Manager 
    Learning Hub
    """.format(tutor_name=res.instructor.first_name+" "+res.instructor.last_name,crs_name=res.course_name)

    from_email = settings.EMAIL_HOST_USER  # Use the sender's email address configured in settings.py
    recipient_list = [res.instructor.user.email]  # Replace with the recipient's email address

    send_mail(subject, content, from_email, recipient_list)

    # ************************************************************


    messages.success(request,"One course is on sale...")
    return redirect('val_course_listv')

decs2
def on_suspend_courseview(request,*args,**kwargs):
    cid=kwargs.get('cid')
    res=Course.objects.get(id=cid)
    res.status="accept"
    res.save()
         
    # ********************EMAIL*******************************
    subject = 'Course Suspend - Course Content Update - Action Required'
    content = """
    Dear {tutor_name},

    I hope this message finds you well. I wanted to reach out and inform you that, as part of our commitment to delivering high-quality education,
    we have temporarily suspended your course, "{crs_name}".

    We believe in the potential of your course, and we see great value in it. However, to ensure that our students-
    have access to the most up-to-date and relevant content, we kindly request that you review and update the course materials.

    To ensure a seamless learning journey for our students,provide the following materials for each tutorial:

        *   Notes
        *   Assignments
        *   Tes Paper

    We appreciate your prompt attention to this matter, as it will allow us to provide the best possible educational experience for our students. 
    If you have any questions or need assistance with any aspect of content development, please do not hesitate to reach out to us.

    Thank you once again for being a part of our educational community. 
    We look forward to the exceptional content you will create for our students

    

    Best regards,
    Manager 
    Learning Hub
    """.format(tutor_name=res.instructor.first_name+" "+res.instructor.last_name,crs_name=res.course_name)

    from_email = settings.EMAIL_HOST_USER  # Use the sender's email address configured in settings.py
    recipient_list = [res.instructor.user.email]  # Replace with the recipient's email address

    send_mail(subject, content, from_email, recipient_list)

    # ************************************************************


    messages.success(request,"One course is on sale...")
    return redirect('val_course_listv')

@signin_required
def wtut_courseview(request,*args,**kwargs):
    cid=kwargs.get('cid')
    res=Course.objects.get(id=cid)
    tut=Tutorial.objects.filter(course=res)
    return render(request,"tutorial_man_view.html",{"tutorial":tut})


# VALIDATED COURSE LIST 
@method_decorator(decs2,name="dispatch") 
class CourseListView(ListView):
    template_name="course_validate_list.html"
    queryset=Course.objects.all()
    context_object_name="course"

    def get_queryset(self):
        return Course.objects.filter(status='on sale')

decs2  
def delete_courseview(request,*args,**kwargs):
    cid=kwargs.get('cid')
    res=Course.objects.get(id=cid)
    res.delete()

     
    # ********************EMAIL*******************************
    subject = ' Course Removal Notification'
    content = """
    Dear {tutor_name},

    I hope this message finds you well. I wanted to reach out to you with some important information regarding your course, "{crs_name}."

    Due to certain reasons and after careful consideration, we have had to make the difficult decision to remove-
    your course from our platform. This decision was not made lightly, and we understand the dedication and effort you put-
    into creating and delivering your course.

    We would like to express our appreciation for your contributions to our educational community. 
    Your expertise and knowledge have been valuable assets, and we are grateful for the time we have worked together.

    While your course has been removed from our platform, please rest assured that this does not-
    diminish the value of your expertise or the impact you have had on our students. 
    We believe in the importance of continued learning and development, 
    and we hope that you will consider other opportunities to share your knowledge in the future.

    If you have any questions or would like to discuss this further, please feel free to reach out to us. 
    We are here to provide any assistance or clarification you may need.

    Once again, we thank you for your contributions, and we wish you all the best in your future endeavors.

    

    Sincerely,
    Manager 
    Learning Hub
    """.format(tutor_name=res.instructor.first_name+" "+res.instructor.last_name,crs_name=res.course_name)

    from_email = settings.EMAIL_HOST_USER  # Use the sender's email address configured in settings.py
    recipient_list = [res.instructor.user.email]  # Replace with the recipient's email address

    send_mail(subject, content, from_email, recipient_list)

    # ************************************************************

    messages.success(request,"One course removed...")
    return redirect('course_listv')


# USER COURSE LIST VIEW
@method_decorator(decs2,name="dispatch") 
class UserCourseListView(ListView):
    template_name="user_course_view.html"
    queryset=Course.objects.all()
    context_object_name="course"

    def get_queryset(self):
        return Course.objects.filter(status='on sale')
    


