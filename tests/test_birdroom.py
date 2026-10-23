"""Unit tests for the course project. Run: python -m unittest discover -s tests -v"""
import unittest
from unittest.mock import patch
from birdroom import Birdroom, Cage, Zebrafinch, Gouldianfinch, Budgerigar, Lovebird

class BirdTests(unittest.TestCase):
    def test_inheritance(self):
        self.assertEqual(Zebrafinch("Z1","01:01:2020",["Gray"]).get_food_type(),"Seeds")
        self.assertEqual(Lovebird("L1","01:01:2020",["Green"]).get_food_type(),"Corn")
    def test_invalid_birth(self):
        with self.assertRaises(ValueError):
            Zebrafinch("Z1","31:02:2020",["Gray"])
    def test_future_birth(self):
        with self.assertRaises(ValueError):
            Zebrafinch("Z1","01:01:2099",["Gray"])
    def test_comparisons(self):
        a=Zebrafinch("Z1","01:01:2020",["Gray"])
        b=Zebrafinch("Z2","01:01:2020",["Black","White"])
        self.assertEqual(a,b)
        self.assertLess(a,b)
    def test_nestbox(self):
        b=Lovebird("L1","01:01:2026",["Green"])
        self.assertEqual(b.find_nestbox(),[["*","*"],["*","*"]])
    def test_vocal_power(self):
        with patch("birdroom.randint",return_value=7):
            self.assertEqual(Budgerigar("B1","01:01:2020",["Blue"]).vocal_power,7)

class CageTests(unittest.TestCase):
    def test_add_and_duplicates(self):
        cage=Cage("C1",30,30,40,"Silver")
        bird=Zebrafinch("Z1","01:01:2020",["Gray"])
        self.assertTrue(cage.add_bird(bird))
        self.assertFalse(cage.add_bird(bird))
    def test_reject_species(self):
        cage=Cage("C1",60,60,60,"Black")
        cage.add_bird(Zebrafinch("Z1","01:01:2020",["Gray"]))
        self.assertFalse(cage.add_bird(Lovebird("L1","01:01:2020",["Green"])))
    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            Cage("C1",35,30,40,"White")

class RoomTests(unittest.TestCase):
    def test_collisions(self):
        room=Birdroom(2,2,2)
        a=Cage("C1",30,30,40,"White")
        b=Cage("C2",30,30,40,"Black")
        a.add_bird(Zebrafinch("Z1","01:01:2020",["Gray"]))
        b.add_bird(Zebrafinch("Z2","01:01:2020",["White"]))
        self.assertTrue(room.add_cage(a,0,0))
        self.assertFalse(room.add_cage(b,0.2,0))
        self.assertTrue(room.add_cage(b,0.3,0))
    def test_layout(self):
        room=Birdroom(2,2,2)
        cage=Cage("C1",30,30,40,"White")
        cage.add_bird(Zebrafinch("Z1","01:01:2020",["Gray"]))
        room.add_cage(cage,0,0)
        self.assertEqual(len(room.get_birdroom()),20)
        self.assertEqual(room.get_birdroom()[0][:3],"ZZZ")
    def test_strength(self):
        room=Birdroom(2,2,2)
        cage=Cage("C1",60,60,60,"White")
        with patch("birdroom.randint",return_value=5):
            cage.add_bird(Gouldianfinch("G1","01:01:2020",["Red"]))
        room.add_cage(cage,0,0)
        self.assertEqual(room.get_strength(),5)

if __name__=="__main__":
    unittest.main()
