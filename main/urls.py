from django.urls import path
from . import views


app_name = 'main'


urlpatterns = [
   path('', views.HomeView.as_view(), name='home'),
   path("signup/", views.SignUpAjaxView.as_view(), name="signup_ajax"),
   path("login/", views.LoginAjaxView.as_view(), name="login_ajax"),
   path("collections/create/", views.CreateCollectionAjaxView.as_view(), name="create_collection"),
   path("collections/<int:collection_id>/delete/", views.DeleteCollectionAjaxView.as_view(), name="delete_collection"),
]
