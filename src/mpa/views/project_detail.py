from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


def project_detail(request, project_id):
    return HttpResponseRedirect(
        reverse("example_list", kwargs={"project_id": project_id})
    )
