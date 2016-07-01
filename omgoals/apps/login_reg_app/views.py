from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User
from ..add_goal.models import Goal, Milestone, Animal, GoalAnimal
from django.contrib import messages
import datetime
import json, re
from django.views.decorators.csrf import csrf_exempt

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
		animal = GoalAnimal.objects.get(goal_id=user_goal).current_image
		progress = Goal.goalManager.progress(goal_id)
		name = user_goal.title
		nextTask = Goal.goalManager.nextMilestone(goal_id)
		all_milestones = Milestone.milestoneManager.filter(goal_id=goal_id)
		done = []
		milestoneTitles = []
		for milestone in all_milestones:
			done.append(milestone.completed)
			milestoneTitles.append(milestone.title)
		json_done = json.dumps(done)
		json_titles = json.dumps(milestoneTitles)
		json_goal = json.dumps(goal_id)
		goal_tuple = (animal, progress, name, nextTask, json_done, json_titles, json_goal)
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

@csrf_exempt
def complete(request):
	goal_id = request.POST['goal_id']
	goal = Goal.goalManager.get(id=goal_id)
	title = request.POST['title']
	milestone_interest = Milestone.milestoneManager.filter(goal_id=goal, title=title)[0]
	milestone_interest.completed = True
	milestone_interest.save()
	goal_ani = GoalAnimal.objects.get(goal_id=goal)
	current_animal = json.dumps(GoalAnimal.objects.get(goal_id=goal).current_image)
	if (Goal.goalManager.progress(goal_id) > 33 and Goal.goalManager.progress(goal_id) < 66):
		current_animal = current_animal.replace('1', '2')
		goal_ani.current_image = current_animal[1:-1].decode('unicode-escape')
		goal_ani.save()
		print('here')
	elif (Goal.goalManager.progress(goal_id) > 66):
		current_animal = current_animal.replace('2', '3')
		goal_ani.current_image = current_animal[1:-1].decode('unicode-escape')
		goal_ani.save()
		print('there')
	return redirect(reverse('dash'))
