from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Setting
import views


class UserMethodTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.date = timezone.now().date()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        user = User.objects.create(username="test user")
        Setting.objects.create(user=user, preferred_hour=6)

    def tearDown(self):
        User.objects.get(username="test user").delete()

    def test_is_under_with_no_tasks(self):
        """
        is_under() should return True for no tasks
        """
        user = User.objects.get(username="test user")

        self.assertEqual(user.setting.is_under(self.date), True)

    def test_is_under_with_under_hours_of_tasks(self):
        """
        is_under() should return True for the sum of each task's hour
        is less than preferred_hour
        """
        user = User.objects.get(username="test user")

        user.task_set.create(user=user, date=self.date, hour=4)

        self.assertEqual(user.setting.is_under(self.date), True)

    def test_is_under_with_over_hours_of_tasks(self):
        """
        is_under() should return True for the sum of each task's hour
        is greater than preferred_hour
        """
        user = User.objects.get(username="test user")

        user.task_set.create(user=user, date=self.date, hour=4)
        user.task_set.create(user=user, date=self.date, hour=4)

        self.assertEqual(user.setting.is_under(self.date), False)

    def test_is_under_with_zero_preferred_hour(self):
        """
        is_under() should return False for preferred_hour is zero
        """
        user = User.objects.get(username="test user")
        Setting.objects.filter(pk=user).update(preferred_hour=0)
        user.refresh_from_db()

        self.assertEqual(user.setting.is_under(self.date), False)

    def test_is_under_with_equal_hours_of_tasks(self):
        """
        is_under() should return False for the sum of each task's hour
        equals to preferred_hour
        """
        user = User.objects.get(username="test user")

        user.task_set.create(user=user, date=self.date, hour=6)

        self.assertEqual(user.setting.is_under(self.date), False)


class ViewMethodTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.date = timezone.now().date()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        user = User.objects.create(username="test user")
        Setting.objects.create(user=user, preferred_hour=6)

    def tearDown(self):
        User.objects.get(username="test user").delete()

    def test_get_dates(self):
        """
        _get_dates should return 7 days
        """
        user = User.objects.get(username="test user")
        dates = views._get_dates(user, self.date)

        self.assertEqual(len(dates), 7)
        self.assertTrue(self.date in [dd['date'] for dd in dates])

    def test_get_tasks(self):
        """
        _get_tasks should return all tasks
        """
        user = User.objects.get(username="test user")
        tasks = views._get_tasks(user, self.date)
        self.assertEquals(len(tasks), 0)

        user.task_set.create(user=user, date=self.date, hour=6)
        tasks = views._get_tasks(user, self.date)
        self.assertEquals(len(tasks), 1)
