import config
import bcrypt
from datetime import datetime, date, timedelta

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text, Index

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref, joinedload

from flask.ext.login import UserMixin

import pdb
# pdb.set_trace()  <--stops console running server at the point you insert this so you can interact with your code pythonically

engine = create_engine(config.DB_URI, echo=True)
session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class Declarations ####

class User(Base, UserMixin):
	__tablename__ = "users" 
	id = Column(Integer, primary_key=True)
	email = Column(String(64), nullable=False)
	username = Column(String(64), nullable=False)
	password = Column(String(64), nullable=False)
	salt = Column(String(64), nullable=False)

	def set_password(self, password):
		self.salt = bcrypt.gensalt()
		password = password.encode("utf-8")
		self.password = bcrypt.hashpw(password, self.salt)

	def authenticate(self, password):
		password = password.encode("utf-8")
		return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password

	def is_active(self):
		return True

	def is_authenticated(self):
		return True

	def get_id(self):
		return str(self.id)
	def is_anonymous(self):
		return False
	def is_authenticated(self):
		return True


class Trip(Base):
	__tablename__="trips"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	name = Column(String(64), nullable=False)
	destination= Column(String(100), nullable=True) # <-- Change to False later
	start_date = Column(DateTime, nullable=True) # Change to False later
	end_date = Column(DateTime, nullable=True) # Change to False later
	total_days = Column(Integer, nullable=True) # Change to False later

	## Relationship
	user = relationship("User", backref=backref("trips", order_by=id,lazy='dynamic'))

class PackingList(Base):
	__tablename__="packing_lists"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	trip_id = Column(Integer, ForeignKey('trips.id'))

	## Relationship
	user = relationship("User", backref=backref("packing_lists", order_by=id))
	trip = relationship("Trip", backref=backref("packing_lists", order_by=id))


class PackListItems(Base):
	__tablename__="packlist_items"
	id = Column(Integer, primary_key=True)
	packing_list_id=Column(Integer, ForeignKey('packing_lists.id'))
	item_id=Column(Integer, ForeignKey('items.id'))

	## Relationship
	packing_list = relationship("PackingList", backref=backref("packlist_items", order_by=id))
	item = relationship("Item", backref=backref("packlist_items", order_by=id))

class Item(Base):
	__tablename__="items"
	id = Column(Integer, primary_key=True)
	name = Column(String(64), nullable=False)

class ActivityItem(Base):
	__tablename__="activity_items"
	id = Column(Integer, primary_key=True)
	item_id = Column(Integer, ForeignKey('items.id'))
	activity_id = Column(Integer, ForeignKey('activities.id'))

	## Relationship
	item = relationship("Item", backref=backref("activity_items", order_by=id))
	activity = relationship("Activity", backref=backref("activity_items", order_by=id))

class Activity(Base):
	__tablename__="activities"
	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)

class TripActivity(Base):
	__tablename__="trip_activities"
	id = Column(Integer, primary_key=True)
	trip_id = Column(Integer, ForeignKey('trips.id'))
	activity_id = Column(Integer, ForeignKey('activities.id'))

	## Relationship
	trip = relationship("Trip", backref=backref("trip_activities", order_by=id))
	activity = relationship("Activity", backref=backref("trip_activities", order_by=id))

### End of class declarations  ###


#### Creating Tables in Database ####

def create_user(email, username, password):
	new_user = User(email=email, username=username)
	new_user.set_password(password)
	session.add(new_user)
	session.commit()

def create_trip(user_id, name, start_date, end_date):
	# add destination
	new_start = datetime.strptime(start_date, '%Y-%m-%d')
	new_end = datetime.strptime(end_date, '%Y-%m-%d')
	days_delta = new_end - new_start
	total_days = days_delta.days + 1
	new_trip = Trip(user_id=user_id,name=name,start_date=new_start, end_date=new_end, total_days=total_days)
	session.add(new_trip)
	session.commit()

def create_packinglist(user_id, trip_id):
    new_packinglist = PackingList(user_id=user_id, trip_id=trip_id)
    session.add(new_packinglist)
    session.commit()

def create_packlist_item(packing_list_id, item_id):
    new_packlist_items = PackListItems(packing_list_id=packing_list_id, item_id=item_id)
    session.add(new_packlist_items)
    session.commit()

def create_trip_activity(trip_id, activity_id):
    new_trip_activity = TripActivity(trip_id=trip_id, activity_id=activity_id)
    session.add(new_trip_activity)
    session.commit()


