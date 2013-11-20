import model
import csv
# import datetime


def load_items(session):
    with open("seed_data/u.items") as csvfile:
        items = csv.reader(csvfile,delimiter="|")
        for item in items:
                new_item = model.Item(name=item[0])
                session.add(new_item)
    return session


def load_activities(session):
    with open("seed_data/u.activities") as csvfile:
        activities = csv.reader(csvfile,delimiter="|")
        for activity in activities:
                new_activity = model.Activity(name=activity[0])
                session.add(new_activity)
    return session


def load_activity_items(session):
    with open("seed_data/u.activity_items", "rb") as csvfile:
        activity_items = csv.reader(csvfile, delimiter=",")
        for activity_item in activity_items:
                new_activity_item = model.ActivityItem(item_id=activity_item[0], activity_id=activity_item[1])
                session.add(new_activity_item)
    return session


def main():
    load_items(model.session)
    load_activities(model.session)
    load_activity_items(model.session)
    session.commit()


if __name__ == "__main__":
    model.Base.metadata.create_all(model.engine)
    session = model.session
    main()

    # model.create_tables()
    # session = model.session
    # s = model.connect()

    # session = model.session
    # model.create_user()
    # model.create_trip()
    # model.create_packinglist()
    # model.create_packlist_item()
    # model.create_trip_activity()

# def main():
    # session = model.connect()
    # model.create_tables()


# def load_activities(session):
#     f = open('seed_data/u.activities')
#     lines = f.readlines()
#     for line in lines:
#         activity = line.split()

#         new_activity = model.Activity(name=activity[0])
#         session.add(new_activity) 
#     session.commit()
#     f.close()

# def load_activity_items(session):
#     f = open('seed_data/u.activity_items')
#     lines = f.readlines()
#     for line in lines:
#         activity_items = line.split("|")

#         new_activity_item = model.ActivityItem(item_id=activity_items[0], activity_id=activity_items[1])
#         session.add(new_activity_item) 
#     session.commit()
#     f.close()