from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('split/pdf',views.PdfView.as_view()),
    path('pdf/list',views.PdfList.as_view()),
    path('change/password',views.ChangePassword.as_view()),
    path('create/account',views.CreateAccount.as_view()),
    path('manage/user',views.ManageUser.as_view()),
    path('login',views.LoginView.as_view()),
    path('dashboard',views.DashboardView.as_view()),
    path('logout',views.LogoutView.as_view()),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    