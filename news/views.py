from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .decorators import allowed_users
from .models import *
from .forms import NewArticle
from django.contrib import messages


def index(request):
    #Home page displays the only the latest 9 articles
    articles = Article.objects.filter(published=True)[:9]

    context = { 'articles': articles }
    return render(request, "news/index.html", context)


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "news/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "news/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "news/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user and also save him as a Reader
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            reader = Reader.objects.create(name=user)
            reader.save()
        except IntegrityError:
            return render(request, "news/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "news/register.html")


#If the request user is in 'authors' group, using POST method can create a new article with NewArticle form
@allowed_users(allowed_roles=['authors'])
def create(request):
    user = User.objects.get(username=request.user.username)
    author = Author.objects.get(name=user)

    if request.method == "POST":
        form = NewArticle(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            if request.user.is_staff:
                new.author = author
                new.published = False
                new.save()
            return redirect(f"profile/{author.name}")
    else:
        form = NewArticle() 

    context = { 'form': form }
    return render(request, "news/create.html", context)


def news_view(request):
    #Display all published articles
    article = Article.objects.filter(published=True)
    #Get the number of articles
    articlesNum = len(article)
    #Pagination
    paginator = Paginator(article,15)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    context = { 'articles': articles,
                'articlesNum': articlesNum,
                'title': f"All News" 
                }
    return render(request, "news/articles.html", context)


def article_view(request, title):
    article = Article.objects.get(title=title)
    is_mine = False

    #Allow the authenticated user to view the whole published article
    if request.user == article.author.name:
                is_mine = True

    if article.published == True:
        if request.user.is_authenticated:

            context = { 'article': article,
                        'is_mine': is_mine
                        }
            return render(request, "news/article.html", context)
        else:
            #If the user is not authenticated redirect him to login page
            return render(request, "news/login.html", {
                    "message": "Sign in to read the article!"
                })
    else:
        #Allow only staff users to view an unpublished article
        if request.user.is_staff:
            context = { 'article': article,
            'is_mine': is_mine }
            return render(request, "news/article.html", context)
        else:
            #If the article is not published, display an error message and redirect to home page
            messages.error(request, 'No permissions for this page!')
            articles = Article.objects.filter(published=True)[:9]
            context = { 'articles': articles }
            return render(request, "news/index.html", context)


def profile_view(request, username):
    profile_user = User.objects.get(username=username)

    #Display all published articles by a specific author
    if request.user.is_authenticated:
        author = Author.objects.get(name=profile_user)
        article = Article.objects.filter(author=author, published=True)

        #Get upublished articles
        unpublishedArticles = Article.objects.filter(author=author, published=False)
        #Get the number of articles
        articlesNum = len(article)

        paginator = Paginator(article,15)
        page_number = request.GET.get('page')
        articles = paginator.get_page(page_number)

        context = { 'articles': articles,
                    'articlesNum': articlesNum,
                    'profile_user': profile_user,
                    'current_user': request.user,
                    'unpublishedArticles': unpublishedArticles
                    }
        return render(request, "news/profile.html", context)


def search(request):
    #Using POST method get the given query and check through all the published articles
    #if the query contained in the title or in the content
    if request.method == "POST":
        query = request.POST.get("query")
        article = Article.objects.filter(Q(published=True) & (Q(title__icontains=query) | Q(content__icontains=query)))
        #Get the number of articles
        articlesNum = len(article)

    #Pagination
    paginator = Paginator(article,15)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    context = { 'articles': articles,
                'articlesNum': articlesNum,
                'title': f"Related News"
                }
    return render(request, "news/articles.html", context)


 #If the request user is in 'editors' or 'authors' group, via json can edit the article with id=id
@allowed_users(allowed_roles=['editors', 'authors'])
@csrf_exempt
def edit(request, id):
    article = Article.objects.get(id=id)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get('content') is not None:
            article.content = data['content']
        article.save()
        return JsonResponse({}, status=200)


 #If the request user is in 'editors' group, publish the article with id=id 
@allowed_users(allowed_roles=['editors'])
@csrf_exempt
def publish(request, id):
    article = Article.objects.get(id=id)

    if request.method == "GET":
        article.published = True
        article.save()
    
    return redirect ('unpublished')


 #If the request user is in 'editors' group, delete the article with id=id   
@allowed_users(allowed_roles=['editors'])
def delete(request, id):
    article = Article.objects.get(id=id)

    if request.method == "GET":
        article.delete()

    return redirect('all_news')


def category_view(request, category_id):
    #For every category get all the published articles
    article = Article.objects.filter(category=category_id, published=True)
    #Get the number of articles
    articlesNum = len(article)

    paginator = Paginator(article,15)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    context = { 'articles': articles,
                'articlesNum': articlesNum,
                'title': f"{Category.objects.get(id=category_id).category}"
                }
    return render(request, "news/articles.html", context)


def authors_view(request):
    #Display all the authors
    try: 
        if request.user.is_authenticated and not request.user.is_staff:
            user = User.objects.get(username=request.user.username)
            context = { 'authors': Author.objects.all(),
                        'reader': Reader.objects.get(name=user)
                        }
        else:
            context = { 'authors': Author.objects.all() }
        return render(request, "news/authors.html", context)
    except:
        return HttpResponseRedirect(reverse("authors"))


@login_required
def follow(request, username):
    #Get the Reader user and the Author
    reader_user = User.objects.get(username=request.user.username)
    reader = Reader.objects.get(name=reader_user)
    author_user = User.objects.get(username=username)
    author = Author.objects.get(name=author_user)
  
    if request.method == 'POST':
        #Check if the author is not in user's following list and add him. Otherwise remove him.
        if 'add' in request.POST:
            reader.following.add(author)
            reader.save()
        else:  
            reader.following.remove(author)
            reader.save()
        return redirect("authors")
    context = { 'authors': Author.objects.all(),
                'reader': reader }
    return render(request, "news/authors.html", context)
 

@login_required
def favorites(request):
    try:
        reader_user = User.objects.get(username=request.user.username)
        reader = Reader.objects.get(name=reader_user)
        #Get all following authors
        following = reader.following.all()
        #Get all published articles by authors in user's following list
        article = Article.objects.filter(author__in = following, published=True)
        #Get the number of articles
        articlesNum = len(article)

        #Pagination
        paginator = Paginator(article,15)
        page_number = request.GET.get('page')
        articles = paginator.get_page(page_number)

        context = { 'title': 'My Favorites',
                    'articlesNum': articlesNum,
                    'articles': articles
                    }
        return render(request, "news/articles.html", context)
    except:
        #Display an error message and redirect to home page if the user is not a Reader
        messages.error(request, 'No permissions for this page!')
        articles = Article.objects.filter(published=True)[:9]
        context = { 'articles': articles }
        return render(request, "news/index.html", context)
        

@allowed_users(allowed_roles=['editors'])
def unpublished(request):
    #Get all the unpublished articles
    article = Article.objects.filter(published=False)
    #Get the number of articles
    articlesNum = len(article)

    #Pagination
    paginator = Paginator(article,15)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    context = { 'title': 'Unpublished Articles',
                'articlesNum': articlesNum,
                'articles': articles
                }
    return render(request, "news/articles.html", context) 

