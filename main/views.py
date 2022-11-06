import math
from datetime import timezone
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView,ListView,CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView,UpdateView
from .models import Report, ReportItem, Task, TaskResult, Chat, Dayplan
from accounts.models import User
from accounts.enums import UserRoles
from .models import Reachment
from .forms import ReportForm, DayplanForm, ReachmentForm, TaskResultForm, ChatForm, MentorReachmentForm, \
    TaskmanagerForm
from django.db.models import Q, Sum

from .services import translate


class AboutView(TemplateView):
    template_name = 'about.html'

class HomePageView(ListView):
    template_name = 'home.html'
    queryset = Report.objects.all()
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        students = User.objects.filter(role=UserRoles.student.value)
        reachments = Reachment.objects.filter(user__role=UserRoles.student.value).order_by('-pk')
        users = User.objects.filter(role=UserRoles.student.value).annotate(count=Sum('report__count'))
        # users = User.objects.filter(role=UserRoles.student.value)
        # for i in users:
        #     count = Report.objects.filter(user=i).aggregate(Sum('count')).get('count__sum')
        #     i.count=count
        context['students'] = students
        context['reachments'] = reachments
        context['users'] = users
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
        task_has = TaskResult.objects.filter(user=student).values('task_id')
        tasks = Task.objects.filter(Q(user=student) | Q(for_all_students=True))
        tasks = tasks.exclude(pk__in=task_has)
        dayplan = Dayplan.objects.filter(user=student).last()
        context['student'] = student
        context['reachments'] = reports
        context['tasks'] = tasks
        context['dayplan'] = dayplan
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



def studentReportListCreate(request,student_pk):
    if request.user.pk is None or request.user.pk != student_pk:
        return redirect('home')
    if request.method == "GET":
        form = ReportForm()
        student = User.objects.get(pk=student_pk)
        reports = Report.objects.filter(user=student,is_verifyed=True).order_by('-pk')
        unreports = Report.objects.filter(user=student,is_verifyed=False).order_by('-pk')
        context = dict()
        context['student'] = student
        context['reports'] = reports
        context['unreports'] = unreports
        context['form'] = form
        return render(request, template_name='student_report.html', context=context)
    else:
        report_form = ReportForm(data=request.POST)
        if report_form.is_valid():
            report_form.save(commit=False)
            report = report_form.instance
            report.user = request.user
            report.save()
            """
            This is translation block
            """
            report = Report.objects.last()
            print(report.words)
            new = report.words.split(sep=',')
            print(new)
            words = report.words.replace("\n"," ")
            words = report.words.replace("\r"," ")
            words = [i.strip().lower() for i in words.split(sep=',')]
            print(words)
            print(len(words))
            all_word = len(words)
            count = 0
            for word in words:
                translation = translate(word)
                similar = ReportItem.objects.filter(word=word)
                if similar:
                    count += 1
                ReportItem.objects.create(user=report.user, report=report, word=word, word_translation=translation)
            similarity = (count / all_word) * 100
            report.count = all_word
            report.similarity = math.floor(similarity)
            report.save()
            # Translation block end
            return redirect('student_report',student_pk=request.user.pk)
        else:
            return render(request, template_name='student_report.html', context={'form': report_form})

def studentDayplanListCreate(request, student_pk):
    if request.user.pk is None or request.user.pk != student_pk:
        return redirect('home')
    if request.method == "GET":
        form = DayplanForm()
        student = User.objects.get(pk=student_pk)
        dayplans = Dayplan.objects.filter(user=student).order_by('-pk')
        context = dict()
        context['student'] = student
        context['dayplans'] = dayplans
        context['form'] = form
        return render(request, template_name='student_dayplan.html', context=context)
    else:
        dayplan_form = DayplanForm(data=request.POST)
        if dayplan_form.is_valid():
            dayplan_form.save(commit=False)
            report = dayplan_form.instance
            report.user = request.user
            report.save()
            return redirect('student_dayplan', student_pk=request.user.pk)
        else:
            return render(request, template_name='student_dayplan.html', context={'form': dayplan_form})


def student_tasks(request,student_pk):
    if request.user.pk is None or request.user.pk != student_pk:
        return redirect('home')
    if request.method == "GET":
        context = dict()
        student = User.objects.get(pk=student_pk)
        tasks = Task.objects.filter(Q(user=student) | Q(for_all_students=True)).order_by('-pk')
        context['student'] = student
        context['tasks'] = tasks
        return render(request, template_name='student_task.html', context=context)


