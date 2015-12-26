from django.test import TestCase
from django.test import Client

import json


class ApiScenarioTests(TestCase):
    def test_user_scenario(self):
        client = Client()

        # check me first
        response = client.get('/api/me/')
        self.assertContains(response, 'Logout')

        # login fails
        response = client.post('/api/login/', {'username': 'tester', 'password': 'tester'})
        self.assertContains(response, 'Wrong Username')

        # register a user
        response = client.post('/api/signup/', {'username': 'tester', 'password': 'tester'})
        self.assertContains(response, 'Success')

        # try login again and succeed
        response = client.post('/api/login/', {'username': 'tester', 'password': 'tester'})
        self.assertContains(response, 'Success')

        # try me again
        response = client.get('/api/me/')
        self.assertContains(response, 'Login')

        data = json.loads(response.content)
        self.assertEquals(data['user']['username'], 'tester')

        # get tasks, empty
        response = client.get('/api/get_tasks/')
        self.assertContains(response, 'Success')

        data = json.loads(response.content)
        self.assertEquals(len(data['tasks']), 0)

        # add a task
        response = client.post('/api/add_task/', {'note': 'TEST NOTE', 'date': '2015-01-01', 'hour': '1'})
        self.assertContains(response, 'Success')

        data = json.loads(response.content)
        self.assertEquals(len(data['tasks']), 1)
        self.assertEquals(data['tasks'][0]['note'], 'TEST NOTE')

        # get tasks on the proper date
        response = client.get('/api/get_tasks/', {'date': '2015-01-01'})
        self.assertContains(response, 'Success')

        data = json.loads(response.content)
        self.assertEquals(len(data['tasks']), 1)

        # get tasks on another date, empty
        response = client.get('/api/get_tasks/', {'date': '2015-01-02'})
        self.assertContains(response, 'Success')

        data = json.loads(response.content)
        self.assertEquals(len(data['tasks']), 0)

        # edit the task
        response = client.post('/api/update_task/',
                               {'task_id': '1', 'note': 'TEST NOTE Updated', 'date': '2015-01-01', 'hour': '1',
                                'action': 'Edit'})
        self.assertContains(response, 'Success')

        data = json.loads(response.content)
        self.assertEquals(len(data['tasks']), 1)
        self.assertEquals(data['tasks'][0]['note'], 'TEST NOTE Updated')

        # delete the task
        response = client.post('/api/update_task/',
                               {'task_id': '1', 'note': 'TEST NOTE Updated', 'date': '2015-01-01', 'hour': '1',
                                'action': 'Delete'})
        self.assertContains(response, 'Success')

        data = json.loads(response.content)
        self.assertEquals(len(data['tasks']), 0)
