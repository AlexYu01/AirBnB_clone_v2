#!/usr/bin/python3
"""test for console"""
import unittest
from unittest.mock import patch
from io import StringIO
import pep8
import os
import json
import console
import tests
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage
from models import storage
import sqlalchemy
import MySQLdb


class TestConsole(unittest.TestCase):
    """this will test the console"""

    @classmethod
    def setUpClass(cls):
        """setup for the test"""
        cls.consol = HBNBCommand()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.consol

    def setUp(self):
        """Setup method"""
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            self.skipTest("Using db storage")

    def tearDown(self):
        """Remove temporary file (file.json) created as a result"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_console(self):
        """Pep8 console.py"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["console.py"])
        self.assertEqual(p.total_errors, 0, 'fix Pep8')

    def test_docstrings_in_console(self):
        """checking for docstrings"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        """test quit command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("quit")
            self.assertEqual('', f.getvalue())

    def test_create(self):
        """Test create command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            self.assertEqual(
                "[[User]", f.getvalue()[:7])

    def test_create_basemodel_0(self):
        """Test create command on BaseModel with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create BaseModel name=\"TV\"")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all BaseModel")
            self.assertNotIn('\'name\': \'TV\'', f.getvalue())

    def test_create_amenity_0(self):
        """Test create command on Amenity with valid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Amenity name=\"TV\"")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Amenity")
            self.assertIn('\'name\': \'TV\'', f.getvalue())

    def test_create_amenity_1(self):
        """Test create command on Amenity with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Amenity name=\"TV\" inval=\"nope\"")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Amenity")
            self.assertNotIn('\'inval\': \'nope\'', f.getvalue())

    def test_create_city_0(self):
        """Test create command on City with valid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create City state_id=\"12\"\
            name=\"San_Francisco\"")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all City")
            self.assertIn('\'state_id\': \'12\'', f.getvalue())
            self.assertIn('\'name\': \'San Francisco\'', f.getvalue())

    def test_create_city_1(self):
        """Test create command on City with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create City num=0")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all City")
            self.assertNotIn('\'num\': 0', f.getvalue())

    def test_create_place_0(self):
        """Test create command on Place with valid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Place city_id=\"1\" user_id=\"2\"\
            name=\"Holberton\" description=\"Nice_house\" number_rooms=10\
            number_bathrooms=3 max_guest=100 price_by_night=9000 latitude=0.0\
            longitude=9.9")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Place")
            self.assertIn('\'city_id\': \'1\'', f.getvalue())
            self.assertIn('\'user_id\': \'2\'', f.getvalue())
            self.assertIn('\'name\': \'Holberton\'', f.getvalue())
            self.assertIn('\'description\': \'Nice house\'', f.getvalue())
            self.assertIn('\'number_rooms\': 10', f.getvalue())
            self.assertIn('\'number_bathrooms\': 3', f.getvalue())
            self.assertIn('\'max_guest\': 100', f.getvalue())
            self.assertIn('\'price_by_night\': 9000', f.getvalue())
            self.assertIn('\'latitude\': 0.0', f.getvalue())
            self.assertIn('\'longitude\': 9.9', f.getvalue())

    def test_create_place_1(self):
        """Test create command on Place with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Place max_guest=\"String\"")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Place")
            self.assertNotIn('\'max_guest\': \'String\'', f.getvalue())

    def test_create_review_0(self):
        """Test create command on Review with valid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Review text=\"Great\"")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Review")
            self.assertIn('\'text\': \'Great\'', f.getvalue())

    def test_create_review_1(self):
        """Test create command on Review with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Review text=\"Great\" inval=\"nope\"")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Review")
            self.assertNotIn('\'inval\': \'nope\'', f.getvalue())

    def test_create_state_0(self):
        """Test create command on State with valid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create State name=\"California\"")
        sid = f.getvalue()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all State")
            self.assertIn('\'name\': \'California\'', f.getvalue())
            self.consol.onecmd("destroy State " + sid)

    def test_create_state_1(self):
        """Test create command on State with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create State name=10")
        sid = f.getvalue()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all State")
            self.assertNotIn('\'name\'', f.getvalue())
            self.consol.onecmd("destroy State " + sid)

    def test_create_user_0(self):
        """Test create command on User with valid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User email=\"BettyHolberton@gmail.com\"\
            password=\"not_encrypted\" first_name=\"Betty\"\
            last_name=\"Holberton\"")
        oid = f.getvalue()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            self.assertIn('\'email\': \'BettyHolberton@gmail.com\'',
                          f.getvalue())
            self.assertIn('\'password\': \'not encrypted\'', f.getvalue())
            self.assertIn('\'first_name\': \'Betty\'', f.getvalue())
            self.assertIn('\'last_name\': \'Holberton\'', f.getvalue())

    def test_create_user_1(self):
        """Test create command on User with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User email=20")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            self.assertNotIn('\'email\': 20', f.getvalue())

    def test_show(self):
        """Test show command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_all(self):
        """Test all command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())

    def test_update(self):
        """Test update command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", f.getvalue())

    def test_z_all(self):
        """Test alternate all command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("asdfsdfsd.all()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("State.all()")
            self.assertEqual("[]\n", f.getvalue())

    def test_z_count(self):
        """Test count command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("asdfsdfsd.count()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("State.count()")
            self.assertEqual("0\n", f.getvalue())

    def test_z_show(self):
        """Test alternate show command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("safdsa.show()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("BaseModel.show(abcd-123)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test alternate destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("Galaxy.destroy()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.destroy(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_update(self):
        """Test alternate destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("sldkfjsl.update()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(" + my_id + ")")
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(" + my_id + ", name)")
            self.assertEqual(
                "** value missing **\n", f.getvalue())


class TestConsoleDb(unittest.TestCase):
    """This will test the console class on DB storage"""

    @classmethod
    def setUpClass(cls):
        """setup for the test"""
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            return
        try:
            cls.consol = HBNBCommand()
            cls.s = State(name='California')
            cls.s.save()
            cls.c = City(name='San Francisco', state_id=cls.s.id)
            cls.c.save()
            cls.u = User(email='Betty@holberton.com', password='Hello')
            cls.u.save()
            cls.p = Place(city_id=cls.c.id, user_id=cls.u.id, name='Home')
            cls.p.save()
        except Exception:
            return

    def setUp(self):
        """Setup method"""
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.skipTest("Using file storage")
        if self.s.id is None or self.c.id is None or self.u.id is None or\
                self.p.id is None:
            self.skipTest("Failed to save objects into database")
        self.create_conn()

    def tearDown(self):
        """Teardown method to reload session"""
        self.cur.close()
        self.conn.close()

    def create_conn(self):
        """Setup mysqldb connection and cursor"""
        self.conn = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'),
                                    port=3306,
                                    user=os.getenv('HBNB_MYSQL_USER'),
                                    passwd=os.getenv('HBNB_MYSQL_PWD'),
                                    db=os.getenv('HBNB_MYSQL_DB'),
                                    charset="utf8")
        self.cur = self.conn.cursor()

    def test_create_amenity_0(self):
        """Test create command on Amenity with valid parameters."""
        self.cur.execute('SELECT COUNT(id) FROM amenities')
        o_count = self.cur.fetchall()

        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create Amenity name="TV"')

        self.tearDown()
        self.create_conn()
        self.cur.execute('SELECT COUNT(id) FROM amenities')
        n_count = self.cur.fetchall()
        self.assertNotEqual(o_count, n_count)

    def test_create_amenity_1(self):
        """Test create command on Amenity with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create Amenity name="Couch" inval="nope"')
        id = f.getvalue()[:-1]

        self.tearDown()
        self.create_conn()
        self.cur.execute("SELECT * FROM amenities WHERE id = '{}'".format(id))
        rows = self.cur.fetchall()
        self.assertIsNotNone(rows)
        self.assertIn('Couch', rows[0])
        self.assertNotIn('inval', rows[0])

    def test_create_city_0(self):
        """Test create command on City with valid parameters."""
        self.cur.execute('SELECT COUNT(id) FROM cities')
        o_count = self.cur.fetchall()

        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create City state_id="{}"\
            name="San_Francisco"'.format(self.s.id))

        self.tearDown()
        self.create_conn()
        self.cur.execute('SELECT COUNT(id) FROM cities')
        n_count = self.cur.fetchall()
        self.assertNotEqual(o_count, n_count)

    def test_create_city_1(self):
        """Test create command on City with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create City state_id="{}"\
            name="San_Francisco" boop=10'.format(self.s.id))
        id = f.getvalue()[:-1]

        self.tearDown()
        self.create_conn()
        self.cur.execute("SELECT * FROM cities WHERE id = '{}'".format(id))
        rows = self.cur.fetchall()
        self.assertIsNotNone(rows)
        self.assertIn('San Francisco', rows[0])
        self.assertNotIn('boop', rows[0])

    def test_create_place_0(self):
        """Test create command on Place with valid parameters."""
        self.cur.execute('SELECT COUNT(id) FROM places')
        o_count = self.cur.fetchall()

        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create Place city_id="{}" user_id="{}"\
            name="Holberton" description="Nice_house" number_rooms=10\
            number_bathrooms=3 max_guest=100 price_by_night=9000 latitude=0.0\
            longitude=9.9'.format(self.c.id, self.u.id))

        self.tearDown()
        self.create_conn()
        self.cur.execute('SELECT COUNT(id) FROM places')
        n_count = self.cur.fetchall()
        self.assertNotEqual(o_count, n_count)

    def test_create_place_1(self):
        """Test create command on Place with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create Place city_id="{}" user_id="{}"\
            name="Holberton" description="Nice_house" number_rooms=10\
            number_bathrooms=3 max_guest=100 price_by_night=9000 latitude=0.0\
            longitude=9.9 I_DONT_EXIST=10'.format(self.c.id, self.u.id))
        id = f.getvalue()[:-1]

        self.tearDown()
        self.create_conn()
        self.cur.execute("SELECT * FROM places WHERE id = '{}'".format(id))
        rows = self.cur.fetchall()
        self.assertIsNotNone(rows)
        self.assertIn('Holberton', rows[0])
        self.assertNotIn('I_DONT_EXIST', rows[0])

    def test_create_review_0(self):
        """Test create command on Review with valid parameters."""
        self.cur.execute('SELECT COUNT(id) FROM reviews')
        o_count = self.cur.fetchall()

        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create Review text="Great" place_id="{}"\
                               user_id="{}"'.format(self.p.id, self.u.id))
        self.tearDown()
        self.create_conn()
        self.cur.execute('SELECT COUNT(id) FROM reviews')
        n_count = self.cur.fetchall()
        self.assertNotEqual(o_count, n_count)

    def test_create_review_1(self):
        """Test create command on Review with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create Review text="Great" place_id="{}"\
                               user_id="{}" nope=10'
                               .format(self.p.id, self.u.id))
        id = f.getvalue()[:-1]

        self.tearDown()
        self.create_conn()
        self.cur.execute("SELECT * FROM reviews WHERE id = '{}'".format(id))
        rows = self.cur.fetchall()
        self.assertIsNotNone(rows)
        self.assertIn('Great', rows[0])
        self.assertNotIn('nope', rows[0])

    def test_create_state_0(self):
        """Test create command on State with valid parameters."""
        self.cur.execute('SELECT COUNT(id) FROM states')
        o_count = self.cur.fetchall()

        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create State name="California"')

        self.tearDown()
        self.create_conn()
        self.cur.execute('SELECT COUNT(id) FROM states')
        n_count = self.cur.fetchall()
        self.assertNotEqual(o_count, n_count)

    def test_create_state_1(self):
        """Test create command on State with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create State name="Texas"\
            I_DONT_EXIST=10')
        id = f.getvalue()[:-1]

        self.tearDown()
        self.create_conn()
        self.cur.execute("SELECT * FROM states WHERE id = '{}'".format(id))
        rows = self.cur.fetchall()
        self.assertIsNotNone(rows)
        self.assertIn('Texas', rows[0])
        self.assertNotIn('I_DONT_EXIST', rows[0])

    def test_create_user_0(self):
        """Test create command on User with valid parameters."""
        self.cur.execute('SELECT COUNT(id) FROM users')
        o_count = self.cur.fetchall()

        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create User email="BettyHolberton@gmail.com"\
            password="not_encrypted" first_name="Betty"\
            last_name="Holberton"')

        self.tearDown()
        self.create_conn()
        self.cur.execute('SELECT COUNT(id) FROM users')
        n_count = self.cur.fetchall()
        self.assertNotEqual(o_count, n_count)

    def test_create_user_1(self):
        """Test create command on User with invalid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create User email="BettyHolberton@gmail.com"\
            password="not_encrypted" first_name="Betty"\
            last_name="Holberton" I_DONT_EXIST=10')
        id = f.getvalue()[:-1]

        self.tearDown()
        self.create_conn()
        self.cur.execute("SELECT * FROM users WHERE id = '{}'".format(id))
        rows = self.cur.fetchall()
        self.assertIsNotNone(rows)
        self.assertIn('BettyHolberton@gmail.com', rows[0])
        self.assertNotIn('I_DONT_EXIST', rows[0])


if __name__ == "__main__":
    unittest.main()
