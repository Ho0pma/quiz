from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView
from . import views


app_name = 'main'


urlpatterns = [
   path('', views.HomeView.as_view(), name='home'),
   path("signup/", views.SignUpAjaxView.as_view(), name="signup_ajax"),
   path("login/", views.LoginAjaxView.as_view(), name="login_ajax"),
   path("forgot-password/", views.ForgotPasswordView.as_view(), name="forgot_password"),
   path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(
       template_name='main/password_reset_confirm.html',
       success_url=reverse_lazy('main:home'),
   ), name="password_reset_confirm"),
   path("profile/update/", views.UpdateProfileAjaxView.as_view(), name="update_profile"),
   path("profile/change-password/", views.ChangePasswordAjaxView.as_view(), name="change_password"),
   path("collections/create/", views.CreateCollectionAjaxView.as_view(), name="create_collection"),
   path("collections/<int:collection_id>/update/", views.UpdateCollectionAjaxView.as_view(), name="update_collection"),
   path("collections/<int:collection_id>/delete/", views.DeleteCollectionAjaxView.as_view(), name="delete_collection"),
   path("collections/<int:collection_id>/cards/create/", views.CreateCardAjaxView.as_view(), name="create_card"),
   path("cards/<int:card_id>/update/", views.UpdateCardAjaxView.as_view(), name="update_card"),
   path("cards/<int:card_id>/delete/", views.DeleteCardAjaxView.as_view(), name="delete_card"),
]
