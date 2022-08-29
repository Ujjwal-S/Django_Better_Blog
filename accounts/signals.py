from .models import User, UserSession
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out

from .models import Profile

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


# @receiver(user_logged_in)
# def post_login(sender, user, request, **kwargs):
# 	print('*'*10)
# 	print("USER LOGGED IN.")
	
# 	sess_key = request.session.session_key
# 	user_session = UserSession.objects.create(
# 		user = request.user,
# 		device = "test device",
# 		sess_key = sess_key
# 	)
# 	user_session.save()

# 	print('*'*10)


@receiver(user_logged_out)
def post_logout(sender, request, user, **kwargs):
	if user:
		print("A user logged out.")
		print(user.username)
		try:
			sess_key = request.session.session_key
			UserSession.objects.get(user=user, sess_key=sess_key).delete()
		except:
			pass
		print('*'*10)
