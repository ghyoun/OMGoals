from django.shortcuts import render
from .models import Achieved
from ..login_reg_app.models import User

def achieved_page(request):
	user_object = User.userManager.get(id=request.session['id'])
	context={'achieved': Achieved.objects.filter(user_id=user_object).order_by('-completion_date')}
	return render(request, 'achieved_app/achieved.html', context)