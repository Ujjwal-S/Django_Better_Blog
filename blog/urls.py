from django.urls import path
from . import views


urlpatterns = [
	
	path('toggleBookmark/', views.toggleBookmark, name='toggleBookmark'),
	path('blog-create/', views.BlogCreateView.as_view(), name='blog-create'),
	path('blog-update/<str:slug>/', views.BlogUpdateView.as_view(), name='blog-update'),
	path('deleteComment/<int:pk>/', views.DeleteComment.as_view(), name='deleteComment'),
	path('<str:slug>', views.BlogDetail.as_view(), name='blog-detail'),
	path('delete-blog/<str:slug>', views.BlogDeleteView.as_view(), name='blog-delete'),
	path('doAction/', views.action, name='action'),
	path('upload_image/', views.upload_image),


	path('', views.BlogList.as_view(), name='blog-list'),
]
