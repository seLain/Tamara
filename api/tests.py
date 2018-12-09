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

    @skip
    def test_get_fragments(self):
        # self.client.login
        # get and check
        pass

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
        # check by model
        self.assertEqual(TrainingFragment.objects.count(), 2)

    @skip
    def test_delete_fragments(self):
        # self.client.login
        # get framents
        # delete 1 fragment
        # check by model
        # delete multiple fragments
        # check by model
        pass

    @skip
    def test_update_fragments(self):
        pass


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
                        "text": "POST-1-Text",
                    }
                ]
            },
            format='json',
        )
        # check by model
        self.assertEqual(RequestFragment.objects.count(), 1)

    @skip
    def test_post_fragments(self):
        # self.client.login
        # send 1 fragment
        # check response
        # send multiple fragments
        # check response
        pass
