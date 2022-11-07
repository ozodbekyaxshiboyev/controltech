from django.urls import path,include
from .views import (
    AboutView,
    HomePageView,
    StudentView,
    StudentEditView,

    studentReportListCreate,
    studentDayplanListCreate,
    student_tasks,
    studentReachmentListCreate,
    taskresultview,
    chat,
    studentReportdetailview,
    reportdeleteview,
    chatdelete,
    ManagerView,
    ManagerEditView,
    RoleView,
    Managerreportview,
    managerreportconfirm,
    managerreportdelete,
    mentorReachmentListCreate,
    mentortaskListCreate,
    mentortaskresultview,
    mentorReportList,
    simpleReportList,
    simpleReportDetail
)


urlpatterns = [
    path('', HomePageView.as_view(),name='home'),
    path('about/', AboutView.as_view(),name='about'),

    path('role/', RoleView.as_view(), name='role'),

    path('student/<int:student_pk>/', StudentView.as_view(), name='student'),
    path('student-profile/<int:student_pk>/', StudentEditView.as_view(), name='student_profile'),
    path('student/<int:student_pk>/reports/', studentReportListCreate, name='student_report'),
    path('student/<int:student_pk>/reports/<int:report_pk>/', studentReportdetailview, name='student_report_detail'),
    path('student/<int:student_pk>/reports/<int:report_pk>/delete/', reportdeleteview,name='report_delete'),

    path('student/<int:student_pk>/dayplans/', studentDayplanListCreate, name='student_dayplan'),
    path('student/<int:student_pk>/tasks/', student_tasks, name='student_task'),
    path('student/<int:student_pk>/reachments/', studentReachmentListCreate, name='student_reachment'),
    path('student/<int:student_pk>/taskansver/<int:task_pk>/', taskresultview, name='task_answer'),
    path('student/<int:person_pk>/chat/', chat, name='student_chat'),
    path('student/<int:person_pk>/chat/<int:chat_pk>/', chatdelete, name='chat_delete'),

    path('manager/<int:manager_pk>/', ManagerView.as_view(), name='manager'),
    path('manager-profile/<int:manager_pk>/', ManagerEditView.as_view(), name='manager_profile'),
    path('manager/<int:manager_pk>/report/<int:report_pk>/', Managerreportview, name='manager_report_detail'),
    path('manager/<int:manager_pk>/report/<int:report_pk>/confirm/', managerreportconfirm, name='manager_report_confirm'),
    path('manager/<int:manager_pk>/report/<int:report_pk>/delete/', managerreportdelete, name='manager_report_delete'),
    path('manager/<int:person_pk>/chat/', chat, name='manager_chat'),
    path('manager/<int:manager_pk>/reachment/', mentorReachmentListCreate, name='manager_reachment'),
    path('manager/<int:manager_pk>/task/', mentortaskListCreate, name='manager_task'),
    path('manager/<int:manager_pk>/taskansver/<int:task_pk>/', mentortaskresultview, name='manager_task_result'),
    path('manager/<int:manager_pk>/student/<int:student_pk>/report/', mentorReportList, name='manager_student_report'),

    path('simple/<int:student_pk>/report/', simpleReportList, name='simple_student_report'),
    path('simple/<int:student_pk>/report/<int:report_pk>/', simpleReportDetail, name='simple_report_detail'),


]