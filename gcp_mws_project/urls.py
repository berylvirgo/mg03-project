from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from education.forms import LoginForm, CustomPasswordResetForm
from education.views import CustomLoginView, SignUpView, ProfileUpdateView, ProfileView, DashboardView, HomeView, sendEmail

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('send-email', sendEmail, name="send_email"),

    path('education/', include("education.urls")),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # # Authentication 
    path('register/', SignUpView.as_view(), name="register"),

    path('login/', CustomLoginView.as_view(
        authentication_form=LoginForm,
        ),
        name='login'
    ),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
        ),
        name='logout'
    ),

    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='change-password.html',
            success_url='/'
        ),
        name='change-password'
    ),
    
    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='forgot-password.html',
             subject_template_name='password-reset/password_reset_subject.txt',
             email_template_name='password-reset/password_reset_email.html',
             form_class=CustomPasswordResetForm
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('oauth/', include('social_django.urls', namespace='social')),  # <-- here
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'education.views.error_404'
# handler500 = 'education.views.error_500'
# handler403 = 'education.views.error_403'
# handler400 = 'education.views.error_400'
