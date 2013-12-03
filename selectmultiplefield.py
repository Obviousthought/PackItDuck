# in forms.py


activity_list = model.session.query(Activity).order_by(id).all()

tuple_key_list = []
tuple_val_list = []

for activity in activity_list:
	tuple_key_list.append(activity.name)
	tuple_val_list.append(activity.id)
return tuple_key_list, tuple_val_list

activity_choices= zip(tuple_key_list, tuple_val_list)

class NewTrip(Form):

	activities = SelectMultipleField('activities', choices=activity_choices, option_widget=CheckboxInput(), widget=ListWidget(prefix_label=True))