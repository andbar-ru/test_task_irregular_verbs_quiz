from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Verb(models.Model): #{{{1
    base_form = models.CharField(primary_key=True, max_length=30)
    past_simple = models.CharField(max_length=30)
    past_participle = models.CharField(max_length=30)

#}}}

