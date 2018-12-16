from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import TagBase, TaggedItemBase, GenericTaggedItemBase
import math
import logging
from core.tfidf import tfidf

logger = logging.getLogger(__name__)


class Fragment(models.Model):

    label = models.CharField(max_length=256)
    text = models.TextField(max_length=4096)


class FragmentTag(TagBase):

    idf = models.DecimalField(max_digits=32, decimal_places=16, default=0)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class FragmentTagM2M(GenericTaggedItemBase):
    # M2M foreign keys
    tag = models.ForeignKey(
        'FragmentTag', on_delete=models.CASCADE, related_name="m2m_fragments")
    # accompanied data
    tf = models.DecimalField(max_digits=32, decimal_places=16, default=0)


class TrainingFragment(Fragment):

    tags = TaggableManager(through=FragmentTagM2M)
    contributor = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='training_fragments')

    def __str__(self):
        return '%s - %s - %s' % (self.label[0:20], self.contributor, self.text[0:30])


@receiver(post_save, sender=TrainingFragment)
def update_tag_idf(sender, instance, **kwargs):
    n = sender.objects.count() + 1
    for t in instance.tags.all():
        m = sender.objects.filter(tags__in=[t]).count()
        t.idf = math.log10(float(n)/m)
        t.save()
    # calling tfidf obj to update idf dataset
    tfidf.update_idf()


class RequestFragment(Fragment):

    tags = TaggableManager(through=FragmentTagM2M)
    sender = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='request_fragments')

    def __str__(self):
        return '%s - %s - %s' % (self.label[0:20], self.sender, self.text[0:30])
