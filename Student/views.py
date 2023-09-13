from django.shortcuts import render

from django.shortcuts import render,redirect

from django.views.generic import View,CreateView,FormView,TemplateView,ListView,DetailView

from .forms import *
from Manager.models import *

from django.urls import reverse_lazy

from django.contrib import messages

from django.contrib.auth import login,authenticate


from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


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
def studreg_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_student:
            messages.success(request,"Welcome Student Home!!")
            return fn(request,*args,**kwargs)
        else:            
            return redirect('reg_stud')
    return inner



decs2=[never_cache,signin_required]
# Create your views here.



# TEACHER REGISTRATION
@method_decorator(decs2,name="dispatch")
class StudentregView(CreateView):
    form_class=StudentModelForm
    template_name="stud_reg.html"
    success_url=reverse_lazy('user_home')

    def post(self,request,*args,**kwargs):
        form_data=StudentModelForm(data=request.POST,files=request.FILES)
        if form_data.is_valid():
            form_data.instance.user=self.request.user
            ob=CustomUser.objects.get(id=self.request.user.id)
            ob.is_student=True
            ob.save()
            form_data.save()
            messages.success(request,"Registraion successfull!!!")
            return redirect('stud_home')
        return render(request,"stud_reg.html",{"form":form_data})


@method_decorator(decs2,name="dispatch")
class StudProfileView(View):
    def get(self,request,*args,**kwargs):
        user=self.request.user
        stud=Student.objects.get(user=user)
        return render(request,"stud_profile.html",{"data":stud})


@method_decorator(decs2,name="dispatch")   
class StudEditProfileView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        stud=Student.objects.get(id=id)
        form_ob=StudentModelForm(instance=stud)
        return render(request,"edit_student.html",{"form":form_ob})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get('id')
        stud=Student.objects.get(id=id)
        form_data=StudentModelForm(data=request.POST,files=request.FILES,instance=stud)
        if form_data.is_valid():
            form_data.save()
            return redirect("stud_home")
        return render(request,"edit_student.html",{"form":form_data})



# COURSE PURCHASE
@method_decorator(decs2,name="dispatch")
class CourseListView(ListView):
    template_name="course_list.html"
    queryset=Course.objects.all()
    context_object_name="course"

    def get_queryset(self):
        return Course.objects.filter(status='on sale')


@method_decorator(decs2,name="dispatch")
class CourseView(DetailView):
    template_name="course_view.html"
    queryset=Course.objects.all()
    pk_url_kwarg="cid"
    context_object_name="data"

@method_decorator([signin_required],name="dispatch")
class PurchaseCourseView(View):
    def get(self,request,*args,**kwargs):
        cid=kwargs.get('cid')
        crs=Course.objects.get(id=cid)
        # stud=Student.objects.get(user=self.request.user)
        print(crs)
        month=crs.duration * 30
        current_date = datetime.now().date()        
        # Calculate the date 6 months from now
        end_date = current_date + timedelta(days=month)
        messages.success(self.request,"Course is added to cart. Please confirm the purchase...")
        print(current_date)
        return render(request,"purchase_view.html",{"data":crs,"cdate":current_date,"edate":end_date})


from django.utils.text import slugify
@signin_required
def create_room_if_not_exists(request,student, teacher ,end_date):
    # Check if a room already exists for this student-teacher pair
    existing_room = Room.objects.filter(student=student, teacher=teacher).first()
    if existing_room:
        if existing_room.date_of_end <= end_date:
            existing_room.date_of_end=end_date
            existing_room.save()

    if not existing_room:
        # Create a new room if it doesn't exist
        room_name = f"{request.user.username} - {teacher.first_name}"
        room_slug = slugify(room_name)

        new_room = Room.objects.create(
            student=student,
            teacher=teacher,
            name=room_name,
            slug=room_slug,
            date_of_end=end_date
        )
        return new_room
    else:
        return existing_room


@signin_required
def pay_purchase_view(request,*args,**kwargs):
    cid=kwargs.get('id')
    crs=Course.objects.get(id=cid)
    stud=Student.objects.get(user=request.user)
    teach=Teacher.objects.get(id=crs.instructor.id)

    month=crs.duration * 30
    current_date = datetime.now().date()        
    # Calculate the date 6 months from now
    end_date = current_date + timedelta(days=month)

    crs_buy=CoursePurchase.objects.filter(student=stud,course=crs)
    if crs_buy:
        for i in crs_buy:
            if i.date_of_end >= current_date:
                messages.error(request,"You are already purchased the course..")
                return redirect("bcourse_list")

    room = create_room_if_not_exists(request,stud, teach,end_date)
    CoursePurchase.objects.create(student=stud,course=crs,date_of_end=end_date,is_paid=True)
    messages.success(request,"purchase successfull..")
    return redirect('course_list')


@method_decorator(decs2,name="dispatch")
class BoughtCourseListView(ListView):
    template_name="bought_course_list.html"
    queryset=CoursePurchase.objects.all()
    context_object_name="course"

    def get_queryset(self):
        stud=Student.objects.get(user=self.request.user)        
        current_date = datetime.now().date()  
        return CoursePurchase.objects.filter(is_paid=True,student=stud,date_of_end__gte=current_date)


# TUTORIAL
@method_decorator(decs2,name="dispatch")
class CourseTutorialListView(View):
    def get(self,request,*args,**kwargs):
        if 'course_id' in request.session:
            del request.session['course_id']
        cid=kwargs.get('id')
        request.session['course_id']=cid
        crs=Course.objects.get(id=cid)
        tut=Tutorial.objects.filter(course=crs)
        return render(request,"course_tut_list.html",{"tutorial":tut,"crs":crs})
    
    
