from django.db import models

from django.conf import settings
from multiselectfield import MultiSelectField
from django.urls import reverse

# Create your models here.


class ScoreCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True,null=True)
    timestamp =models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    def get_absolute_url(self):
        return reverse("scorecard:detail", kwargs={'id':self.id})
    def get_hx_url(self):
        return reverse("scorecard:hx-detail", kwargs={'id':self.id})
        
    def get_edit_url(self):
        return reverse("scorecard:update", kwargs={'id':self.id})
    
    def get_scorecard_children(self):
        return self.scorecardtitle_set.all()
    
    def get_delete_url(self):
         return reverse("scorecard:delete", kwargs={'id':self.id})
class ScoreCardTitle(models.Model):
    MY_CHOICES = (
     ('Postive','Postive'),
     ('Negative','Negative'),
    ('Neutral','Neutral'))

    scorecard = models.ForeignKey(ScoreCard, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    options = MultiSelectField(choices=MY_CHOICES,max_choices=1,max_length=200,null=True)

    def get_absolute_url(self):
        return self.scorecard.get_absolute_url()
    def get_delete_url(self):
        kwargs = {
            "parent_id":self.scorecard.id,
            "id" : self.id
        }
        return reverse("scorecard:scorecard-delete", kwargs=kwargs)
    def get_hx_edit_url(self):
        kwargs = {
            "parent_id":self.scorecard.id,
            "id" : self.id
        }
        return reverse("scorecard:hx-scorecard-detail", kwargs=kwargs)