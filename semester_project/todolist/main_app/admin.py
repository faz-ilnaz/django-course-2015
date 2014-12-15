from django.contrib import admin

# Register your models here.
from main_app.models import *


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'color')


class AttachmentAdmin(admin.ModelAdmin):
    search_fields = ('content', )
    list_display = ('content', 'user')


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('text', 'comment_time')
    list_display = ('text', 'comment_time', 'task', 'user')


class DictionaryAdmin(admin.ModelAdmin):
    search_fields = ('value', )
    list_display = ('parent', 'value')


class FilterAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    list_display = ('text', 'user')


class LabelAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'color', 'user')


class NoteAdmin(admin.ModelAdmin):
    search_fields = ('text', )
    list_display = ('text', 'user')


class TaskAdmin(admin.ModelAdmin):
    search_fields = ('title', 't_date',)
    list_display = ('title', 't_date', 'priority', 'note', 'isDone', 'project')


class PriorityAdmin(admin.ModelAdmin):
    search_fields = ('name', 'value', )
    list_display = ('name', 'color','value', 'user')


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('birth_date', 'registration_date')
    list_display = ('user', 'avatar', 'birth_date', 'registration_date')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(Filter, FilterAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Priority, PriorityAdmin)
admin.site.register(Profile, ProfileAdmin)

