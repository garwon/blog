from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from app import app, db
from models import Entry, Tag, User

class EntryModelView(ModelView):
    _status_choices = [(choice, label) for choice, label in [
        (Entry.STATUS_PUBLIC, 'Public'),
        (Entry.STATUS_DRAFT, 'Draft'),
        (Entry.STATUS_DELETED, 'Deleted'),
    ]]

    column_choices = {
        'status': _status_choices,
    }

    column_list = [
        'title', 'status', 'author', 'tease', 'tag_list', 'created_timestamp'
    ]
    column_select_related_list = ['author']

class UserModelView(ModelView):
    column_list = ['email', 'name', 'active', 'created_timestamp']
 
admin = Admin(app, 'Blog BackEnd')
admin.add_view(EntryModelView(Entry, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(UserModelView(User, db.session))

