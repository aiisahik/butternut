from django.shortcuts import render
from django.views.generic.base import TemplateView, View


class AccountView(TemplateView):
    template_name = 'base/_base.html'
    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        return response

    def get_context_data(self, **kwargs):
    	context = {}
    	return context


# Create your views here.
