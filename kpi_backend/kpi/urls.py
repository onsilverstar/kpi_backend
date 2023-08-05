from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #path("", views.Index.as_view()),
    path("createuser", views.CreateUserAPI.as_view()),
    path("login", views.LoginView.as_view()),
    path("logout", views.LogoutView.as_view()),
    # path("createpayment", views.CreatePayment.as_view()),
    # path("currentuser", views.CurrentUserView.as_view()),
    # path("createorder", views.CreateOrder.as_view()),
    # path("checkpayment", views.CheckPayment.as_view()),
    # path("search", views.Search.as_view())
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
