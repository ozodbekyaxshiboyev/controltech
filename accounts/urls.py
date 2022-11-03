from django.urls import path,include
from .views import user_register_view


urlpatterns = [
    # path('login/', login_view, name='login'),
    path('signup/', user_register_view, name='signup'),

]
