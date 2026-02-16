from django.urls import path
from . import views

urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.sign_up, name="signup"),
    path("email_sent/", views.email_sent_page, name="email_sent"),
    
    # User Management
    
    path("", views.management, name='user_management'),
    path("new_user/", views.new_user_page, name='new_user'),
    path("update_user/<int:id>", views.update_user_page, name='update_user'),
    path("view_all/", views.view_all, name='view_all'),
    path("verify/<str:username>/<str:token>/", views.verify_email, name='verify_email'),
    path("forgot_password/", views.forgot_pass, name='forgot_password'),
    path("forgot_password/<int:uid>/<str:token>/", views.reset_password, name='forgot_password_confirm'),
    path("forgot_password/sent/", views.email_sent_forgot, name='email_sent_forgot'),
    path("reach_us/", views.reach_us, name='reach'),
    path("profile/", views.profile, name='profile'),
    path("change_password/", views.change_password, name='change_password'),
    path("terms/", views.terms_conditions, name='terms'),
]
