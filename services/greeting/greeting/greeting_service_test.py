import unittest
from greeting_service import GreetingService


class TestGreetingService(unittest.TestCase):

    def test_hello_with_zero_exclamations(self):
        greeting = GreetingService()

        msg = greeting.hello("John", 0)
        expected = "Hello John"

        self.assertEqual(msg, expected)

    def test_hello_with_three_exclamations(self):
        greeting = GreetingService()

        msg = greeting.hello("John", 3)
        expected = "Hello John!!!"

        self.assertEqual(msg, expected)

    def test_hello_with_empty_name_and_no_exclamations(self):
        greeting = GreetingService()

        msg = greeting.hello("")
        expected = "Hello !"

        self.assertEqual(msg, expected)

    def test_dumpster_fire(self):
        greeting = GreetingService()

        msg = greeting.dumpsterFire("", 3)
        expected = "blabla !!!"
        self.assertEqual(msg, expected)

    def test_blabla(self):
        greeting = GreetingService()

        msg = greeting.blalba("John")
        expected = "blabla John!"

        self.assertEqual(msg, expected)

    def test_blabla_with_four_exclamations(self):
        greeting = GreetingService()

        msg = greeting.dumpsterFire("Yakov", 4)
        expected = "blabla Yakov!!!!"

        self.assertEqual(msg, expected)

    def test_hi_there_with_three_questionmarks(self):
        greeting = GreetingService()

        msg = greeting.hi_there("Jack", 3)
        expected = "hi Jack, how you doin' ???"

        self.assertEqual(msg, expected)



if __name__ == "__main__":

    unittest.main()
