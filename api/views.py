import json

from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import TrainingFragment, RequestFragment
from api.serializers import (
    TrainingFragmentSerializer, RequestFragmentSerializer
)
from core.tfidf import tfidf


class TrainingFragmentViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    queryset = TrainingFragment.objects.all()
    serializer_class = TrainingFragmentSerializer

    '''
    request.data =
    {
        "fragments": [
            {
                "label": "POST-1",
                "text": "POST-1-Text",
                "tags": [
                    "POST-1-Tag-1", "POST-2-Tag-2"
                ]
            }
        ]
    }
    '''
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        ret = {}
        
        if request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)

        fragment_list = request.data.get('fragments', None)
        if not fragment_list:
            return Response('Need fragments data', status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if isinstance(fragment_list, str):
                fragment_list = json.loads(fragment_list)
        except json.JSONDecodeError:
            return Response(
                'Fragment list format error. Must be JSON serializable.',
                status=status.HTTP_400_BAD_REQUEST)

        try:
            collect_for_return = []
            if len(fragment_list) > 30:
                return Response('Max fragments: %s' % 30, status=status.HTTP_400_BAD_REQUEST)
            # [FIXME] Can not do bulk_create due to taggit. Need a way to get over it.
            for fragment in fragment_list:
                obj = TrainingFragment.objects.create(
                        label = fragment['label'],
                        text = fragment['text'],
                        contributor = request.user)
                for tag in fragment['tags']:
                    obj.tags.add(tag)
                obj.save()
                collect_for_return.append(obj.id)
        except KeyError:
            return Response(
                'Fragment list error. Some keys are missing.',
                status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                'Error saving fragments.',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # prepare returning data
        try:
            return_fragments = TrainingFragment.objects.filter(id__in=collect_for_return)
            serializer = self.get_serializer(return_fragments, many=True)
            ret = serializer.data
        except TrainingFragment.DoesNotExist:
            # [ToDo] logging
            pass

        return Response(ret)

    @transaction.atomic
    def destroy(self, request, pk, *args, **kwargs):
        
        if request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            TrainingFragment.objects.filter(id=pk, contributor=request.user).delete()
        except TrainingFragment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)


class RequestFragmentViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    queryset = RequestFragment.objects.all()
    serializer_class = RequestFragmentSerializer

    '''
    request.data =
    {
        "fragments": [
            {
                "label": "POST-1",
                "text": "POST-1-Text",
            }
        ]
    }
    '''
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        ret = {}
        
        if request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        fragment_list = request.data.get('fragments', None)
        if not fragment_list:
            return Response('Need fragments data', status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if isinstance(fragment_list, str):
                fragment_list = json.loads(fragment_list)
        except json.JSONDecodeError:
            return Response(
                'Fragment list format error. Must be JSON serializable.',
                status=status.HTTP_400_BAD_REQUEST)

        try:
            collect_for_return = []
            if len(fragment_list) > 10:
                return Response('Max fragments: %s' % 10, status=status.HTTP_400_BAD_REQUEST)
            # [FIXME] Can not do bulk_create due to taggit. Need a way to get over it.
            for fragment in fragment_list:
                obj = RequestFragment.objects.create(
                        label = fragment['label'],
                        text = fragment['text'],
                        sender = request.user)
                # compute tags here
                tags = tfidf.extract_tags(obj.text, topK=3, withWeight=False)
                for tag in tags:
                    obj.tags.add(tag)
                obj.save()
                collect_for_return.append(obj.id)
        except KeyError:
            return Response(
                'Fragment list error. Some keys are missing.',
                status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                'Error saving fragments.',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # prepare returning data
        try:
            return_fragments = RequestFragment.objects.filter(id__in=collect_for_return)
            serializer = self.get_serializer(return_fragments, many=True)
            ret = serializer.data
        except RequestFragment.DoesNotExist:
            # [ToDo] logging
            pass

        return Response(ret)
