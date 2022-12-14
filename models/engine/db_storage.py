#!/usr/bin/python3
"""
This is the db_storage module
"""
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import (sessionmaker, scoped_session)
from os import getenv
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class DBStorage:
    """
    The storage system for HBnB
    Uses MySQL databases
    """
    __engine = None
    __session = None
    __Session = None

    def __init__(self):
        """
        initializes engine
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')))
        self.__models_available = {"User": User,
                                   "Amenity": Amenity, "City": City,
                                   "Place": Place, "Review": Review,
                                   "State": State}
        if getenv('HBNB_MYSQL_ENV', 'not') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        returns a dictionary of all the class objects
        """
        orm_objects = {}
        if cls:
            for k in self.__session.query(self.__models_available[cls]):
                orm_objects[k.__dict__['id']] = k
        else:
            for i in self.__models_available.values():
                j = self.__session.query(i).all()
                if j:
                    for k in j:
                        orm_objects[k.__dict__['id']] = k
        return orm_objects

    def new(self, obj):
        """
        adds a new obj to the session
        """
        self.__session.add(obj)

    def save(self):
        """
        saves the objects fom the current session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes an object from the current session
        """
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """
        WARNING!!!! I'm not sure if Base.metadata.create_all needs to
        be in the init method
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def close(self):
        """
        close a session
        """
        self.__session.remove()

    def get(self, cls, id):
        """
        Get the specified object by class and id
        """
        obj = None
        if cls:
            get_cls = self.__models_available.get(cls)
            if get_cls:
                obj = self.__session.query(get_cls).filter_by(id=id).first()
        return obj

    def count(self, cls=None):
        """
        Count the number of a given class in the database
        """
        orm_objects = {}
        if cls:
            for k in self.__session.query(self.__models_available[cls]):
                orm_objects[k.__dict__['id']] = k
        else:
            for i in self.__models_available.values():
                j = self.__session.query(i).all()
                if j:
                    for k in j:
                        orm_objects[k.__dict__['id']] = k
        return len(orm_objects)
