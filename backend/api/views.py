import logging

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from . import forms

logger = logging.getLogger(__name__)


def users(request):
    # TODO: attach GET parameter to span event
    logger.info("headers in view.users: %r", request.headers)

    users = [
        forms.UserForm(instance=u).initial
        for u in User.objects.all()
    ]
    logger.debug("response users: %r", users)

    return JsonResponse({"users": users})


def user_get(request, pk):
    # TODO: attach POST parameter to span event
    user = get_object_or_404(User, pk=pk)
    logger.info("target user: %r", user)

    form = forms.UserForm(request.POST, instance=user)
    if not form.is_valid():
        return JsonResponse({"error": form.errors}, status=400)

    logger.debug("Save data: %r", form.cleaned_data)
    form.save()

    return JsonResponse({})