def studentReachmentListCreate(request, student_pk):
    if request.user.pk is None or request.user.pk != student_pk:
        return redirect('home')
    if request.method == "GET":
        form = ReachmentForm()
        student = User.objects.get(pk=student_pk)
        reachments = Reachment.objects.filter(user=student).order_by('-pk')
        context = dict()
        context['student'] = student
        context['reachments'] = reachments
        context['form'] = form
        return render(request, template_name='student_reachment.html', context=context)
    else:
        reachment_form = ReachmentForm(data=request.POST)
        if reachment_form.is_valid():
            reachment_form.save(commit=False)
            report = reachment_form.instance
            report.user = request.user
            report.save()
            return redirect('student_reachment', student_pk=request.user.pk)
        else:
            return render(request, template_name='student_reachment.html', context={'form': reachment_form})


def taskresultview(request,student_pk, task_pk):
    if request.user.pk is None or request.user.pk != student_pk:
        return redirect('home')
    if request.method == "GET":
        form = TaskResultForm()
        student = User.objects.get(pk=student_pk)
        taskresults = TaskResult.objects.filter(task__pk=task_pk,user=student).all()
        print(taskresults)
        context = dict()
        context['student'] = student
        context['task_pk'] = task_pk
        context['taskresults'] = taskresults
        context['form'] = form
        return render(request, template_name='task_result.html', context=context)
    else:
        data=request.POST
        print(data)
        text = data.get('text')
        task_pk = data.get('task_pk')
        if text and task_pk:
            TaskResult.objects.create(task=Task.objects.get(pk=task_pk),user=request.user,text=text)
        return redirect('student', student_pk=request.user.pk)


def chat(request,person_pk):
    if request.user.pk is None or request.user.pk != person_pk:
        return redirect('home')
    if request.method == "GET":
        form = ChatForm()
        person = User.objects.get(pk=person_pk)
        chats = Chat.objects.all()[:30]
        context = dict()
        context['chats'] = chats
        context['person'] = person
        context['form'] = form
        return render(request, template_name='chat.html', context=context)
    else:
        chat_form = ChatForm(data=request.POST)
        if chat_form.is_valid():
            chat_form.save(commit=False)
            chat = chat_form.instance
            chat.user = request.user
            chat.save()
            if request.user.role == 'student':
                return redirect('student_chat',person_pk=request.user.pk)
            elif request.user.role == 'manager':
                return redirect('manager_chat', person_pk=request.user.pk)
            else:
                return
        else:
            return render(request, template_name='chat.html', context={'form': chat_form})


def studentReportdetailview(request,student_pk, report_pk):
    if request.user.pk is None or request.user.pk != student_pk:
        return redirect('home')
    if request.method == "GET":
        student = User.objects.get(pk=student_pk)
        report = Report.objects.get(pk=report_pk)
        reportitems = ReportItem.objects.filter(report=report,user=student).all()
        context = dict()
        context['student'] = student
        context['report'] = report
        context['reportitems'] = reportitems
        return render(request, template_name='student_report_detail.html', context=context)

def reportdeleteview(request,student_pk, report_pk):
    if request.user.pk is None or request.user.pk != student_pk:
        return redirect('home')
    student = User.objects.get(pk=student_pk)
    report = Report.objects.get(pk=report_pk)
    report.delete()
    return redirect("student_report", student_pk=student.pk)  #bu boshqa viewni ishlatadi  shuning uchun ma`lumot junatish shart emas

def chatdelete(request, person_pk, chat_pk):
    if request.user.pk is None or request.user.pk != person_pk:
        return redirect('home')
    user = User.objects.get(pk=person_pk)
    chat = Chat.objects.get(pk=chat_pk)
    chat.delete()
    if request.user.role == 'student':
        return redirect("student_chat", person_pk=user.pk)
    elif request.user.role == 'manager':
        return redirect('manager_chat', person_pk=user.pk)
    else:
        return

    # def get_success_url(self):
    #     student = self.get_object()
    #     return reverse_lazy("student", kwargs={"student_pk": student.pk})  bu klas modeli bor uchun chuniki qayta ma`lumot junatish kerak


class RoleView(ListView):
    template_name = 'role.html'
    context_object_name = 'user'

    def get_queryset(self):
        return self.request.user


class ManagerView(DetailView):
    template_name = 'manager.html'
    context_object_name = 'context'
    pk_url_kwarg = 'manager_pk'

    def get_context_data(self, **kwargs):
        context = super(ManagerView, self).get_context_data(**kwargs)
        manager_pk = self.kwargs["manager_pk"]
        manager = User.objects.get(pk=manager_pk)
        reports = Report.objects.filter(is_verifyed=False)
        students = User.objects.filter(role=UserRoles.student.value)
        context['manager'] = manager
        context['reports'] = reports
        context['students'] = students
        return context

    def get_object(self, queryset=None):
        return self.request.user


