import logging
import random

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def home(request):
    users = User.objects.all()
    headers = request.headers
    logger.info("headers %r", headers, extra={"headers": headers})
    if random.random() < 0.1:
        raise RuntimeError('random error')
    return render(request, 'home.html', {'users': users, 'headers': headers})


@login_required
def user_home(request):
    user = request.user
    context = {'name': user.email}
    return render(request, 'user_home.html', context)
