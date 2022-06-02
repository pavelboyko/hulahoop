from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


@login_required
def index(request):
    return HttpResponseRedirect(reverse("project_list"))
