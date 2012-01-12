# encoding: utf-8
from django.db import models

class Order(models.Model):
    slug = models.SlugField()
    status = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode("Order number %d: %s"%(self.slug, self.status,))
