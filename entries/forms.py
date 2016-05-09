import wtforms

from wtforms import validators
from wtforms.validators import DataRequired
from models import Entry, Tag

class TagField(wtforms.StringField):
    def _value(self):
        if self.data:
            return ', '.join([tag.name for tag in self.data])
        return ''
    
    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')
        tag_names = [name.strip() for name in raw_tags if name.strip()]
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])
        new_tags = [Tag(name=name) for name in new_names]
        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []

class EntryForm(wtforms.Form):
    title = wtforms.StringField('Title', validators=[DataRequired()])
    body = wtforms.TextAreaField('Body', validators=[DataRequired()])
    status = wtforms.SelectField(
        'Entry status',
        choices = (
            (Entry.STATUS_PUBLIC, 'Public'),
            (Entry.STATUS_DRAFT, 'Draft')),
        coerce=int)
    tags = TagField('Tags', description='Separate multiple tags with commas.')

    def save_entry(self, entry):
        self.populate_obj(entry)
        entry.generate_slug()
        return entry

class ImageForm(wtforms.Form):
    file = wtforms.FileField('Image file')

class CommentForm(wtforms.Form):
    name = wtforms.StringField('Name', validators=[validators.DataRequired()])
    email = wtforms.StringField('Email', validators=[
        validators.DataRequired(),
        validators.Email()])
    url = wtforms.StringField('URL', validators=[
        validators.Optional(),
        validators.URL()])
    body = wtforms.TextAreaField('Comment', validators=[
        validators.DataRequired(),
        validators.Length(min=10, max=3000)])
    entry_id = wtforms.HiddenField(validators=[
        validators.DataRequired()])

    def validate(self):
        if not super(CommentForm, self).validate():
            return False

        entry = Entry.query.filter(
            (Entry.status == Entry.STATUS_PUBLIC) &
            (Entry.id == self.entry_id.data)).first()

        if not entry:
            return False

        return True
