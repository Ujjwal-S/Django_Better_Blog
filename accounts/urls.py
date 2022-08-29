from django.urls import path, include
from . import views


urlpatterns = [
	path('ua-string/', views.ua_string, name='ua-string'),

	path('bookmarks/', views.Bookmarks.as_view(), name='bookmarks'),
	path('settings/', views.UpdateProfile.as_view(), name='settings'),		# update_profile
	path('signup/', views.SignUpView.as_view(), name='signup'),
	path('emailVerification/<uidb64>/<token>', views.activate, name='activate'),
	path('security/', views.Security.as_view(), name='security'),
	path('my-blogs/', views.MyBlogs.as_view(), name='my-blogs'),
	path('login/', views.NewLoginView.as_view(redirect_authenticated_user=True), name='login'),
	path('logout-session/<int:pk>/', views.logout_session, name='logout-session'),
	path('', include('django.contrib.auth.urls')),
]

