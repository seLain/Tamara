from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class TrainingFragment(models.Model):

    label = models.CharField(max_length=256)
    text = models.TextField(max_length=4096)
    ground_tags = TaggableManager()
    contributor = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='training_fragments')

    def __str__(self):
        return '%s - %s - %s' % (self.label[0:20], self.contributor, self.text[0:30])
