from django.contrib import admin

# Register your models here.
from main_app.models import *

admin.site.register(Attachment)
admin.site.register(Comment)
admin.site.register(Dictionary)
admin.site.register(Filter)
admin.site.register(Label)
admin.site.register(Note)
admin.site.register(Task)
admin.site.register(Priority)
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Member)