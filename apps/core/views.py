from django.shortcuts import render


def index(request):
    return render(request, "landing/index.html")


def privacy(request):
    return render(request, "landing/privacy.html")


def healthz(request):
    from django.http import HttpResponse
    return HttpResponse("ok", content_type="text/plain")


def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)
