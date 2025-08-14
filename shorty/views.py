from django.db.models import F
from django.http import Http404
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import LinkForm
from .models import Link

def home(request):
    form = LinkForm(request.POST or None)
    short_url = None
    if request.method == "POST" and form.is_valid():
        link = form.save()
        short_url = request.build_absolute_uri(f"/{link.code}")
    recent = Link.objects.order_by("-created_at")[:5]
    return render(request, "shorty/home.html", {
        "form": form,
        "short_url": short_url,
        "recent": recent
    })

def redirect_short(request, code):
    link = get_object_or_404(Link, code=code)
    return redirect(link.long_url)

