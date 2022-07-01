from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


@login_required
def project_detail(request, project_id):
    return HttpResponseRedirect(
        reverse("issue_list", kwargs={"project_id": project_id}) + "?status=0"
    )
