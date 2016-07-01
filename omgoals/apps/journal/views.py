from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from ..login_reg_app.models import User
from ..add_goal.models import Goal
from ..achieved_app.models import Achieved
from django.contrib import messages
from .models import Journal

def journal(request):
	user_object= User.userManager.get(id=request.session['id'])

	context={'journal_entries': Journal.objects.filter(user_id=user_object).order_by('entry_date'),
			'goals': Goal.goalManager.filter(user_id=user_object),
			'achieved': Achieved.objects.filter(user_id=user_object)}

	print  Achieved.objects.filter(user_id=user_object)

	return render(request, 'journal.html', context)

def add_journal(request):
	user_object= User.userManager.get(id=request.session['id'])
	goal_object= Goal.goalManager.get(id=request.POST['goal'])
	Journal.objects.create(user_id=user_object, goal_id=goal_object, entry=request.POST['entry'], entry_date=request.POST['due_date'])
	return redirect(reverse('journal'))