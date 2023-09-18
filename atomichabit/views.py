from django.shortcuts import render
def home_view(request):

    return render(request, "scorecard/home-view.html")



def about_view(request):

    return render(request, "about.html")