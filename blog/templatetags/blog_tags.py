from django import template
from blog.models import Comment, Opinion
from django.shortcuts import get_object_or_404


register = template.Library()

@register.simple_tag
def userLikedComment(user, commentId):
	try:
		c = get_object_or_404(Comment, id=int(commentId))
		o = get_object_or_404(Opinion, user=user, comment=c)
		if o.action==1:
			return "fas"
		return "far"

	except Exception as e:
		return "far"
			

@register.simple_tag
def userDislikedComment(user, commentId):
	try:
		c = get_object_or_404(Comment, id=int(commentId))
		o = get_object_or_404(Opinion, user=user, comment=c)
		if o.action==-1:
			return "fas"
		return "far"

	except Exception as e:
		return "far"
			
