import os
import tempfile
import unittest

from ubuntucleaner.settings.common import RawConfigSetting

config_content = """
[section1]
option1=value1
option2=value2
"""


class TestRawConfigSetting(unittest.TestCase):

    def setUp(self):
        fp = tempfile.NamedTemporaryFile(delete=False)
        fp.close()
        self.config_path = fp.name

    def tearDown(self):
        os.unlink(self.config_path)

    def test_base(self):
        fp = open(self.config_path, 'w')
        fp.write(config_content)
        fp.close()
        settings = RawConfigSetting(self.config_path)
        self.assertEqual(settings.sections(), ['section1'])
        self.assertEqual(settings.options('section1'), ['option1', 'option2'])
        self.assertEqual(settings.get_value('section1', 'option1'), 'value1')

    def test_set_value(self):
        settings = RawConfigSetting(self.config_path)
        settings.set_value('section2', 'option1', 'value1')
        self.assertEqual(settings.get_value('section2', 'option1'), 'value1')
