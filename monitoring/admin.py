from django.contrib import admin

from monitoring.models import Project, Contributor, Issue, Comment

admin.site.register(Project)
admin.site.register(Contributor)
admin.site.register(Issue)
admin.site.register(Comment)
