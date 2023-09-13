from django.forms.models import BaseModelForm
from django.http import HttpResponse

from django.shortcuts import render,redirect

from django.views.generic import View,CreateView,FormView,TemplateView,ListView,DetailView

from .forms import *

from django.urls import reverse_lazy

from django.contrib import messages

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from Manager.views import signin_required,decs2

from Student.models import Room,Message



decs2
def check_teacher_reg(request,*args,**kwargs):
    try:
        teacher = Teacher.objects.get(user=request.user)
        print(teacher)
        if not teacher:
            messages.success(request,"Register first!!!")
            return redirect('reg_teach')
        elif teacher and request.user.is_teacher:
            messages.success(request,"Welcome Teacher Home")
            return redirect('teach_home')
        else:
            messages.error(request,"Once your registration is approved, you will gain access to this")
            return redirect('user_home')
    except:
        return redirect('reg_teach')



# TEACHER REGISTRATION
@method_decorator(decs2,name="dispatch")
class TeacherregView(CreateView):
    form_class=TeacherModelForm
    template_name="teacher_reg.html"
    success_url=reverse_lazy('user_home')

    def post(self,request):
        form_data=TeacherModelForm(data=request.POST,files=request.FILES)
        if form_data.is_valid():
            form_data.instance.user=request.user
            form_data.save()
            messages.success(request,"Registraion successfull!!! please wait for the approval.")
            return redirect('user_home')
        return render(request,"teacher_reg.html",{"form":form_data})

      

@method_decorator(decs2,name="dispatch")
class ProfileView(View):
    def get(self,request,*args,**kwargs):
        user=self.request.user
        teach=Teacher.objects.get(user=user)
        return render(request,"profile.html",{"data":teach})



@method_decorator(decs2,name="dispatch") 
class EditProfileView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        teach=Teacher.objects.get(id=id)
        form_ob=TeacherModelForm(instance=teach)
        return render(request,"edit_teacher.html",{"form":form_ob})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get('id')
        teach=Teacher.objects.get(id=id)
        form_data=TeacherModelForm(data=request.POST,files=request.FILES,instance=teach)
        if form_data.is_valid():
            form_data.save()
            return redirect("teach_home")
        return render(request,"edit_teacher.html",{"form":form_data})


# ASK AN EXPERT 
@method_decorator(decs2,name="dispatch")
class QaListView(ListView):
    def get(self,request,*args,**kwargs):
        teach=Teacher.objects.get(user=self.request.user)
        print(teach)
        quest=QuestAnswer.objects.filter(teacher=teach)
        print(quest)
        return render(request,"qa_teacher_quest_view.html",{"quest":quest})
    

    
