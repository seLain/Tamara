import json
from unittest import skip
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from core.models import (
    TrainingFragment, RequestFragment
)


class TrainingFragmentAPITest(APITestCase):

    fixtures = ['admin.json']

    def test_post_one_fragment(self):
        # self.client.login
        logged_in = self.client.login(
            username='tamara-admin', password='admin-tamara')
        # add token to header
        token = Token.objects.get(user__username='tamara-admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # send 1 fragment
        response = self.client.post(
            path='/api/trainings/',
            data={
                "fragments": [
                    {
                        "label": "POST-1",
                        "text": "POST-1-Text",
                        "tags": ['tag1', 'tag2', 'tag3'],
                    }
                ]
            },
            format='json',
        )
        # check by model
        self.assertEqual(TrainingFragment.objects.count(), 1)

    def test_post_fragments(self):
        # self.client.login
        logged_in = self.client.login(
            username='tamara-admin', password='admin-tamara')
        # add token to header
        token = Token.objects.get(user__username='tamara-admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # send multiple fragments
        response = self.client.post(
            path='/api/trainings/',
            data={
                "fragments": [
                    {
                        "label": "POST-1",
                        "text": "POST-1-Text",
                        "tags": ['tag1', 'tag2', 'tag3'],
                    },
                    {
                        "label": "POST-2",
                        "text": "POST-2-Text",
                        "tags": ['tag3', 'tag4', 'tag5'],
                    }
                ]
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        # check by model
        self.assertEqual(TrainingFragment.objects.count(), 2)

    def test_get_fragments(self):
        # create fragments
        self.test_post_fragments()
        # self.client.login
        logged_in = self.client.login(
            username='tamara-admin', password='admin-tamara')
        # add token to header
        token = Token.objects.get(user__username='tamara-admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # send 1 fragment
        response = self.client.get(path='/api/trainings/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_delete_fragments(self):
        # create fragments
        self.test_post_fragments()
        # self.client.login
        logged_in = self.client.login(
            username='tamara-admin', password='admin-tamara')
        # add token to header
        token = Token.objects.get(user__username='tamara-admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # send 1 fragment
        response = self.client.get(path='/api/trainings/')
        results = response.json()['results']
        # delete one of them
        self.assertEqual(TrainingFragment.objects.count(), 2)
        response = self.client.delete(path='/api/trainings/%s/' % results[0]['id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TrainingFragment.objects.count(), 1)



class RequestFragmentAPITest(APITestCase):

    fixtures = ['admin.json']

    def test_post_one_fragment(self):
        # self.client.login
        logged_in = self.client.login(
            username='tamara-admin', password='admin-tamara')
        # add token to header
        token = Token.objects.get(user__username='tamara-admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # send 1 fragment
        response = self.client.post(
            path='/api/requests/',
            data={
                "fragments": [
                    {
                        "label": "POST-1",
                        "text": "SIMPLE is a strategy-based game for programming learning. Write down your strategy in defined programming language, control your workers then compete with your friends. The programming languages supported by SIMPLE are Python and Java.",
                    }
                ]
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        # check by model
        self.assertEqual(RequestFragment.objects.count(), 1)

    def test_post_fragments(self):
        # self.client.login
        logged_in = self.client.login(
            username='tamara-admin', password='admin-tamara')
        # add token to header
        token = Token.objects.get(user__username='tamara-admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # send 1 fragment
        response = self.client.post(
            path='/api/requests/',
            data={
                "fragments": [
                    {
                        "label": "POST-1",
                        "text": "SIMPLE is a strategy-based game for programming learning. Write down your strategy in defined programming language, control your workers then compete with your friends. The programming languages supported by SIMPLE are Python and Java.",
                    },
                    {
                        "label": "POST-2",
                        "text": "SIMPLE motivates students to practice programming skills via gaming. Players of SIMPLE write their strategies to control entities in the game. The specified actions of entities in strategies will gain or consume some scores.",
                    }
                ]
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        # check by model
        self.assertEqual(RequestFragment.objects.count(), 2)
