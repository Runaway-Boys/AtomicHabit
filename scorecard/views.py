"""
Name : Bobby Mitchell
Date Created: 3 September 2023
Applicaiton Name : Atomic habits
Description : A webpage to track what type of habits someone has and whether they 
deem the habit postive negative or neutral

based on James Clears atomic habits
 for more information on Atomic Habits -> https://jamesclear.com/


"""




from django.shortcuts import redirect,render,get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse

from.forms import ScoreCardForm,ScoreCardTitleForm
from .models import ScoreCard,ScoreCardTitle
from django.db.models import Count
# Create your views here.


@login_required
def scorecard_list_view(request):
    """
    Produces a list of all the scorecards a specific
    user has created in the database
    """
    qs = ScoreCard.objects.filter(user=request.user) 
    """
    parameters
    ---------------------

    user=request.user -> filters the scorecards for only the user logged in scorecards

    --------------------
    """   
    context = {
        "object_list":qs,
    }
    return render(request, "scorecard/list.html",context)




@login_required
def scorecard_detail_view(request,id=None):
    """
    
    Shows the scorecard details ie,
    the scorecard desctiption what the daily habits are
    and whether they are positve negative or neutral
    can also update or delete these scorecards
    """
    hx_url = reverse("scorecard:hx-detail", kwargs={'id':id})   
    """
    when reverse link -> 
    parameters
    ------------------------
    "scorecard:hx-detail", kwargs={'id':id} -> 
    scorecard:hx-detail is the location,
    and the id of the scorecard page is  passed through
    ------------------------
    
    """

    context = {
        "hx_url":hx_url,
    }
    return render(request, "scorecard/detail.html",context)


@login_required
def scorecard_detail_hx_view(request,id=None):

    """
    when the page has been updated the user is redirected to the 
    hx view page
    """
    if not request.htmx:
        raise Http404
    try:
        obj =ScoreCard.objects.get(id=id,user=request.user)
    except:
        obj=None
    if obj is  None:
        return HttpResponse("not found")
    context = {
        "object":obj,
    }
    return render(request, "scorecard/partials/detail.html",context)





@login_required
def scorecard_create_view(request):
    """
    creating the scorecards
    making a form from the scorecard form

    """
    form = ScoreCardForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        obj = form.save(commit = False)
        """"
        parameter 
        ---------------
        commit = False -> 
        creating the form in memory but not to the database for it to be updated later

        ---------------
        """
        obj.user = request.user
        obj.save()
        if request.htmx:
            headers  = {
                "HX-Redirect" : obj.get_absolute_url()
            }
            return HttpResponse("created",headers=headers)
        return redirect(obj.get_absolute_url())
    return render(request, "scorecard/create-update.html",context)



@login_required
def scorecard_update_view(request,id=None):
    """
    if the user wants to update the scorecards

    """
    obj = get_object_or_404(ScoreCard,id=id,user=request.user)    
    form = ScoreCardForm(request.POST or None,instance=obj)
    new_scorecard_url = reverse('scorecard:hx-scorecard-create',kwargs={
        "parent_id":obj.id,
    })
    context = {
        'form':form,
        'new_scorecard_url':new_scorecard_url,
        "object":obj,
    }
    if form.is_valid():
        form.save()
    if request.htmx:
        return render(request,"scorecard/partials/forms.html",context)
    return render(request, "scorecard/create-update.html",context)


@login_required
def scorecard_children_update_hx_view(request,id=None,parent_id=None):

    """
    this function allows the user to update any previously added
    habits 
    
    """
    if not request.htmx:
        raise Http404
    try:
        parent_obj =ScoreCard.objects.get(id=parent_id,user=request.user)
    except:
        parent_obj=None
    if parent_obj is  None:
        return HttpResponse("not found")    
    instance = None
    if id is not None:
        try:
            instance = ScoreCardTitle.objects.get(scorecard=parent_obj,id=id)
        except:
            instance=None
    form = ScoreCardTitleForm(request.POST or None, instance=instance)
    url = reverse('scorecard:hx-scorecard-create',kwargs={
        "parent_id":parent_obj.id,
    })
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        'url':url,
        'form' :form,
        "object":instance,
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.scorecard = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "scorecard/partials/scorecard-inline.html",context)

    return render(request, "scorecard/partials/scorecard-form.html",context)


@login_required
def scorecard_delete_view(request,id=None):

    """
    deleting the scorecards
    """
    try:
        obj = ScoreCard.objects.get(id=id,user=request.user)
    except:
        obj =None
    if obj is None:
        if request.htmx:
            return HttpResponse("Not Found")
        raise Http404   
    if request.method =="POST":
        obj.delete()
        success_url = reverse('scorecard:list')
        if request.htmx:
            headers = {
                'HX-Redirect' : success_url
            }
            return HttpResponse("Success",headers=headers)
        return redirect(success_url)
    context = {
        "object":obj,
    }
    return render(request, "scorecard/delete.html",context)




@login_required
def scorecard_children_delete_view(request,id=None,parent_id=None):
    """
    Deleting any of the habits
    """
    try:
        obj = ScoreCardTitle.objects.get(
            scorecard__id = parent_id,
            id=id,
            scorecard__user=request.user
              )
    except:
        obj =None
    if obj is None:
        if request.htmx:
            return HttpResponse("Not Found")
        raise Http404   
    if request.method =="POST":
        name = obj.name
        obj.delete()
        success_url = reverse('scorecard:detail',kwargs={'id':parent_id})
        if request.htmx:
            return render(request, "scorecard/partials/scorecard-inline-delete.html",{'name':name})
        return redirect(success_url)
    context = {
        "object":obj,
    }
    return render(request, "scorecard/delete.html",context)


