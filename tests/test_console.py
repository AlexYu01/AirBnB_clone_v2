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

    @unittest.skip('Not updated to Table yet')
    def test_create_amenity_0(self):
        """Test create command on Amenity with valid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Amenity name=\"TV\"")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Amenity")
            self.assertIn('\'name\': \'TV\'', f.getvalue())

    @unittest.skip('Not updated to Table yet')
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

    @unittest.skip('Not updated to Table yet')
    def test_create_review_0(self):
        """Test create command on Review with valid parameters."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Review text=\"Great\"")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Review")
            self.assertIn('\'text\': \'Great\'', f.getvalue())

    @unittest.skip('Not updated to Table yet')
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

if __name__ == "__main__":
    unittest.main()
