# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table(u'main_app_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('t_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main_app.Priority'], null=True)),
            ('note', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main_app.Note'], null=True)),
            ('isDone', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', null=True, to=orm['main_app.Project'])),
            ('attachments', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main_app.Attachment'], null=True)),
        ))
        db.send_create_signal(u'main_app', ['Task'])

        # Adding M2M table for field labels on 'Task'
        m2m_table_name = db.shorten_name(u'main_app_task_labels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm[u'main_app.task'], null=False)),
            ('label', models.ForeignKey(orm[u'main_app.label'], null=False))
        ))
        db.create_unique(m2m_table_name, ['task_id', 'label_id'])

        # Adding model 'Label'
        db.create_table(u'main_app_label', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main_app.Dictionary'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'main_app', ['Label'])

        # Adding model 'Project'
        db.create_table(u'main_app_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['auth.User'])),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main_app.Dictionary'], null=True)),
        ))
        db.send_create_signal(u'main_app', ['Project'])

        # Adding model 'Note'
        db.create_table(u'main_app_note', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'main_app', ['Note'])

        # Adding model 'Attachment'
        db.create_table(u'main_app_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'main_app', ['Attachment'])

        # Adding model 'Filter'
        db.create_table(u'main_app_filter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'main_app', ['Filter'])

        # Adding model 'Priority'
        db.create_table(u'main_app_priority', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main_app.Dictionary'], null=True)),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'main_app', ['Priority'])

        # Adding model 'Dictionary'
        db.create_table(u'main_app_dictionary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main_app.Dictionary'])),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'main_app', ['Dictionary'])

        # Adding model 'Profile'
        db.create_table(u'main_app_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('about_me', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('registration_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main_app', ['Profile'])

        # Adding model 'Comment'
        db.create_table(u'main_app_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('comment_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main_app.Task'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'main_app', ['Comment'])

        # Adding M2M table for field attachment on 'Comment'
        m2m_table_name = db.shorten_name(u'main_app_comment_attachment')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm[u'main_app.comment'], null=False)),
            ('attachment', models.ForeignKey(orm[u'main_app.attachment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['comment_id', 'attachment_id'])


    def backwards(self, orm):
        # Deleting model 'Task'
        db.delete_table(u'main_app_task')

        # Removing M2M table for field labels on 'Task'
        db.delete_table(db.shorten_name(u'main_app_task_labels'))

        # Deleting model 'Label'
        db.delete_table(u'main_app_label')

        # Deleting model 'Project'
        db.delete_table(u'main_app_project')

        # Deleting model 'Note'
        db.delete_table(u'main_app_note')

        # Deleting model 'Attachment'
        db.delete_table(u'main_app_attachment')

        # Deleting model 'Filter'
        db.delete_table(u'main_app_filter')

        # Deleting model 'Priority'
        db.delete_table(u'main_app_priority')

        # Deleting model 'Dictionary'
        db.delete_table(u'main_app_dictionary')

        # Deleting model 'Profile'
        db.delete_table(u'main_app_profile')

        # Deleting model 'Comment'
        db.delete_table(u'main_app_comment')

        # Removing M2M table for field attachment on 'Comment'
        db.delete_table(db.shorten_name(u'main_app_comment_attachment'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main_app.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'content': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main_app.comment': {
            'Meta': {'object_name': 'Comment'},
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main_app.Attachment']", 'symmetrical': 'False'}),
            'comment_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main_app.Task']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main_app.dictionary': {
            'Meta': {'object_name': 'Dictionary'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main_app.Dictionary']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'main_app.filter': {
            'Meta': {'object_name': 'Filter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main_app.label': {
            'Meta': {'object_name': 'Label'},
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main_app.Dictionary']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main_app.note': {
            'Meta': {'object_name': 'Note'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main_app.priority': {
            'Meta': {'object_name': 'Priority'},
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main_app.Dictionary']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'main_app.profile': {
            'Meta': {'object_name': 'Profile'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'main_app.project': {
            'Meta': {'object_name': 'Project'},
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main_app.Dictionary']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': u"orm['auth.User']"})
        },
        u'main_app.task': {
            'Meta': {'object_name': 'Task'},
            'attachments': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main_app.Attachment']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isDone': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main_app.Label']", 'null': 'True', 'symmetrical': 'False'}),
            'note': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main_app.Note']", 'null': 'True'}),
            'priority': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main_app.Priority']", 'null': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'null': 'True', 'to': u"orm['main_app.Project']"}),
            't_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['main_app']