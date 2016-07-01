"""omgoals URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from apps.login_reg_app.models import User
from apps.achieved_app.models import Achieved
from apps.add_goal.models import Category, Animal, Goal, GoalAnimal, Milestone
from apps.journal.models import Journal

class UserAdmin(admin.ModelAdmin):
	pass
admin.site.register(User, UserAdmin)
admin.site.register(Category, UserAdmin)
admin.site.register(Animal, UserAdmin)
admin.site.register(Goal, UserAdmin)
admin.site.register(GoalAnimal, UserAdmin)
admin.site.register(Milestone, UserAdmin)
admin.site.register(Achieved, UserAdmin)
admin.site.register(Journal, UserAdmin)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.login_reg_app.urls')),
    url(r'^add', include('apps.add_goal.urls')),
    url(r'^journal', include('apps.journal.urls')),
    url(r'^achieved', include('apps.achieved_app.urls'))
]
