import unittest
from greeting_service import GreetingService


class TestGreetingService(unittest.TestCase):

    def test_hello_with_zero_exclamations(self):
        greeting = GreetingService()

        msg = greeting.hello('John', 0)
        expected = 'Hello John'

        self.assertEqual(msg, expected)

    def test_hello_with_three_exclamations(self):
        greeting = GreetingService()

        msg = greeting.hello('John', 3)
        expected = 'Hello John!!!'

        self.assertEqual(msg, expected)

    def test_hello_with_empty_name_and_no_exclamations(self):
        greeting = GreetingService()

        msg = greeting.hello('')
        expected = 'Hello !'

        self.assertEqual(msg, expected)

    def test_dumpster_fire(self):
        greeting = GreetingService()

        msg = greeting.dumpsterFire('', 3)
        expected = " is in a dampster fire###"
        self.assertEqual(msg, expected)


if __name__ == '__main__':
    unittest.main()
