from datetime import timezone
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView,ListView,CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView,UpdateView
from .models import Report, ReportItem, Task, TaskResult, Chat
from accounts.models import User
from accounts.enums import UserRoles
from .models import Reachment
from .forms import ReportForm




class AboutView(TemplateView):
    template_name = 'about.html'

class HomePageView(ListView):
    template_name = 'home.html'
    queryset = Report.objects.all()
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        students = User.objects.filter(role=UserRoles.student.value)
        reachments = Reachment.objects.filter(user__role=UserRoles.student.value)
        context['students'] = students
        context['reachments'] = reachments
        return context


class StudentView(DetailView):
    template_name = 'student.html'
    context_object_name = 'context'
    pk_url_kwarg = 'student_pk'



    def get_context_data(self, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)
        student_pk = self.kwargs["student_pk"]
        student = User.objects.get(pk=student_pk)
        reports = Report.objects.filter(user=student)
        task = Task.objects.filter(user=student).last()
        context['student'] = student
        context['reachments'] = reports
        context['task'] = task
        return context

    def get_object(self, queryset=None):
        return self.request.user


class StudentEditView(UpdateView):
    template_name = 'student_profile.html'
    context_object_name = 'student'
    fields = ('username','first_name','last_name','age','bio','image')
    pk_url_kwarg = 'student_pk'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        student = self.get_object()
        return reverse_lazy("student", kwargs={"student_pk": student.pk})


class StudentReportListCreate(ListView, UpdateView):
    template_name = 'student_report.html'
    queryset = Report.objects.all()
    fields = ['book','from_lesson','to_lesson','count','comment']
    context_object_name = 'reports'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        # context = super(StudentReportListCreate, self).get_context_data(**kwargs)
        context = dict()
        student = self.get_object()
        reports = Report.objects.filter(user=student)
        context['student'] = student
        context['reports'] = reports
        return context


def studentReportListCreate(request,student_pk):
    if request.method == "GET":
        form = ReportForm()
        student = User.objects.get(pk=student_pk)
        reports = Report.objects.filter(user=student)
        context = dict()
        context['student'] = student
        context['reports'] = reports
        context['form'] = form
        return render(request, template_name='student_report.html', context=context)
    else:
        report_form = ReportForm(data=request.POST)
        if report_form.is_valid():
            report_form.save(commit=False)
            report = report_form.instance
            report.user = request.user
            report.save()
            return redirect('student_report',student_pk=request.user.pk)
        else:
            return render(request, template_name='student_report.html', context={'form': report_form})

    # pk_url_kwarg = 'task_pk'
    #
    #
    #     def get_success_url(self):
    #         pk = self.kwargs["pk"]
    #         lesson_pk = self.kwargs["lesson_pk"]
    #         task_pk = self.kwargs["task_pk"]
    #         return reverse_lazy("taskdetail", kwargs={"pk": pk,'lesson_pk':lesson_pk,'task_pk':task_pk})