class ManagerEditView(UpdateView):
    template_name = 'manager_profile.html'
    context_object_name = 'manager'
    fields = ('username','first_name','last_name','age','bio','image')
    pk_url_kwarg = 'manager_pk'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        manager = self.get_object()
        return reverse_lazy("manager", kwargs={"manager_pk": manager.pk})


def Managerreportview(request, manager_pk, report_pk):
    if request.user.pk is None or request.user.pk != manager_pk:
        return redirect('home')
    if request.method == "GET":
        manager = User.objects.get(pk=manager_pk)
        report = Report.objects.get(pk=report_pk)
        reportitems = ReportItem.objects.filter(report=report).all()
        context = dict()
        context['manager'] = manager
        context['report'] = report
        context['reportitems'] = reportitems
        return render(request, template_name='manager_report_detail.html', context=context)


def managerreportconfirm(request,manager_pk, report_pk):
    if request.user.pk is None or request.user.pk != manager_pk:
        return redirect('home')
    manager = User.objects.get(pk=manager_pk)
    report = Report.objects.get(pk=report_pk)
    report.is_verifyed = True
    report.save()
    return redirect("manager", manager_pk=manager.pk)


def managerreportdelete(request,manager_pk, report_pk):
    if request.user.pk is None or request.user.pk != manager_pk:
        return redirect('home')
    manager = User.objects.get(pk=manager_pk)
    report = Report.objects.get(pk=report_pk)
    report.delete()
    return redirect("manager", manager_pk=manager.pk)


def mentorReachmentListCreate(request, manager_pk):
    if request.user.pk is None or request.user.pk != manager_pk:
        return redirect('home')
    if request.method == "GET":
        form = MentorReachmentForm()
        manager = User.objects.get(pk=manager_pk)
        reachments = Reachment.objects.all().order_by('-pk')
        context = dict()
        context['manager'] = manager
        context['reachments'] = reachments
        context['form'] = form
        return render(request, template_name='manager_reachment.html', context=context)
    else:
        reachment_form = MentorReachmentForm(data=request.POST)
        if reachment_form.is_valid():
            reachment_form.save()
            return redirect('manager_reachment', manager_pk=request.user.pk)
        else:
            return render(request, template_name='manager_reachment.html', context={'form': reachment_form})


def mentortaskListCreate(request, manager_pk):
    if request.user.pk is None or request.user.pk != manager_pk:
        return redirect('home')
    if request.method == "GET":
        form = TaskmanagerForm()
        manager = User.objects.get(pk=manager_pk)
        tasks = Task.objects.filter(creator=manager).order_by('-pk')
        context = dict()
        context['manager'] = manager
        context['tasks'] = tasks
        context['form'] = form
        return render(request, template_name='manager_tasks.html', context=context)
    else:
        print(1111)
        task_form = TaskmanagerForm(data=request.POST)
        if task_form.is_valid():
            task_form.save(commit=False)
            task = task_form.instance
            print(request.user)
            task.creator = request.user
            task.save()
            print(task)
            return redirect('manager_task', manager_pk=request.user.pk)
        else:
            return render(request, template_name='manager_tasks.html', context={'form': task_form})


def mentortaskresultview(request,manager_pk, task_pk):
    if request.user.pk is None or request.user.pk != manager_pk:
        return redirect('home')
    if request.method == "GET":
        manager = User.objects.get(pk=manager_pk)
        taskresults = TaskResult.objects.filter(task__pk=task_pk).all()
        context = dict()
        context['manager'] = manager
        context['taskresults'] = taskresults
        return render(request, template_name='manager_task_result.html', context=context)



def mentorReportList(request,manager_pk, student_pk):
    if request.user.pk is None or request.user.pk != manager_pk:
        return redirect('home')
    if request.method == "GET":
        manager = User.objects.get(pk=manager_pk)
        student = User.objects.get(pk=student_pk)
        reports = Report.objects.filter(user__id=student_pk, is_verifyed=True).order_by('-pk')
        unreports = Report.objects.filter(user__id=student_pk, is_verifyed=False).order_by('-pk')
        context = dict()
        context['student'] = student
        context['manager'] = manager
        context['reports'] = reports
        context['unreports'] = unreports
        return render(request, template_name='manager_student_report.html', context=context)
