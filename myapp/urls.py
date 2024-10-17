
from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('login/',views.login),
    path('logout/',views.logout),
    path('login_post/',views.login_post),
    path('adminhome/',views.adminhome),
    path('viewacceptorreject/',views.viewacceptorreject),
    path('accept_post/',views.accept_post),
    path('approve_owner/<id>',views.approve_owner),
    path('rejected/', views.rejected),
    path('rejected_post/', views.rejected_post),
    path('rejected_owner/<id>', views.rejected_owner),
    path('change_pswd/',views.change_pswd),
    path('change_pswd_post/',views.change_pswd_post),
    path('Manage_owner/',views.Manage_owner),
    path('Manage_owner_post/',views.Manage_owner_post),
    path('payment_report/',views.payment_report),
    path('payment_report_post/',views.payment_report_post),
    path('reply_cm/<id>',views.reply_cm),
    path('reply_post/',views.reply_post),
    path('review_rating/',views.review_rating),
    path('review_rating_post/',views.review_rating_post),
    path('view_complaint/',views.view_complaint),
    path('view_complaint_post/',views.view_complaint_post),
    path('view_house/<id>',views.view_house),
    path('view_house_post/',views.view_house_post),
    path('view_house_user/',views.view_house_user),

    #house owner

    path('ownerhome/', views.ownerhome),
    path('add_house/',views.add_house),
    path('owner_pswd/', views.owner_pswd),
    path('owner_pswd_post/',views.owner_pswd_post),
    path('add_house_post/',views.add_house_post),
    path('edit_house/<id>',views.edit_house),
    path('edit_house_post/',views.edit_house_post),
    path('delete_house/<id>',views.delete_house),
    path('edit_profile/<id>',views.edit_profile),
    path('edit_profile_post/',views.edit_profile_post),
    path('owner_signup/',views.owner_signup),
    path('owner_signup_post/',views.owner_signup_post),
    path('owner_rating/',views.owner_rating),
    path('owner_rating_post/',views.owner_rating_post),
    path('send_complaint/',views.send_complaint),
    path('send_complaint_post/',views.send_complaint_post),
    path('ownerview_house/',views.ownerview_house),
    path('ownerview_house_post/',views.ownerview_house_post),
    path('view_payment/',views.view_payment),
    path('view_payment_post/',views.view_payment_post),
    path('view_profile/',views.view_profile),
    # path('view_profile_post/',views.view_profile_post),
    path('view_reply/', views.view_reply),
    path('view_reply_post/', views.view_reply_post),
    path('view_request/',views.view_request),
    path('view_request_post/', views.view_request_post),
    path('accept_user<id>/',views.accept_user),
    path('reject_user<id>/',views.reject_user),
    path('view_accepted_user/',views.view_accepted_user),
    path('view_accepted_user_post/',views.view_accepted_user_post),
    path('signup/',views.signup),
    #user

    path('userhome/', views.userhome),
    path('user_pswd/', views.user_pswd),
    path('user_pswd_post/', views.user_pswd_post),
    path('edit_userprofile/', views.edit_userprofile),
    path('edit_userprofile_post/', views.edit_userprofile_post),
    path('user_report/', views.user_report),
    path('user_report_post/', views.user_report_post),
    path('search_house/', views.search_house),
    path('search_house_post/', views.search_house_post),
    path('user_complaint/', views.user_complaint),
    path('user_complaint_post/', views.user_complaint_post),
    path('send_review/', views.send_review),
    path('send_review_post/', views.send_review_post),
    path('user_signup/', views.user_signup),
    path('user_signup_post/', views.user_signup_post),
    path('user_reply/', views.user_reply),
    path('user_reply_post/', views.user_reply_post),
    path('view_request_status/', views.view_request_status),
    path('view_request_status_post/', views.view_request_status_post),
    path('view_userprofile/', views.view_userprofile),
    #path('view_userprofile_post/', views.view_userprofile_post),
    path('user_request/',views.user_request),
    path('user_request_post/',views.user_request_post),
    path('payment/<id>/<aid>',views.payment),










]