@method_decorator(decs2,name="dispatch")
class QaTeacherAnswerView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        res=QuestAnswer.objects.get(id=id)
        form=QaAnswerModelForm(instance=res)
        return render(request,"qa_teacher_ans_view.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get('id')
        res=QuestAnswer.objects.get(id=id)
        form_data=QaAnswerModelForm(data=request.POST,instance=res)
        if form_data.is_valid():
            instance=form_data.save(commit=False)
            instance.is_answer=True
            instance.save()
            return redirect("qa_questv")
        return render(request,"qa_teacher_ans_view.html",{"form":form_data})
    

# COURSE
@method_decorator(decs2,name="dispatch")
class AddCourseView(CreateView):
    form_class=CourseModelForm
    template_name="add_course.html"
    success_url=reverse_lazy('teach_home')

    def post(self,request):
        form_data=CourseModelForm(data=request.POST,files=request.FILES)
        if form_data.is_valid():
            teach_ob=Teacher.objects.get(user=self.request.user)
            instance = form_data.save(commit=False)
            instance.instructor = teach_ob  # Set the teacher for the instance
            instance.status="pending"
            instance.save() 
            messages.success(request,"Course added successfully!!!")
            return redirect('teach_home')
        return render(request,"add_course.html",{"form":form_data})


@method_decorator(decs2,name="dispatch")
class CourseListView(ListView):
    def get(self,request,*args,**kwargs):
        if 'course_id' in request.session:
            self.request.session.pop('course_id',None)
        teach=Teacher.objects.get(user=self.request.user)
        crs=Course.objects.filter(instructor=teach).exclude(status='pending')
        return render(request,"teach_course_list.html",{"course":crs})
    
decs2   
def store_cid_session(request,*args,**kwargs):
    id=kwargs.get('id')
    request.session['course_id']=id
    return redirect('tc_home')

decs2
def course_home_view(request,*args,**kwargs):
    if 'tut_id' in request.session:
            request.session.pop('tut_id',None)
    cid=request.session.get('course_id')
    crs=Course.objects.get(id=cid)
    return render(request,"teach_course_home.html",{"course":crs})


# TUTORIAL
@method_decorator(decs2,name="dispatch")    
class AddTutorialView(View):
    def get(self,request,*args,**kwargs):
        if 'tut_id' in self.request.session:
            self.request.session.pop('tut_id',None)
        form_ob=TutorialForm()
        return render(request,"add_tutorial.html",{"form":form_ob})
    
    def post(self,request,*args,**kwargs):
        cid=self.request.session.get('course_id')
        crs=Course.objects.get(id=cid)
        print(crs)
        form_ob=TutorialForm(data=request.POST,files=request.FILES)
        if form_ob.is_valid():
            instance = form_ob.save(commit=False)
            instance.course=crs 
            instance.save() 
            messages.success(self.request,"uploaded...")
            return redirect('view_tut')
        return render(request,"add_tutorial.html",{"form":form_ob})
    

    
@method_decorator(decs2,name="dispatch")
class TutorialListView(View):
    def get(self,request,*args,**kwargs):
        if 'tut_id' in self.request.session:
            self.request.session.pop('tut_id',None)
        cid=request.session.get('course_id')
        crs=Course.objects.get(id=cid)
        tut=Tutorial.objects.filter(course=crs)
        return render(request,"tutorial_list.html",{"tutorial":tut})
    

decs2
def store_tutid_session(request,*args,**kwargs):
    if 'tut_id' in request.session:
        request.session.pop('tut_id',None)
    id=kwargs.get('id')
    request.session['tut_id']=id
    return redirect('tut_home')

decs2
def tutorial_home_view(request,*args,**kwargs):
    tid=request.session.get('tut_id')
    tut=Tutorial.objects.get(id=tid)
    return render(request,"teach_tut_home.html",{"tutorial":tut})


@method_decorator(decs2,name="dispatch")
class EditTutorialView(View):
    def get(self,request,*args,**kwargs):
        tid=request.session.get('tut_id')
        tutorial=Tutorial.objects.get(id=tid)
        form_ob=TutorialForm(instance=tutorial)
        return render(request,"edit_tutorial.html",{"form":form_ob})
    
    def post(self,request,*args,**kwargs):
        tid=request.session.get('tut_id')
        tutorial=Tutorial.objects.get(id=tid)
        form_data=TutorialForm(data=request.POST,files=request.FILES,instance=tutorial)
        if form_data.is_valid():
            form_data.save()
            return redirect("tut_home")
        return render(request,"edit_tutorial.html",{"form":form_data})


decs2
def delete_tutorialView(request,*args,**kwargs):
    tid=kwargs.get('id')
    tutorial=Tutorial.objects.get(id=tid)
    tutorial.delete()
    messages.success(request,"tutorial deleted successfully!!")
    return redirect('view_tut')

# ASSIGNMENT
@method_decorator(decs2,name="dispatch")
class AddAssignmentView(CreateView):
    form_class=AssignmentModelForm
    template_name="add_assignment.html"
    success_url=reverse_lazy('tut_home')

    def post(self,request,*args,**kwargs):
        tid=request.session.get('tut_id')
        tutorial=Tutorial.objects.get(id=tid)
        form_data=AssignmentModelForm(data=request.POST)
        if form_data.is_valid():
            instance = form_data.save(commit=False)
            instance.tutorial = tutorial 
            instance.save()  
            messages.success(self.request,"New assignment added...")
            return redirect("tut_home")
        return render(request,"add_assignment.html",{"form":form_data})


@method_decorator(decs2,name="dispatch")   
class AssignmentListView(ListView):
    template_name="teach_assign_list.html"
    queryset=Assignment.objects.all()
    context_object_name="assign"

    def get_queryset(self):
        tid=self.request.session.get('tut_id')
        return Assignment.objects.filter(tutorial=tid)
        
@method_decorator([signin_required],name="dispatch")
class EditAssignmentView(View):
    def get(self,request,*args,**kwargs):
        aid=kwargs.get('id')
        res=Assignment.objects.get(id=aid)
        form_ob=AssignmentModelForm(instance=res)
        return render(request,"edit_assignment.html",{"form":form_ob})
    
    def post(self,request,*args,**kwargs):
        aid=kwargs.get('id')
        res=Assignment.objects.get(id=aid)
        form_data=AssignmentModelForm(data=request.POST,instance=res)
        if form_data.is_valid():
            form_data.save()
            return redirect("t_ass_list")
        return render(request,"edit_assignment.html",{"form":form_data})
    
decs2
def delete_assignmentView(request,*args,**kwargs):
    aid=kwargs.get('id')
    res=Assignment.objects.get(id=aid)
    res.delete()
    messages.success(request,"assignment deleted successfully!!")
    return redirect('t_ass_list')


@method_decorator(decs2,name="dispatch")
class ValidateAssignmentListView(ListView):
    template_name="validate_assign.html"
    queryset=Assignment.objects.all()
    context_object_name="assign"

    def get_queryset(self):
        tid=self.request.session.get('tut_id')
        return Assignment.objects.filter(tutorial=tid)


@method_decorator([signin_required],name="dispatch")  
class StudentAssignmentView(View):
    def get(self,request,*args,**kwargs):
        aid=kwargs.get('id')
        ass=Assignment.objects.get(id=aid)
        ass_file=AssignmentFile.objects.filter(assignment=ass)
        return render(request,"validate_assign_view.html",{"assign":ass_file})


decs2
def accept_assignmentView(request,*args,**kwargs):
    aid=kwargs.get('id')
    res=AssignmentFile.objects.get(id=aid)
    res.status="Accept"
    res.save()
    messages.success(request,"assignment accepted")
    return redirect('validate_ass')


decs2
def reject_assignmentView(request,*args,**kwargs):
    aid=kwargs.get('id')
    res=AssignmentFile.objects.get(id=aid)
    res.delete()
    messages.error(request,"assignment rejected")
    return redirect('validate_ass')

   
# NOTES
@method_decorator(decs2,name="dispatch")
class AddNoteView(CreateView):
    form_class=NoteModelForm
    template_name="add_note.html"
    success_url=reverse_lazy('tut_home')

    def post(self,request,*args,**kwargs):
        tid=request.session.get('tut_id')
        tutorial=Tutorial.objects.get(id=tid)
        form_data=NoteModelForm(data=request.POST,files=request.FILES)
        if form_data.is_valid():
            instance = form_data.save(commit=False)
            instance.tutorial = tutorial 
            instance.save()  
            messages.success(self.request,"New note added...")
            return redirect("tut_home")
        return render(request,"add_note.html",{"form":form_data})
    

@method_decorator(decs2,name="dispatch")   
class NoteListView(ListView):
    template_name="teach_note_list.html"
    queryset=Note.objects.all()
    context_object_name="note"

    def get_queryset(self):
        tid=self.request.session.get('tut_id')
        return Note.objects.filter(tutorial=tid)
        

@method_decorator(signin_required,name="dispatch")
class EditNoteView(View):
    def get(self,request,*args,**kwargs):
        nid=kwargs.get('id')
        res=Note.objects.get(id=nid)
        form_ob=NoteModelForm(instance=res)
        return render(request,"edit_note.html",{"form":form_ob})
    
    def post(self,request,*args,**kwargs):
        nid=kwargs.get('id')
        res=Note.objects.get(id=nid)
        form_data=NoteModelForm(data=request.POST,instance=res)
        if form_data.is_valid():
            form_data.save()
            return redirect("t_note_list")
        return render(request,"edit_note.html",{"form":form_data})


decs2
def delete_noteView(request,*args,**kwargs):
    nid=kwargs.get('id')
    res=Note.objects.get(id=nid)
    res.delete()
    messages.success(request,"note deleted successfully!!")
    return redirect('t_note_list')


# TEST
@method_decorator(decs2,name="dispatch")
class AddTestView(View):
    def get(self,request,*args,**kwargs):
        form_data=TestModelForm()
        
        if 'test_id' in request.session:
            del request.session['test_id']

        return render(request,"add_test.html",{"form":form_data})

    def post(self,request,*args,**kwargs):
        tid=request.session.get('tut_id')
        tutorial=Tutorial.objects.get(id=tid)
        form_data=TestModelForm(data=request.POST)
        if form_data.is_valid():
            instance = form_data.save(commit=False)
            instance.tutorial = tutorial 
            instance.save()  
            
            request.session['test_id']=instance.id

            messages.success(self.request,"New test added...")
            return redirect("add_question")
        return render(request,"add_test.html",{"form":form_data})
    

@method_decorator(decs2,name="dispatch")
class AddQuestionView(View):

    def get(self,request):        
        test_id = request.session.get('test_id')
        test = Test.objects.get(id=test_id)
        no_questions = test.no_questions
        question_forms = [QuestionsModelForm(prefix=str(i)) for i in range(no_questions)]
        return render(request,"add_questions.html", {'forms': question_forms})

    def post(self, request):
        test_id = request.session.get('test_id')
        test = Test.objects.get(id=test_id)
        no_questions = test.no_questions
        question_forms = [QuestionsModelForm(request.POST, prefix=str(i)) for i in range(no_questions)]

        if all(form.is_valid() for form in question_forms):
            for form in question_forms:
                question = form.save(commit=False)
                question.test = test
                question.save()
                test.is_question=True
                test.save()
            return redirect('tut_home')
        
        return render(request, "add_questions.html", {'forms': question_forms})


@method_decorator(decs2,name="dispatch")
class TestListView(ListView):
    def get(self,request,*args,**kwargs):
        tid=self.request.session.get('tut_id')
        noq_test=Test.objects.filter(tutorial=tid,is_question=False)
        noq_test.delete()
        test=Test.objects.filter(tutorial=tid,is_question=True)
        return render(request,"teach_test_list.html",{"test":test})


@method_decorator([signin_required],name="dispatch")
class Test_QuestionView(View):
    def get(self,request,*args,**kwargs):
        if 'test_id' in request.session:
            del request.session['test_id']
        tid=kwargs.get('id')        
        request.session['test_id'] = tid

        test=Test.objects.get(id=tid)
        questions=Questions.objects.filter(test=test)
        return render(request,"view_test_question.html",{"test":test,"questions":questions})



@method_decorator([signin_required],name="dispatch")
class EditTestView(View):

    def get(self,request,*args,**kwargs):   
        test_id = request.session.get('test_id')
        test = Test.objects.get(id=test_id)
        test_form = TestForm(instance=test)
        return render(request, "edit_test.html", {'form': test_form})
    
    def post(self, request,*args,**kwargs):
        test_id = request.session.get('test_id')
        test = Test.objects.get(id=test_id)
        test_form = TestForm(request.POST, instance=test)
        if test_form.is_valid():
            test_form.save()
            # messages.success(request,"edited")
            return redirect('edit_test')
        
        return render(request, "edit_test.html", {'form': test_form})
        

@method_decorator(decs2,name="dispatch")
class EditQuestionsView(View):

    def get(self, request):
        test_id = request.session.get('test_id')
        test = Test.objects.get(id=test_id)
        questions=Questions.objects.filter(test=test)
        question_forms = [QuestionsModelForm(instance=question, prefix=str(i)) for i, question in enumerate(questions)]
        
        # question_forms = [QuestionsModelForm(prefix=str(i)) for i in range(no_of_questions)]
        return render(request, "edit_questions.html", {'forms': question_forms})
    
    def post(self, request):
        test_id = request.session.get('test_id')
        test = Test.objects.get(id=test_id)
        questions=Questions.objects.filter(test=test)
        question_forms = [QuestionsModelForm(request.POST, instance=question, prefix=str(i)) for i, question in enumerate(questions)]
        # question_forms = [QuestionsModelForm(request.POST, prefix=str(i)) for i in range(no_of_questions)]

        if all(form.is_valid() for form in question_forms):
            for form in question_forms:
                question = form.save(commit=False)
                question.test = test
                question.save()
            return redirect('tut_home')

        return render(request, "edit_questions.html", {'forms': question_forms})
    

decs2
def dlt_testquest_view(request,*args,**kwargs):
    test_id=kwargs.get('id')
    test=Test.objects.get(id=test_id)
    Questions.objects.filter(test=test).delete()
    test.delete()
    return redirect('t_test_list')


@method_decorator(decs2,name="dispatch")
class CheckTestListView(ListView):
    template_name="check_test_list.html"
    queryset=Test.objects.all()
    context_object_name="test"

    def get_queryset(self):
        tid=self.request.session.get('tut_id')
        return Test.objects.filter(tutorial=tid)


@method_decorator([signin_required],name="dispatch")
class CheckTestMarkView(View):
    def get(self,request,*args,**kwargs):
        tid=kwargs.get('id')
        test=Test.objects.get(id=tid)
        test_mark=TestMark.objects.filter(test=test)
        return render(request,"check_test_mark.html",{"test_mark":test_mark})
    



# CHATBOX
@method_decorator(decs2,name="dispatch")
class RoomListView(View):
    def get(self,request,*args,**kwargs):
        teach=Teacher.objects.get(user=self.request.user)
        rooms = Room.objects.filter(teacher=teach)
        return render(request, 'teach_rooms.html', {'rooms': rooms})


@method_decorator([signin_required],name="dispatch")   
class RoomView(View):
    def get(self,request,*args,**kwargs):
        slug=kwargs.get('slug')
        room = Room.objects.get(slug=slug)
        messages = Message.objects.filter(room=room)[0:25]

        return render(request, 'teach_room.html', {'room': room, 'messages': messages})