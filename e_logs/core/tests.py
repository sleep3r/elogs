from django.test import TestCase

from e_logs.core.models import Setting


class SettingTestCase(TestCase):
    def setUp(self):
        pass
        # load_database()

    def test_animals_can_speak(self):
        """Settings are saved and work correctly"""

        Setting["brackets_test"] = "brackets_val"
        self.assertEqual(Setting["brackets_test"], "brackets_val")

        Setting.set_value(name='set_test', value='set_val')
        self.assertEqual(Setting.get_value('set_test1'), 'set_val')

        with self.assertRaises(ValueError):
            a = Setting['sadfsda']