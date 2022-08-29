from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse

from .models import Blog, Tag, Comment, Bookmark, Opinion, Tag
from .forms import *
from django.http import Http404

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import model_to_dict

from datetime import datetime, timezone
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.conf import settings
from django.http import JsonResponse
import os


def my_login_required(function):
	def wrapper(request, *args, **kw):
		user=request.user  
		if not (user.id):
			return HttpResponse(json.dumps({'response': 'ERROR'}))
		else:
			return function(request, *args, **kw)
	return wrapper

class BlogCreateView(LoginRequiredMixin, CreateView):
	model = Blog
	template_name = 'blog/blog-form.html'
	form_class = BlogCreateForm
	success_url = '/accounts/my-blogs/'

	def form_valid(self, form):
		print(form.cleaned_data['test_category'], '*'*10)
		
		self.object = form.save(commit=False)
		self.object.author = self.request.user
		self.object.save()

		categories = form.cleaned_data['test_category']
		categories = categories.split()
		for category in categories:
			c, _ = Tag.objects.get_or_create(name=category)
			self.object.tags.add(c)	
		
		return HttpResponseRedirect(self.get_success_url())


class BlogUpdateView(LoginRequiredMixin, UpdateView):
	model = Blog
	template_name = 'blog/blog-update.html'
	form_class = BlogCreateForm
	success_url = '/accounts/my-blogs/'

	def get_object(self, queryset=None):
		obj = super(BlogUpdateView, self).get_object(queryset=queryset)
		if obj.author != self.request.user:
			raise Http404()
		return obj


class BlogDeleteView(LoginRequiredMixin, DeleteView):
	model = Blog
	success_url = '/accounts/my-blogs/'
	template_name = 'blog/blog_confirm_delete.html'

	def get_object(self, queryset=None):
		obj = super(BlogDeleteView, self).get_object(queryset=queryset)
		if obj.author != self.request.user:
			raise Http404()
		return obj


class BlogList(ListView):
	model = Blog
	template_name = 'blog/blog-list.html'
	context_object_name = 'blogs'
	paginate_by = 3
	queryset = Blog.objects.filter(status=1)


class BlogDetail(FormMixin, DetailView):
	model = Blog
	template_name = 'blog/blog-detail.html'
	slug_url_kwarg = 'slug'
	queryset = Blog.objects.filter(status=1)
	form_class = CommentForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['blog'].n_views += 1
		context['blog'].save()
		
		context['comment_form'] = CommentForm()
		context['bookmarked'] = True if self.request.user.is_authenticated and Bookmark.objects.filter(user=self.request.user, blog=context['blog']) else False
		context['comments'] = Comment.objects.filter(blog=context['blog'], parent=None)
		return context

	def post(self, *args, **kwargs):
		# form = self.get_context_data(**kwargs)['comment_form']
		form = CommentForm(self.request.POST)
		if form.is_valid():
			print("in form valid().")
			parent_obj = None
			try:
				parent_id = int(self.request.POST.get('parent_id'))
				print('parent_id = ', parent_id)
			except:
				parent_id = None
			if parent_id:
				parent_obj = Comment.objects.get(id=parent_id)

			commenter = self.request.user
			body = form.cleaned_data['body']
			blog = self.get_object()

			if parent_obj:
				Comment(commenter=commenter, body=body, blog=blog, parent=parent_obj).save()
			else:
				Comment(commenter=commenter, body=body, blog=blog).save()
			return HttpResponseRedirect(reverse('blog-detail', kwargs={'slug': self.get_object().slug}))


class DeleteComment(LoginRequiredMixin, DeleteView):
	model = Comment

	def get(self, *args, **kwargs):
		return self.post(*args, **kwargs)

	def get_success_url(self):
		print('*'*30)
		return reverse('blog-detail', kwargs={"slug": self.get_object().blog.slug})



@csrf_exempt
@my_login_required
def toggleBookmark(request):
	data = json.loads(request.body)
	try:
		slug = data['slug']
		blog = get_object_or_404(Blog, slug=slug)

		if Bookmark.objects.filter(user=request.user, blog=blog) .exists():
			print('it exists. and now deleting.')
			Bookmark.objects.get(user=request.user, blog=blog).delete()
			status = False

		else:
			print("Does not exist creating now.")
			bookmark = Bookmark.objects.create(user=request.user, blog=blog)
			bookmark.save()
			status = True

		response = json.dumps({'response': 'OK', 'status': status})

	except Exception as e:
		response = json.dumps({'response': 'ERROR'})

	return HttpResponse(response)


@login_required
@csrf_exempt
def action(request):
	data = json.loads(request.body)
	try:
		commentId = data['commentId']
		action = data['action']
		print(commentId, action)

		comment = get_object_or_404(Comment, id=commentId)

		op, _ = Opinion.objects.get_or_create(user=request.user, comment=comment)

		if action == "LIKE": status = 1
		if action == "DISLIKE": status = -1

		if status == op.action:
			op.delete()
			status = 0
		else: 
			op.action = status
			op.save()

		response = json.dumps({'response': 'OK', 'like': status==1, 'dislike': status==-1, 'nlikes': comment.n_likes()})

	except:
		response = json.dumps({'response': 'ERROR'})

	return HttpResponse(response)


@login_required
@csrf_exempt
def upload_image(request):
	if request.method == "POST":
		file_obj = request.FILES['file']
		file_name_suffix = file_obj.name.split(".")[-1]
		if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
			return JsonResponse({"message": "Wrong file format"})

		path = os.path.join(
			settings.MEDIA_ROOT,
			'tinymce',
		)
		# If there is no such path, create
		if not os.path.exists(path):
			os.makedirs(path)

		file_path = os.path.join(path, file_obj.name)

		file_url = f'{settings.MEDIA_URL}tinymce/{file_obj.name}'

		if os.path.exists(file_path):
			return JsonResponse({
				"message": "file already exist",
				'location': file_url
			})

		with open(file_path, 'wb+') as f:
			for chunk in file_obj.chunks():
				f.write(chunk)

		return JsonResponse({
			'message': 'Image uploaded successfully',
			'location': file_url
		})
	return JsonResponse({'detail': "Wrong request"})