# class RoleView(ListView):
#     template_name = 'role.html'
#     context_object_name = 'course_assestant'
#
#     def get_queryset(self):
#         course_assestant = None
#         if self.request.user.is_superuser:
#             print("superuser")
#             print(course_assestant)
#             return {'course_assestant': course_assestant}
#         else:
#             customuser = CustomUser.objects.get(user=self.request.user)
#             course_assestant = customuser.course_assestant.all()
#             print("else...")
#             print(course_assestant)
#             return {'course_assestant':course_assestant}
#
#
#
#
#
#
# class CourseDetail(ListView):
#     template_name = 'course_detail.html'
#     context_object_name = 'lessons'
#     # queryset = Course.objetcs.all()
#
#     def get_queryset(self):
#         data = dict()
#         lessons = Lesson.objects.filter(course__pk=self.kwargs['pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         data['lessons']=lessons
#         data['course']=course
#         return {'lessons':lessons,'course':course}
#
#     def get_context_data(self, **kwargs):
#         context = super(CourseDetail, self).get_context_data(**kwargs)
#         lessons = Lesson.objects.filter(course__pk=self.kwargs['pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         context['lessons'] = lessons
#         context['course'] = course
#
#         return context
#
#
# class MentorView(ListView):
#     template_name = 'mentor.html'
#     queryset = Course.objects.all()
#     context_object_name = 'courses'
#
#     # def get_queryset(self):
#     #     data = dict()
#     #     print("1111")
#     #     courses = Course.objects.all()
#     #     customusers = CustomUser.objects.all()
#     #     data['courses'] = courses
#     #     data['customusers'] = customusers
#     #     return {'courses':courses, 'customusers': customusers}
#     #
#     # def get_context_data(self, **kwargs):
#     #     print("222222")
#     #     context = super(MentorView, self).get_context_data(**kwargs)
#     #     courses = Course.objects.all()
#     #     customusers = CustomUser.objects.all()
#     #     context['courses'] = courses
#     #     context['customusers'] = customusers
#     #
#     #     return context
#
# def set_assestant(request,pk):
#     customuser = CustomUser.objects.get(pk=request.GET.get('u_pk'))
#     course = Course.objects.get(pk=pk)
#     if customuser:
#         customuser.course_assestant.add(course)
#
#     return redirect(f'/mentor/{pk}/courselessons/')
#
#
# def noset_assestant(request,pk,u_pk):
#     customuser = CustomUser.objects.get(pk=u_pk)
#     course = Course.objects.get(pk=pk)
#     customuser.course_assestant.remove(course)
#
#     return redirect(f'/mentor/{pk}/courselessons/')
#
#
#
# class CourseCreateView(CreateView):
#     model = Course
#     template_name = 'mentor_course_create.html'
#     fields = ('name', 'description', 'duration',)
#     success_url = reverse_lazy("mentor")
#
#
# class CourseLessonView(ListView):
#     template_name = 'mentor_course_lessons.html'
#     context_object_name = 'lessons'
#
#
#     def get_queryset(self):
#         data = dict()
#         lessons = Lesson.objects.filter(course__pk=self.kwargs['pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         customusers = CustomUser.objects.all()
#         # print(customusers)
#         assestants = CustomUser.objects.filter(course_assestant=course)  #todo bu manytomanyfieldni ichida bor degan so`rov takomillashtirish kerak
#         data['lessons'] = lessons
#         data['course'] = course
#         data['customusers'] = customusers
#         data['assestants'] = assestants
#         return {'lessons': lessons, 'course': course,'customusers':customusers,'assestants':assestants}
#
#     def get_context_data(self, **kwargs):
#         context = super(CourseLessonView, self).get_context_data(**kwargs)
#         lessons = Lesson.objects.filter(course__pk=self.kwargs['pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         customusers = CustomUser.objects.all()
#         assestants = CustomUser.objects.filter(course_assestant=course)
#         # print(assestants)
#         context['lessons'] = lessons
#         context['course'] = course
#         context['customusers'] = customusers
#         context['assestants'] = assestants
#
#         return context
#
#
# class CourseDeleteView(DeleteView):
#     model = Course
#     template_name = 'mentor_course_delete.html'
#     success_url = reverse_lazy('mentor')
#
#
# class LessonCreateView(CreateView):
#     model = Lesson
#     template_name = 'mentor_lesson_create.html'
#     fields = ('name', 'source_file', 'video_file','others')
#     # success_url = reverse_lazy("lessons")  bu holatda pk aniqlanmay qolyapti urldagi
#
#     def form_valid(self, form):
#         form.instance.course = Course.objects.get(id=self.kwargs.get('pk'))
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         pk = self.kwargs["pk"]
#         return reverse_lazy("lessons", kwargs={"pk": pk})
#
#
#
# class LessonTaskView(ListView):
#     model = Lesson
#     template_name = 'mentor_lesson_tasks.html'
#     context_object_name = 'tasks'
#
#
#     def get_queryset(self):
#         data = dict()
#         print("1111")
#         tasks = Task.objects.filter(lesson__pk=self.kwargs['lesson_pk'])
#         lesson = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         data['tasks'] = tasks
#         data['lesson'] = lesson
#         data['course'] = course
#         return {'tasks':tasks,'lessons': lesson, 'course': course}
#
#     def get_context_data(self, **kwargs):
#         print("222222")
#         context = super(LessonTaskView, self).get_context_data(**kwargs)
#         tasks = Task.objects.filter(lesson__pk=self.kwargs['lesson_pk'])
#         lesson = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         context['tasks'] = tasks
#         context['lesson'] = lesson
#         context['course'] = course
#
#         return context
#
#
# class LessonDeleteView(DeleteView):
#     model = Lesson
#     template_name = 'mentor_lesson_delete.html'
#     pk_url_kwarg = 'lesson_pk'  #agar buni aniqlab qo`ymasa uchiradigan objectni id sini pk deb oladi default holatda
#
#
#     def get_success_url(self):
#         print("get_successga keldi")
#         pk = self.kwargs["pk"]
#         return reverse_lazy("lessons", kwargs={"pk": pk})
#
#
# class TaskCreateView(CreateView):
#     model = Task
#     template_name = 'mentor_task_create.html'
#     fields = ('number', 'description', 'image')
#
#     # success_url = reverse_lazy("lessons")  bu holatda pk aniqlanmay qolyapti urldagi
#
#     def form_valid(self, form):
#         form.instance.lesson = Lesson.objects.get(pk=self.kwargs.get('lesson_pk'))
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         pk = self.kwargs["pk"]
#         lesson_pk = self.kwargs["lesson_pk"]
#         return reverse_lazy("tasks", kwargs={"pk": pk,'lesson_pk':lesson_pk})
#
# class TaskDetailView(DetailView):
#     model = Task
#     template_name = 'mentor_task_detail.html'
#     context_object_name = 'task'
#     pk_url_kwarg = 'task_pk'   #detailview shu task_pk bo`yicha ko`rsatadi
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['now'] = timezone.now()
#     #     return context
#
#     def get_context_data(self, **kwargs):
#         print("222222")
#         context = super(TaskDetailView, self).get_context_data(**kwargs)
#         task = Task.objects.get(pk=self.kwargs['task_pk'])
#         lesson = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         context['task'] = task
#         context['lesson'] = lesson
#         context['course'] = course
#
#         return context
#
#
# class TaskDeleteView(DeleteView):
#     model = Task
#     template_name = 'mentor_task_delete.html'
#     pk_url_kwarg = 'task_pk'  # agar buni aniqlab qo`ymasa uchiradigan objectni id sini pk deb oladi default holatda
#
#     def get_success_url(self):
#         pk = self.kwargs["pk"]
#         lesson_pk = self.kwargs["lesson_pk"]
#         return reverse_lazy("tasks", kwargs={"pk": pk,'lesson_pk':lesson_pk})
#
#
# class TaskUpdateView(UpdateView):
#     model = Task
#     fields = ['number','description','image']
#     template_name = 'mentor_task_update.html'
#     pk_url_kwarg = 'task_pk'
#
#
#     def get_success_url(self):
#         pk = self.kwargs["pk"]
#         lesson_pk = self.kwargs["lesson_pk"]
#         task_pk = self.kwargs["task_pk"]
#         return reverse_lazy("taskdetail", kwargs={"pk": pk,'lesson_pk':lesson_pk,'task_pk':task_pk})
#
#     def get_context_data(self, **kwargs):
#         print("222222")
#         context = super(TaskUpdateView, self).get_context_data(**kwargs)
#         task = Task.objects.get(pk=self.kwargs['task_pk'])
#         lesson = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         context['task'] = task
#         context['lesson'] = lesson
#         context['course'] = course
#
#         return context
#
#
# def registercourse(request,pk):
#     user = request.user
#     customuser = CustomUser.objects.filter(user=user).first()
#     if customuser:
#         course = Course.objects.get(pk=pk)
#         customuser.course.add(course)
#     return redirect('home')
#
#
# class StudentView(ListView):
#     template_name = 'student.html'
#     context_object_name = 'courses'
#     # model = Course
#
#     def get_queryset(self):
#         user = self.request.user
#         courses=None
#         customuser = CustomUser.objects.filter(user=user).first()    #filter bilan olsa query qaytaradi get bilan olsa obyekt qayataradi
#         if customuser:
#             print(customuser)
#             courses = customuser.course.all()
#         return courses
#
#     # def get_queryset(self):
#     #     qs = super().get_queryset()
#     #     return qs.filter(course__id__in=self.kwargs['name'])
#
#
#
# class StudentCourseLessonView(ListView):
#     template_name = 'student_course_lessons.html'
#     context_object_name = 'lessons'
#
#     def get_queryset(self):
#         data = dict()
#         lessons = Lesson.objects.filter(course__pk=self.kwargs['pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         data['lessons'] = lessons
#         data['course'] = course
#         return {'lessons': lessons, 'course': course}
#
#     def get_context_data(self, **kwargs):
#         context = super(StudentCourseLessonView, self).get_context_data(**kwargs)
#         lessons = Lesson.objects.filter(course__pk=self.kwargs['pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         context['lessons'] = lessons
#         context['course'] = course
#
#         return context
#
#
# class StudentLessonTaskView(ListView):
#     model = Lesson
#     template_name = 'student_lesson_tasks.html'
#     context_object_name = 'tasks'
#
#
#     def get_queryset(self):
#         data = dict()
#         print("1111")
#         tasks = Task.objects.filter(lesson__pk=self.kwargs['lesson_pk'])
#         lesson = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         data['tasks'] = tasks
#         data['lesson'] = lesson
#         data['course'] = course
#         return {'tasks':tasks,'lessons': lesson, 'course': course}
#
#     def get_context_data(self, **kwargs):
#         print("222222")
#         context = super(StudentLessonTaskView, self).get_context_data(**kwargs)
#         tasks = Task.objects.filter(lesson__pk=self.kwargs['lesson_pk'])
#         lesson = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         context['tasks'] = tasks
#         context['lesson'] = lesson
#         context['course'] = course
#
#         return context
#
#
# class StudentTaskDetailView(CreateView):
#
#     model = Task
#     template_name = 'student_task_detail.html'
#     context_object_name = 'task'
#     pk_url_kwarg = 'task_pk'
#
#     form_class = TextTaskForm
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['now'] = timezone.now()
#     #     return context
#
#     def get_context_data(self, **kwargs):
#         print("222222")
#         context = super(StudentTaskDetailView, self).get_context_data(**kwargs)
#         user = self.request.user
#         customuser = CustomUser.objects.get(user=user)
#         task = Task.objects.get(pk=self.kwargs.get('task_pk'))
#
#         texttasks = TextTask.objects.filter(user=customuser, task=task).all()
#         task = Task.objects.get(pk=self.kwargs['task_pk'])
#         lesson = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         context['texttasks'] = texttasks
#         context['task'] = task
#         context['lesson'] = lesson
#         context['course'] = course
#
#         return context
#
#     def form_valid(self, form):
#         form.instance.user = CustomUser.objects.get(user=self.request.user)
#         form.instance.task = Task.objects.get(pk=self.kwargs.get('task_pk'))
#         form.instance.is_user = True
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         pk = self.kwargs["pk"]
#         lesson_pk = self.kwargs["lesson_pk"]
#         task_pk = self.kwargs["task_pk"]
#         return reverse_lazy("studenttaskdetail", kwargs={"pk": pk,'lesson_pk':lesson_pk,'task_pk':task_pk})
#
#
# #================================================================
# #================================================================
#
# class AssistantView(ListView):
#     template_name = 'assestant.html'
#     context_object_name = 'course_assestant'
#     # model = Course
#
#     def get_queryset(self):
#         user = self.request.user
#         courses=None
#         customuser = CustomUser.objects.filter(user=user).first()
#         if customuser:
#             print(customuser)
#             courses = customuser.course_assestant.all()
#         return courses
#
#
# class AssistantStudentView(ListView):
#     template_name = 'assestant_course_student.html'
#     context_object_name = 'students'
#
#
#     def get_queryset(self):
#         context = dict()
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         students = CustomUser.objects.filter(course=course)
#         context['students'] = students
#         context['course'] = course
#         return {'students': students, 'course': course}
#
#
#     def get_context_data(self, **kwargs):
#         print("222222")
#         context = super(AssistantStudentView, self).get_context_data(**kwargs)
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         students = CustomUser.objects.filter(course=course)
#
#         context['students'] = students
#         context['course'] = course
#
#         return context
#
#
# class AssistantStudentLessonView(ListView):
#     template_name = 'assestant_course_lessons.html'
#     context_object_name = 'lessons'
#
#     def get_queryset(self):
#         data = dict()
#         lessons = Lesson.objects.filter(course__pk=self.kwargs['pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         student = CustomUser.objects.get(pk=self.kwargs.get('student_pk'))
#         data['lessons'] = lessons
#         data['course'] = course
#         data['student'] = student
#         return {'lessons': lessons, 'course': course,'student':student}
#
#     def get_context_data(self, **kwargs):
#         context = super(AssistantStudentLessonView, self).get_context_data(**kwargs)
#         lessons = Lesson.objects.filter(course__pk=self.kwargs['pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         student = CustomUser.objects.get(pk=self.kwargs.get('student_pk'))
#         context['lessons'] = lessons
#         context['course'] = course
#         context['student'] = student
#
#         return context
#
#
# class AssistantStudentTaskView(ListView):
#     model = Task
#     template_name = 'assestant_lesson_tasks.html'
#     context_object_name = 'tasks'
#
#     def get_queryset(self):
#         data = dict()
#         print("1111")
#         tasks = Task.objects.filter(lesson__pk=self.kwargs['lesson_pk'])
#         lesson = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         student = CustomUser.objects.get(pk=self.kwargs.get('student_pk'))
#         data['tasks'] = tasks
#         data['lesson'] = lesson
#         data['course'] = course
#         data['student'] = student
#         return {'tasks': tasks, 'lessons': lesson, 'course': course,'student':student}
#
#     def get_context_data(self, **kwargs):
#         print("222222")
#         context = super(AssistantStudentTaskView, self).get_context_data(**kwargs)
#         tasks = Task.objects.filter(lesson__pk=self.kwargs['lesson_pk'])
#         lesson = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         student = CustomUser.objects.get(pk=self.kwargs.get('student_pk'))
#         context['tasks'] = tasks
#         context['lesson'] = lesson
#         context['course'] = course
#         context['student'] = student
#         return context
#
#
# class AssistantTaskDetailView(CreateView):
#     model = Task
#     template_name = 'assestant_task_detail.html'
#     context_object_name = 'task'
#     pk_url_kwarg = 'task_pk'
#
#     form_class = TextTaskForm
#
#
#     def get_context_data(self, **kwargs):
#         print("222222")
#         context = super(AssistantTaskDetailView, self).get_context_data(**kwargs)
#         customuser = CustomUser.objects.get(pk=self.kwargs.get('student_pk'))
#         task = Task.objects.get(pk=self.kwargs.get('task_pk'))
#
#         texttasks = TextTask.objects.filter(user=customuser, task=task).all()
#         task = Task.objects.get(pk=self.kwargs['task_pk'])
#         lesson = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
#         course = Course.objects.get(pk=self.kwargs['pk'])
#         student = CustomUser.objects.get(pk=self.kwargs.get('student_pk'))
#         context['texttasks'] = texttasks
#         context['task'] = task
#         context['lesson'] = lesson
#         context['course'] = course
#         context['student'] = student
#
#         return context
#
#     def form_valid(self, form):
#         form.instance.user = CustomUser.objects.get(pk=self.kwargs.get('student_pk'))
#         form.instance.task = Task.objects.get(pk=self.kwargs.get('task_pk'))
#         form.instance.is_user = False
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         pk = self.kwargs["pk"]
#         lesson_pk = self.kwargs["lesson_pk"]
#         task_pk = self.kwargs["task_pk"]
#         student_pk = self.kwargs.get('student_pk')
#         return reverse_lazy("assistanttaskdetail", kwargs={"pk": pk, 'student_pk':student_pk,'lesson_pk': lesson_pk, 'task_pk': task_pk})