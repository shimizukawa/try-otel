from django.shortcuts import render


def home(request):
    context = {'name': 'OTEL'}
    return render(request, 'home.html', context)
