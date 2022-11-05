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
    RoleView
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
    path('manager/<int:manager_pk>/report/<int:report_pk>/', studentReportdetailview, name='student_report_detail'),
    path('manager/<int:manager_pk>/report/<int:report_pk>/confirm/', reportdeleteview, name='manager_report_confirm'),
    path('manager/<int:manager_pk>/report/<int:report_pk>/delete/', reportdeleteview, name='report_delete'),

    # path('role/', RoleView.as_view(),name='role'),
    #
    # path('register/<int:pk>/',registercourse,name='register'),
    #
    # path('mentor/', MentorView.as_view(),name='mentor'),
    # path('mentor/coursecreate/', CourseCreateView.as_view(),name='coursecreate'),
    # path('mentor/<int:pk>/courselessons/', CourseLessonView.as_view(),name='lessons'),
    # path('mentor/<int:pk>/courselessons/set/', set_assestant,name='set'),
    # path('mentor/<int:pk>/courselessons/noset/<int:u_pk>/', noset_assestant,name='noset'),
    # path('mentor/<int:pk>/coursedelete/', CourseDeleteView.as_view(),name='coursedelete'),
    # path('mentor/<int:pk>/lessoncreate/', LessonCreateView.as_view(),name='lessoncreate'),
    # path('mentor/<int:pk>/<int:lesson_pk>/', LessonTaskView.as_view(),name='tasks'),
    # path('mentor/<int:pk>/<int:lesson_pk>/lessondelete/', LessonDeleteView.as_view(),name='lessondelete'),
    # path('mentor/<int:pk>/<int:lesson_pk>/taskcreate/', TaskCreateView.as_view(),name='taskcreate'),
    # path('mentor/<int:pk>/<int:lesson_pk>/<int:task_pk>/', TaskDetailView.as_view(),name='taskdetail'),
    # path('mentor/<int:pk>/<int:lesson_pk>/<int:task_pk>/delete', TaskDeleteView.as_view(),name='taskdelete'),
    # path('mentor/<int:pk>/<int:lesson_pk>/<int:task_pk>/update', TaskUpdateView.as_view(),name='taskupdate'),
    #
    #
    # # path('login/', login_view, name='login'),
    # path('activate-email/', email_activate, name='activate-email'),
    # path('signup/', user_register_view, name='signup'),
    #
    # path('student/',StudentView.as_view(),name='student'),
    # path('student/<int:pk>/courselessons/', StudentCourseLessonView.as_view(),name='studentlessons'),
    # path('student/<int:pk>/<int:lesson_pk>/', StudentLessonTaskView.as_view(),name='studenttasks'),
    # path('student/<int:pk>/<int:lesson_pk>/<int:task_pk>/', StudentTaskDetailView.as_view(),name='studenttaskdetail'),
    #
    # path('assistant/',AssistantView.as_view(),name='assistant'),
    # path('assistant/<int:pk>/students/',AssistantStudentView.as_view(),name='assistantstudent'),
    # path('assistant/<int:pk>/<int:student_pk>/',AssistantStudentLessonView.as_view(),name='assistantstudentlesson'),
    # path('assistant/<int:pk>/<int:student_pk>/<int:lesson_pk>/',AssistantStudentTaskView.as_view(),name='assistantstudenttask'),
    # path('assistant/<int:pk>/<int:student_pk>/<int:lesson_pk>/<int:task_pk>/',AssistantTaskDetailView.as_view(),name='assistanttaskdetail'),

]
