from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from .models import News
from .forms import NewsForm


def home_page(request):
    news_list = News.objects.filter(is_published=True).order_by("-created_at")
    
    return render(request, "index.html", {"news_list": news_list})


def detail_page(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    news_item.views_count += 1
    news_item.save()
    return render(request, "detail.html", {"news_item": news_item})


@login_required
def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.user = request.user
            news.save()
            return redirect("home_page")
    else:
        form = NewsForm()
    return render(request, "add_news.html", {"form": form})


@login_required
def edit_news(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    if request.user != news_item.user:
        return redirect("home_page")
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news_item)
        if form.is_valid():
            form.save()
            return redirect("detail_page", pk=news_item.pk)
    else:
        form = NewsForm(instance=news_item)
    return render(request, "edit_news.html", {"form": form})


@login_required
def delete_news(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    if request.user == news_item.user:
        news_item.delete()
    return redirect("home_page")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home_page")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home_page")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home_page")


