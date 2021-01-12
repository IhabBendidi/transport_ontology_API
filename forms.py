from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf import Form

class SearchForm(Form):
  search = StringField('', [DataRequired()])
  submit = SubmitField('Search',
                       render_kw={'class': 'btn btn-success btn-block'})
