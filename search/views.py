from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from scorecard.models import ScoreCard

SEARCH_TYPE_MAPPING = {
    'scorecard' : ScoreCard,
    'scorecards' : ScoreCard,
}
@login_required
def search_view(request):
    query = request.GET.get('q')
    search_type = request.GET.get('type')
    default_class = ScoreCard
    if search_type in SEARCH_TYPE_MAPPING.keys():
        default_class = SEARCH_TYPE_MAPPING[search_type]
    qs = default_class.objects.search(query=query)
    context = {
        'queryset':qs
    }
    template = "search/results-view.html"
    if request.htmx:
        context['queryset']= qs[:5]
        template = "search/partials/results.html"
    return render(request,template,context)
    