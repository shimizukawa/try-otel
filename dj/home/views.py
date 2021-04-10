from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


@login_required
def user_home(request):
    user = request.user
    context = {'name': user.email}
    return render(request, 'user_home.html', context)
