from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User
from ..add_goal.models import Goal, Milestone, Animal, GoalAnimal
from django.contrib import messages
import datetime
def index(request):
	return render(request, 'login_reg_app/index.html')

def signin(request):
	if User.userManager.login_val(request.POST['email'], request.POST['password']):
		request.session['id'] = User.userManager.get_id(request.POST['email'],request.POST['password'])
		return redirect(reverse('dash'))
	else:
		messages.error(request, 'Invalid Login', extra_tags='login')
		return redirect(reverse('index'))

def logout(request):
	try:
		del request.session['id']
	except:
		pass
	return redirect(reverse('index'))

def validation(request):

	if request.method =='POST':
		valid = True
		if not User.userManager.name_val(request.POST['first_name']):
			messages.error(request, 'Name must be longer than 2 characters, Letters only', extra_tags='first_name')
			valid = False
		if not User.userManager.name_val(request.POST['last_name']):
			messages.error(request, 'Name must be longer than 2 characters, Letters only', extra_tags='last_name')
			valid = False
		if not User.userManager.email_val(request.POST['email']):
			messages.error(request, 'Invalid Email or Email already exists', extra_tags='email')
			valid = False
		if not User.userManager.password_val(request.POST['password']):
			messages.error(request, 'Must be 8 characters or longer', extra_tags='password')
			valid = False
		if not User.userManager.confirm_val(request.POST['password'], request.POST['confirm']):
			messages.error(request, 'Password does not match', extra_tags='confirm')
			valid = False
		if not User.userManager.alias_val(request.POST['alias']):
			messages.error(request, 'Alias must be at least 2 characters, Letters and numbers, Space, Dash, and Underscore only')
			valid = False

		if valid:
			User.userManager.register_user(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['alias'])

			request.session['id'] = User.userManager.get_id(request.POST['email'], request.POST['password'])
			messages.success(request, 'registered.')

			return redirect(reverse('dash'))
		else:
			return redirect(reverse('index'))

def dash(request):
	user = User.userManager.get(id=request.session['id'])
	today = datetime.datetime.now().date
	user_goals = Goal.goalManager.filter(user_id=user)
	goals = []
	for user_goal in user_goals:
		goal_id = user_goal.id
		animal = Goal.goalManager.getAnimal(goal_id)
		progress = Goal.goalManager.progress(goal_id)
		name = user_goal.title
		nextTask = Goal.goalManager.nextMilestone(goal_id)
		all_milestones = Milestone.milestoneManager.filter(goal_id=goal_id)
		goal_tuple = (animal, progress, name, nextTask, all_milestones)
		print animal
		print progress
		goals.append(goal_tuple)
	context = {
		'user' : user,
		'today' : today,
		'goals' : goals
	}
	return render(request, 'login_reg_app/dash.html', context)

def profile(request):
	#get profile
	context={'profile': User.userManager.filter(id=request.session['id'])}

	return render(request, 'login_reg_app/profile.html', context)

def edit_profile(request):
	context={'profile': User.userManager.filter(id=request.session['id'])}
	return render(request, 'login_reg_app/editprofile.html', context)

def edit_name(request):
	valid = True
	if not User.userManager.name_val(request.POST['first']):
		messages.error(request, 'Name must be longer than 2 characters, Letters only', extra_tags='first_name')
		valid = False

	if not User.userManager.name_val(request.POST['last']):
		messages.error(request, 'Name must be longer than 2 characters, Letters only', extra_tags='last_name')
		valid = False

	if valid:
		User.userManager.filter(id=request.session['id']).update(first_name=request.POST['first'], last_name=request.POST['last'])

	return redirect(reverse('edit_profile'))

def edit_email(request):
	if not User.userManager.email_val(request.POST['email']):
		messages.error(request, 'Invalid Email or Email is the same', extra_tags='email')
	else:
		User.userManager.filter(id=request.session['id']).update(email=request.POST['email'])
	return redirect(reverse('edit_profile'))
