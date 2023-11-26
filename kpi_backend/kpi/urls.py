from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.Users.as_view()),
    path("createuser", views.CreateUserAPI.as_view()),
    path("login", views.LoginView.as_view()),
    path("logout", views.LogoutView.as_view()),
    path("kpimetrics", views.KPIMetric.as_view()),
    path("kpimeasures", views.KPIMeasure.as_view()),
    path("searchbykpi", views.SearchKPIMeasureByKPI.as_view()),
    path("editkpi", views.EDITKPI.as_view()),
    path("edituser", views.EditUser.as_view()),
    path("editkpimeasure", views.EDITKPIMeasure.as_view()),
    path("kpidashboard", views.KPIDashboard.as_view()),
    path("kpiupdatemeasure", views.KPIMeasureUpdate.as_view()),
    path("searchkpi", views.SearchKPI.as_view()),
    path("searchuser", views.SearchUser.as_view()),
    path("createkpimeasuretodate", views.CreateKPIMeasuretoDate.as_view()),
    path("searchkpimeasure", views.SearchKPIMeasure.as_view()),
    path("authuser", views.AuthenticateUser.as_view()),
    path("validateedit", views.ValidateEditPermision.as_view()),
    path("addusertokpi", views.AddUserToKPI.as_view()),
    path("createkpi", views.CreateKPIAPI.as_view()),
    path("department", views.Department.as_view()),
    path("kpibydepartment", views.KPIbyDepartment.as_view()),
    path("createdep", views.CreateDepAPI.as_view()),











]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
