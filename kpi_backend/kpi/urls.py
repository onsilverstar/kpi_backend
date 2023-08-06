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
    path("seachbykpi", views.SearchKPIMeasureByKPI.as_view()),
    path("editkpi", views.EDITKPI.as_view()),
    path("edituser", views.EditUser.as_view()),
    path("editkpimeasure", views.EDITKPIMeasure.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
