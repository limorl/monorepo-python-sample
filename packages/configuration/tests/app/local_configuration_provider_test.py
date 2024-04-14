import os
import unittest
from configuration.app.local_configuration_provider import  LocalConfigurationProvider


class TestLocalConfigurationProvider(unittest.TestCase):
    def setUp(self):
        os.environ['LOCAL_CONFIGURATION_FOLDER'] = os.path.join(os.getcwd(), 'tests/config')

    def test_get_raw_configuration(self):
        config_provider = LocalConfigurationProvider()
        config_provider.init_configuration()
        val1 = config_provider.get_configuration('raw1')
        val2 = config_provider.get_configuration('raw2')

        self.assertEqual(val1, 1)
        self.assertEqual(val2, 2)

    def test_get_configuration_section(self):
        config_provider = LocalConfigurationProvider()
        config_provider.init_configuration()
        config1 = config_provider.get_configuration('section1')
        config10 = config_provider.get_configuration('section10')

        self.assertEqual(config1['num1'], 1)
        self.assertEqual(config1['str1'], 'val1')
        self.assertEqual(config10['num10'], 10)
        self.assertEqual(config10['str10'], 'val10')


if __name__ == '__main__':
    unittest.main()
