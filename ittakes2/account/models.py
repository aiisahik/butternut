from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    dob = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "{0} - {1}".format(self.user.username, self.last_name)



# Create your models here.
