from __future__ import unicode_literals

from django.db import models
from ..login_reg_app.models import User

class GoalManager(models.Manager):
    def insert_goal(self, title, description, due_date, priority, category_name, user_id, animal_name):
        category = Category.objects.get(category=category_name)
        user = User.userManager.get(id=user_id)
        self.create(title=title, description=description, due_date=due_date, category_id=category, user_id=user)
        this_goal = self.get(title=title, user_id=user, description=description)
        animal = Animal.objects.get(name=animal_name)
        GoalAnimal.objects.create(goal_id=this_goal, animal_id=animal, current_image=animal.image)

    def progress(self, goal_id):
        goal = self.get(id=goal_id)
        milestones = Milestone.objects.filter(goal_id=goal)
        total = len(milestones)
        count = 0
        for milestone in milestones:
            if (milestone.completed == True):
                count += 1
        try:
            print count
            print (count*100)/total
            return (count*100)/total
        except:
            return 1

    def nextMilestone(self, goal_id):
        goal = self.get(id=goal_id)
        milestones = Milestone.objects.filter(goal_id=goal)
        for milestone in milestones:
            if (milestone.completed == False):
                return milestone.title

    def getAnimal(self, goal_id):
        goal = self.get(id=goal_id)
        goal_animal = GoalAnimal.objects.get(goal_id=goal)
        return goal_animal.current_image

class MilestonelManager(models.Manager):
    def insert_milestone(self, title, goal_id):
        goal = Goal.objects.get(id=goal_id)
        self.create(title=title, goal_id=goal)


# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Animal(models.Model):
    name = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category)
    image = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Goal(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=50)

    category_id = models.ForeignKey(Category)
    user_id = models.ForeignKey(User)

    goalManager = GoalManager()
    objects = models.Manager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GoalAnimal(models.Model):
    goal_id = models.ForeignKey(Goal)
    animal_id = models.ForeignKey(Animal)
    current_image = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Milestone(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    reoccuring = models.BooleanField(default=False)
    goal_id = models.ForeignKey(Goal)

    milestoneManager = MilestonelManager()
    objects = models.Manager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
