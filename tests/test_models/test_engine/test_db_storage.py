#!/usr/bin/python3
"""test for db storage"""
import unittest
import pep8
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
from models.engine.db_storage import DBStorage


class TestDBStorage(unittest.TestCase):
    '''this will test the DBStorage'''

    def setUp(self):
        """Setup method"""
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.skipTest("Using file storage")

    def tearDown(self):
        """teardown"""
        storage.reload()

    def test_pep8_DB_Storage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    @unittest.skip("Review is not updated yet")
    def test_all(self):
        """tests if all works in database Storage"""
        obj = storage.all()
        self.assertEqual(type(obj), dict)

    @unittest.skip("Review is not updated yet")
    def test_all_class(self):
        """tests if all with class works in database Storage"""
        storage.new(State(name='Hawaii'))
        objs = storage.all()
        u_objs = storage.all(User)
        self.assertIsNotNone(objs)
        self.assertIsNotNone(u_objs)
        self.assertEqual(type(objs), dict)
        self.assertEqual(type(u_objs), dict)
        self.assertEqual(objs, storage.all())
        self.assertNotEqual(u_objs, storage.all())
        self.assertNotEqual(objs, u_objs)

    @unittest.skip("Review is not updated yet")
    def test_delete(self):
        """Tests if database deletion works"""
        u = User(first_name="Hello", last_name="Good bye")
        key = u.to_dict()['__class__'] + '.' + u.id
        objs = storage.all()
        self.assertNotIn(key, objs)
        storage.new(u)
        objs = storage.all()
        self.assertIn(key, objs)
        storage.delete(u)
        objs = storage.all()
        self.assertNotIn(key, objs)

    @unittest.skip("Review is not updated yet")
    def test_new(self):
        """test when new is called"""
        obj = storage.all()
        s = State('New York')
        self.assertIsNone(storage.__session.new)
        storage.new(s)
        self.assertIsNotNone(storage.__session.new)

    @unittest.skip("Review is not updated yet")
    def test_save(self):
        """test when save is called"""
        obj = storage.all()
        s = State('Nevada')
        self.assertIsNone(storage.__session.new)
        storage.new(s)
        self.assertIsNotNone(storage.__session.new)
        storage.save()
        self.assertInNone(storage.__session.new)

    def test_reload_db(self):
        """Test DBStorage reload does not error out
        """
        self.assertIsNone(storage.reload())

if __name__ == "__main__":
    unittest.main()
