"""
Name : Bobby Mitchell
Date Created: 3 September 2023
Applicaiton Name : Atomic habits
Description : A webpage to track what type of habits someone has and whether they 
deem the habit postive negative or neutral

based on James Clears atomic habits
 for more information on Atomic Habits -> https://jamesclear.com/


"""

from django import forms



from .models import ScoreCard,ScoreCardTitle

class ScoreCardForm(forms.ModelForm):
    required_css_class = 'required-css'
    class Meta:
        model = ScoreCard
        fields = ['name','description']
        
       
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        self.fields['name'].widget.attrs.update({'class':'form-control ',"placeholder":"Scorecard Title" })
        self.fields['description'].widget.attrs.update({'class':'form-control',"placeholder":"Scorecard Description","rows":4})


class ScoreCardTitleForm(forms.ModelForm):
    class Meta:
        model = ScoreCardTitle
        fields = ['name','options']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-control',"placeholder":"Daily Habit"})
        self.fields['options'].widget.attrs.update({'class':'form-check '})