@signin_required
def stud_store_tutid_session(request,*args,**kwargs):
    if 'tut_id' in request.session:
            del request.session['tut_id']
    id=kwargs.get('id')
    request.session['tut_id']=id
    return redirect('stud_tut_home')


@signin_required
def stud_tutorial_home_view(request,*args,**kwargs):
    tid=request.session.get('tut_id')
    tut=Tutorial.objects.get(id=tid)
    return render(request,"stud_tut_home.html",{"tutorial":tut})


# NOTES
@method_decorator(decs2,name="dispatch")
class StudNoteListView(ListView):
    template_name="stud_note_list.html"
    queryset=Note.objects.all()
    context_object_name="note"

    def get_queryset(self):
        tid=self.request.session.get('tut_id')
        return Note.objects.filter(tutorial=tid)


# ASSIGNMENT
@method_decorator(decs2,name="dispatch")
class StudAssignmentListView(ListView):
    template_name="stud_assign_list.html"
    queryset=Assignment.objects.all()
    context_object_name="assign"

    def get_queryset(self):
        tid=self.request.session.get('tut_id')
        return Assignment.objects.filter(tutorial=tid)



@method_decorator([signin_required],name="dispatch")
class AddAssignmentFileView(View):

    def get(self,request,*args,**kwargs): 
        if 'ass_id' in self.request.session:
            del self.request.session['ass_id']

        ass_id=kwargs.get('id')        
        self.request.session['ass_id'] =ass_id
        ass = Assignment.objects.get(id=ass_id)

        stud_id=self.request.session.get('stud_id')
        stud=Student.objects.get(id=stud_id)

        ass_file=AssignmentFile.objects.filter(assignment=ass,student=stud).first()
        form_ob=AssignmentFileForm()        
        return render(request,"add_assign_file.html", {"form":form_ob,"assignment":ass,"ass_file":ass_file})
    

    def post(self,request,*args,**kwargs):
        form_ob=AssignmentFileForm(data=request.POST,files=request.FILES)

        stud_id=self.request.session.get('stud_id')
        stud=Student.objects.get(id=stud_id)
        ass_id=self.request.session.get('ass_id')
        ass=Assignment.objects.get(id=ass_id)
        ass_file=AssignmentFile.objects.filter(assignment=ass,student=stud).first()

        if form_ob.is_valid():
        # If an AssignmentFile already exists, update it with the form_ob data
            if ass_file:
                form_ob = AssignmentFileForm(request.POST, request.FILES, instance=ass_file)                
                form_ob.instance.status = "Submitted"
            # Otherwise, create a new AssignmentFile instance
            else:
                form_ob.instance.student = stud
                form_ob.instance.assignment = ass
                form_ob.instance.status = "Submitted"

            if form_ob.is_valid():
                form_ob.save()
                return redirect('stud_assign_list')

        return render(request,"add_assign_file.html",{"form":form_ob,"assignment":ass,"ass_file":ass_file})


# TEST
@method_decorator(decs2,name="dispatch")
class StudTestListView(ListView):
    template_name="stud_test_list.html"
    queryset=Test.objects.all()
    context_object_name="test"

    def get_queryset(self):
        tid=self.request.session.get('tut_id')
        return Test.objects.filter(tutorial=tid)
    

@method_decorator(decs2,name="dispatch")
class AttendTestView(View):

    def get(self,request,*args,**kwargs): 
        test_id=kwargs.get('id')        
        self.request.session['test_id'] =test_id
        test = Test.objects.get(id=test_id)
        questions = Questions.objects.filter(test=test)

        formset = []
        for question in questions:
            form = TestAnswerForm(prefix=str(question.id))
            formset.append((question, form))

        stud_id=self.request.session.get('stud_id')
        stud=Student.objects.get(id=stud_id)
        test_mark=TestMark.objects.filter(test=test,student=stud).first()

        return render(request, "attend_testpaper.html", {'questions': formset,"test_mark":test_mark})

       
    def post(self,request,*args,**kwargs):
        test_id = self.request.session.get('test_id')
        test = Test.objects.get(id=test_id)

        stud_id = self.request.session.get('stud_id')
        stud = Student.objects.get(id=stud_id)

        test_mark = TestMark.objects.filter(test=test, student=stud).first()
        
        questions = Questions.objects.filter(test=test)

        answers = {}
        mark=0
        for question in questions:
            form = TestAnswerForm(request.POST, prefix=str(question.id))
            if form.is_valid():
                answers[question.id] = form.cleaned_data['answer']
                print(answers[question.id])

                if question.answer == answers[question.id]:
                    mark+=1
            else:
                formset = []
                for question in questions:
                    form = TestAnswerForm(prefix=str(question.id))
                    formset.append((question, form))
                return render(request,"attend_testpaper.html", {"questions":formset,"questions":questions,"test_mark":test_mark})
            
        TestMark.objects.create(student=stud,test=test,mark=mark,status="attended")
        return redirect("stud_test_list")
            


# CHATBOX
@method_decorator(decs2,name="dispatch")
class RoomListView(View):
    def get(self,request,*args,**kwargs):
        current_date=datetime.now().date()  
        stud=Student.objects.get(user=self.request.user)
        rooms = Room.objects.filter(student=stud,date_of_end__gte=current_date)
        return render(request, 'stud_rooms.html', {'rooms': rooms})
    

@method_decorator([signin_required],name="dispatch")
class RoomView(View):
    def get(self,request,*args,**kwargs):
        slug=kwargs.get('slug')
        room = Room.objects.get(slug=slug)
        messages = Message.objects.filter(room=room)[0:25]

        return render(request, 'stud_room.html', {'room': room, 'messages': messages})
            
        
    