from django.shortcuts import render
from django.views.generic import View
from django.http import Http404, HttpResponseRedirect, HttpResponse
import simplejson
from models import calc_all_rankings


# Create your views here.
class MatchCalculatorView(View):
    def post(self, request, *args, **kwargs):
    	# calc = request.body('calc', None)
    	request_data = simplejson.loads(request.body)
    	success = False
    	if request_data.get('calc', None) == 'all': 
    		try: 
    			calc_all_rankings()
    			success = True
    		except: 
    			pass
    	context = {
    		'success': success
    	}
    	return HttpResponse(simplejson.dumps(context))