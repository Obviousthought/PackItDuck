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


class Trip(Base):
	__tablename__="trips"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	name = Column(String(64), nullable=False)
	destination= Column(String(100), nullable=False)
	length_of_trip= Column(Integer, nullable=True)  # nullable=True for now

	user = relationship("User", backref=backref("trips", order_by=id))

class PackingList(Base):
	__tablename__="packing_lists"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	trip_id = Column(Integer, ForeignKey('trips.id'))

### Write code to auto-update user_id in Trip and PackingList ####

	user = relationship("User", backref=backref("packing_lists", order_by=id))
	trip = relationship("Trip", backref=backref("packing_lists", order_by=id))

# google sqlalchemy: auto-update for foreignkeys
# figure out why db let you add packing list to a trip that didn't exist


class PackListItems(Base):
	__tablename__="packlist_items"
	id = Column(Integer, primary_key=True)
	packing_list_id=Column(Integer, ForeignKey('packing_lists.id'))
	item_id=Column(Integer, ForeignKey('items.id'))

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

	trip = relationship("Trip", backref=backref("trip_activities", order_by=id))
	activity = relationship("Activity", backref=backref("trip_activities", order_by=id))


### End of class declarations  ###

# 1 adds a new user to the database
def create_user(email, username, password):
	new_user = User(email=email, username=username)
	new_user.set_password(password)
	session.add(new_user)
	session.commit()

# 2 retrieves user attributes as a list with the user's id
def get_user_by_id(id):
	user = session.query(User).get(id)
	return user


# 3 Returns a list of trip_id's for the user:
def get_user_packlist(id):
	packlist = session.query(PackingList).filter_by(user_id=id)
	user_trips = []
	for p in packlist:
		user_trips.append(p.id)
	return user_trips

# 4 Check if there is a user with a certain username and password:
def validate_user(username, password):
	user = session.query(User).filter_by(username=username, password=password).first()
	if user == None:
		return None
	return user.id

# 5 Check if an email already exists:
def email_exists(email):
    user = session.query(User).filter_by(email=email).first()
    if user == None:
        return False
    return True


# 6 Check if a username is already taken:
def username_exists(username):
    user = session.query(User).filter_by(username=username).first()
    if user == None:
        return False
    return True



def create_tables():
	Base.metadata.create_all(engine)


if __name__ == "__main__":
	create_tables()