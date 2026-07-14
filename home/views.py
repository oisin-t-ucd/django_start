from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name="home/about.html"

# Create your views here.
def index(request):
    """A view to return the index page"""

    return render(request, "index.html")
