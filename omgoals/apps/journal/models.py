from __future__ import unicode_literals
from ..login_reg_app.models import User
from django.db import models
from ..add_goal.models import Goal


class Journal(models.Model):
	user_id = models.ForeignKey(User)
	goal_id = models.ForeignKey(Goal)
	entry = models.CharField(max_length=1000)
	entry_date = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

