# from Flask import g
from wtforms import Form, SelectField, SelectMultipleField, TextField, TextAreaField, PasswordField, validators, DateField, DateTimeField
# , RadioField, widgets, SelectMultipleField
import model

class LoginForm(Form):
    username = TextField("username", [validators.Required()])
    password = PasswordField("password", [validators.Required()])

class RegisterForm(Form):
    email = TextField("email", [validators.Required()])
    username = TextField("username", [validators.Required()])
    password = PasswordField("password", [validators.Required()])
    password_verify = PasswordField("password_verify", [validators.Required()])


# data = model.session.query(Activity).order_by(id=id).all()



class NewTripForm(Form):
	def create_activity_choices():
		activity_list = model.session.query(Activity).order_by(id).all()
		tuple_key_list = []
		tuple_val_list = []
		for activity in activity_list:
			tuple_key_list.append(activity.name)
			tuple_val_list.append(activity.id)
		return tuple_key_list, tuple_val_list
	def tuple_choices(tuple_key_list, tuple_val_list):
		activity_choices= zip(tuple_key_list, tuple_val_list)
		return activity_choices

    	name = TextField("trip_name", [validators.Required()])
    	destination = TextField("destination")
    # , [validators.Required()])
   	start_date = DateField("start_date")
    	# , [validators.Required()])
    	end_date = DateField("end_date")
    	# , [validators.Required()])
	
    	activities = SelectMultipleField('activity', choices='activity_choices')






# class MultiCheckboxField(SelectMultipleField):
#     """
#     A multiple-select, except displays a list of checkboxes.

#     Iterating the field will produce subfields, allowing custom rendering of
#     the enclosed checkbox fields.
#     """
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()




























    # activity = SelectField("activity")
    # activities = SelectMultipleField("activity", choices=model.session.query(Activity).order_by(id).get(id).all(), coerce=int)
    # activities = QuerySelectMultipleField("activity", coerce=int, query_factor=None, get_pk=None, get_label=None, allow_blank=True)



# def select_multi_checkbox(field, ul_class='', **kwargs):
#     kwargs.setdefault('type', 'checkbox')
#     field_id = kwargs.pop('id', field.id)
#     html = [u'<ul %s>' % html_params(id=field_id, class_=ul_class)]
#     for value, label, checked in field.iter_choices():
#         choice_id = u'%s-%s' % (field_id, value)
#         options = dict(kwargs, name=field.name, value=value, id=choice_id)
#         if checked:
#             options['checked'] = 'checked'
#         html.append(u'<li><input %s /> ' % html_options(**options))
#         html.append(u'<label %s>%s</label></li>')
#     html.append(u'</ul>')
#     return u''.join(html)


# class SelectMultipleField(SelectField):
#     """
#     No different from a normal select field, except this one can take (and
#     validate) multiple choices.  You'll need to specify the HTML `rows`
#     attribute to the select field when rendering.
#     """
#     widget = widgets.Select(multiple=True)

#     def iter_choices(self):
#         for value, label in self.choices:
#             selected = self.data is not None and self.coerce(value) in self.data
#             yield (value, label, selected)

#     def process_data(self, value):
#         try:
#             self.data = list(self.coerce(v) for v in value)
#         except (ValueError, TypeError):
#             self.data = None

#     def process_formdata(self, valuelist):
#         try:
#             self.data = list(self.coerce(x) for x in valuelist)
#         except ValueError:
#             raise ValueError(self.gettext(u'Invalid choice(s): one or more data inputs could not be coerced'))

#     def pre_validate(self, form):
#         if self.data:
#             values = list(c[0] for c in self.choices)
#             for d in self.data:
#                 if d not in values:
#                     raise ValueError(self.gettext(u"'%(value)s' is not a valid choice for this field") % dict(value=d))








