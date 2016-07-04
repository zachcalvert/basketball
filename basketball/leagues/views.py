import json 

from django.core.urlresolvers import resolve, reverse, Resolver404
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, ListView


from leagues.models import Team, League
from leagues.utils import JSONView


# class SiteHomeView(JSONView):
#     def get(JSONView):


class LeagueView(JSONView):

    def get(self, request, league_id, *args, **kwargs):
        try:
			league = League.objects.get(id=league_id)
        except League.DoesNotExist:
            raise Http404()

        data = league.to_data()
        return data


class LeaguesListView(ListView):

    model = League


class TeamView(JSONView):

    def get(self, request, league_id, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            raise Http404()

        data = team.to_data(player_data=player_data)
        return data


class WebPageWrapperView(TemplateView):
    template_name = "leagues/page.html"
    context_object_name = "page"
    url_namespace = 'leagues.api_urls'

    def get_api_url(self, page_path, *args, **kwargs):
        return u"/" + page_path.strip('/') + u".json"

    def dispatch(self, request, *args, **kwargs):
        try:
            resolver_match = resolve(self.get_api_url(*args, **kwargs), self.url_namespace)
        except Resolver404:
            raise Http404

        request.META['HTTP_X_DHDEVICEOS'] = 'web'
        response = resolver_match.func(request, *resolver_match.args, **resolver_match.kwargs)
        if response.status_code >= 400:
            return response

        # working solution
        if isinstance(response, TemplateResponse):
            response.render()

        self.page_data = json.loads(response.content)
        return super(WebPageWrapperView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WebPageWrapperView, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.page_data
        return context