#### End Database Configuration ####

###############################################################################


# Check if there is a user with a certain username and password:
def validate_user(username, password):
	user = session.query(User).filter_by(username=username, password=password).first()
	if user == None:
		return None
	return user.id

# Check if an email already exists:
def email_exists(email):
    user = session.query(User).filter_by(email=email).first()
    if user == None:
        return False
    return True


# Check if a username is already taken:
def username_exists(username):
    user = session.query(User).filter_by(username=username).first()
    if user == None:
        return False
    return True


####### "GET" Functions #########


## USER ##

def get_user_by_id(id):
	user = session.query(User).filter_by(id=id).one()
	return user

def get_user_by_username(username):
	user = session.query(User).filter_by(username=username).first()
	return user

def get_user_by_trip_id(id):
	user = get_user_by_id(get_trip_by_id(id))
	return user

###########################

## TRIP ##

# Get a trip's attributes by trip_id 
def get_trip_by_id(id):
	trip = session.query(Trip).filter_by(id=id).one()
	return trip

def get_trip_by_packlist_id(id):
	packing_list = session.query(PackingList).filter_by(id=id).one()
	trip_id = packing_list.trip_id
	trip = get_trip_by_id(trip_id)
	return trip

# Get a list of trip names by the user's id
def get_user_trip_names(id):
	trips = session.query(Trip).filter_by(user_id=id).order_by(Trip.name).all()
	trip_list = []
	for trip in trips:
		trip_list.append(trip.name)
	return trip_list

# Get's a trip's attributes by trip name
def get_trip_by_name(name):
	trip = session.query(Trip).filter_by(name=name).first()
	return trip


#####################

## PACKING_LIST ##

# Get a list of packing_list_id's by user_id:
def get_user_packlist(id):
	packlists = session.query(PackingList).filter_by(user_id=id).all()
	user_trips = []
	for packlist in packlists:
		user_trips.append(packlist.id)
	return user_trips




# Get a list of item names for a packing list by packing_list_id
# def get_packing_list(id):
# 	item_id_list = session.query(PackListItems).filter_by(packing_list_id=id)
# 	list_item_names = []
# 	item_id = item_id_list[item_id]
# 	for item in item_id_list:

# 		item_name = get_item_name_by_id(item_id)
# 		list_item_names.append(item.name)

		##### ABOVE IS NOT WORKING YET!!!! ######


# Get a packing list of items by trip name
def get_pl_items_by_trip_name(name):
	trip = get_trip_by_name(name)
	packing_list = session.query(PackingList).filter_by(trip_id=trip.id).first()
	packlist_items = get_packing_list(packing_list_id=packing_list.id).all()
	return packlist_items


#####################

## ITEM ##

# Get a list of all items in DATABASE
def get_list_of_items():
	items = session.query(Item).all()
	item_list = []
	for i in items:
		item_list.append(i.name)   # .sort()
	return item_list



# Get item name by item id
def get_item_name_by_id(id):
	item = session.query(Item).filter_by(id=id).first()
	return item.name


#####################


# get trip name and packing list id by trip id
def trip_name_packlist_id(trip_id):
	packlist = session.query(PackingList).filter_by(trip_id=trip_id).one()
	trip = session.query(Trip).filter_by(id=trip_id).one()
	return trip.name, packlist.id

######## "Pull Items" Functions #########

# Get activity by trip_id
def get_activity_by_trip(id):
	trip_activity = session.query(TripActivity).filter_by(trip_id=id).first()
	activity = session.query(Activity).filter_by(id=trip_activity.activity_id).first()
	return activity

# Get a list of item's by activity_id
# def get_items_by_activity(id):
# 	activity_ = session.query(Activity).filter_by()


######### Dictionaries for possible later use #############

# Get a dictionary of all items in DATABASE
def get_dict_of_items():
	item_dict = {}
	item_list = get_list_of_items()
	for item in item_list:
		item_dict[item] = 1
	return item_dict

# Get a dictionary of item names for a packing list (by packing_list_id)
def get_packing_dict(id):
	item_id_list = session.query(PackListItems).filter_by(packing_list_id=id).all()
	packlist_items = {}
	for item in item_id_list:
		packlist_items[item.name] = 1
	return packlist_items

###########################################################

def create_tables():
	Base.metadata.create_all(engine)

def main():
	pass

if __name__ == "__main__":
	main()











