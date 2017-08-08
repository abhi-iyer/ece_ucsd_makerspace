from .models import User
def get_user(pid):
	try:
		user = User.objects.get(pid=pid)
		return user
	except:
		return None #No entry

def card_parse(input):
	if input:
		if ( input[0] == ';' ):
			# magnetic-strip card swiper's rules
			user_pid = input[2:11]
			return user_pid
		else:
			return 0

