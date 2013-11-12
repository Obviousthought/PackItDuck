import config
import bcrypt
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

from flask.ext.login import UserMixin

engine = create_engine(config.DB_URI, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
						 autocommit = False,
						 autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class User(Base, UserMixin):
	__tablename__ = "users" 
	id = Column(Integer, primary_key=True)
	email = Column(String(64), nullable=False)
	username = Column(String(64), nullable=False)
	password = Column(String(64), nullable=False)
	salt = Column(String(64), nullable=False)

	trip = relationship("Trip", backref=backref("users", order_by=id))
	packing_list = relationship("PackingList", backref=backref("users", order_by=id))
	# posts = relationship("Post", uselist=True)

	def set_password(self, password):
		self.salt = bcrypt.gensalt()
		password = password.encode("utf-8")
		self.password = bcrypt.hashpw(password, self.salt)

	def authenticate(self, password):
		password = password.encode("utf-8")
		return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password


class Trip(Base):
	__tablename__="trips"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	# packing_list_id = Column(Integer, ForeignKey('packing_lists.id')) #nullable=True?
	name = Column(String(64), nullable=False)
	destination= Column(String(100), nullable=False)
	length_of_trip= Column(Integer, nullable=True)  # Figure out how to time units (ex. 2-3 months)

########## Put this here? ############
	activities_id=Column(Integer, ForeignKey('activities.id'))  #might not have activities added
##########

	packing_list = relationship("PackingList", uselist=False, backref=backref("trips", order_by=id))
	activity = relationship("Activity", backref=backref("trips", order_by=id))


class PackingList(Base):
	__tablename__="packing_lists"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	trip_id = Column(Integer, ForeignKey('trips.id'))

	packlist_item = relationship("PackListItems", backref=backref("packing_lists", order_by=id))


class PackListItems(Base):
	__tablename__="packlist_items"
	id = Column(Integer, primary_key=True)
	packing_list_id=Column(Integer, ForeignKey('packing_lists.id'))
	item_id=Column(Integer, ForeignKey('items.id'))

	# packing_list = relationship("PackingList", backref=backref("packlist_items", order_by=id))
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

	item = relationship("Item", backref=backref("activity_items", order_by=id))
	activity = relationship("Activity", backref=backref("activity_items", order_by=id))

class Activity(Base):
	__tablename__="activities"
	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)


### End of class declarations  ###

def create_user(username, email, password):
	new_user = User(username=username, email=email, password=password)
	session.add(new_user)
	session.commit()

def user_by_id(id):
	user=session.query(User).get(id).first()
	return user

def get_user_trips(id):
	user = session.query(User).filter_by(id=id).first()
	trips = user.trips
	user_trips = {}
	for trip in trips:
		user_trips[trip.user_id] = trip.trip
	return user_trips

def userExists(username, email):
	user = session.query(User).filter_by(username=username, email=email).first()
	if user == None:
		return False
	return True

# In views.py:

# def user_exists(email):
# 	user = session.query(User).filter_by(email=email).first()
# 	if user == None:
# 		return False
# 	return True

# def authenticate(username, email, password):
# 	user = session.query(User).filter_by(username=username, email=email, password=password).first()
# 	if user == None:
# 		return None
# 	return user.id


def main():
	pass


if __name__ == "__main__":
	main()










