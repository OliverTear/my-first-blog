from django.shortcuts import render
from django.utils import timezone
# from .models import Post
from django.shortcuts import get_object_or_404
from .forms import *
from django.shortcuts import redirect
from django.http import HttpResponse
import requests
from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, models, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpRequest, HttpResponseRedirect




# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})

# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})

# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         endpoint = "https://api.openbd.jp/v1/get"
#         headers= {
#         }
#         params={
#             "isbn":"9784061538290"
#         }
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             params["isbn"]=post.title
#             result = requests.get(endpoint, headers=headers, params=params)
#             res = result.json()
#             url = "https://cover.openbd.jp/"+post.title+".jpg"
#             # response = (requests.get(url))
#             # post.bookimage = response.content
#             post.title = res[0]["onix"]["DescriptiveDetail"]["TitleDetail"]["TitleElement"]["TitleText"]["content"]
#             post.published_date = timezone.now()
#             post.save()
#             print(url)
#             print("abc\n")
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})

def add_post(request):
    # Bookshelfが50件以上登録されていたら、古いものを1件削除
    tmp = Bookshelf.objects.all()
    if len(tmp) > 50:
        Book.objects.filter(target__exact=tmp[0].pk).all().delete()
        tmp[0].delete()

    form = BookshelfForm(request.POST or None)
    context = {'form': form,'username':request.user.username}
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        formset = BookFormset(request.POST, files=request.FILES, instance=post)
        if formset.is_valid():
            post.name = request.user
            post.save()
            formset.save()
            print(post.pk)
            return redirect('book_detail', post.pk)
        else:
            context['formset'] = formset
    else:
        context['formset'] = BookFormset()
    return render(request, 'blog/post_form.html', context)



def book_serch(request, key):
    url = "https://api.openbd.jp/v1/get?isbn=" + key
    html = requests.get(url)
    # 先頭と最後尾にカッコがついているので取って返却
    return HttpResponse(html.text[1:-1])

class BookList(ListView):
    model = Bookshelf
    template_name = 'blog/post_list.html'
    print(model)
    def get_queryset(self):
        return Bookshelf.objects.all().order_by("-pk")

def book_list(request: HttpRequest) -> HttpResponse:
    model = Bookshelf.objects.filter(name=request.user)
    return render(request, 'blog/post_list.html', {'username': request.user.username, 'book': model})


def book_detail(request, pk):
    bookshelf = Bookshelf.objects.get(pk=pk)
    books = Book.objects.filter(target__exact=pk).all()

    context = {'bookshelf': bookshelf,
               'books': books}
    return render(request, 'blog/post_detail.html', context)

def delete_post(request,pk):
    bookshelf = Bookshelf.objects.get(pk=pk)
    Bookshelf.objects.filter(pk=pk).all().delete()
    model = Bookshelf.objects.filter(name=request.user)
    return render(request, 'blog/post_list.html', {'username': request.user.username, 'book': model})

def top(request):
    return render(request, 'blog/post_list.html', {'username': request.user.username})

def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login/')

    # tasks = Bookshelf.objects.filter(name=request.user)
    model = Bookshelf.objects.filter(name=request.user)
    print("I am here!\n")
    return render(
        request,
        'blog/post_list.html',
        {'username': request.user.username, 'model': model}
    )



def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'blog/login.html')
    elif request.method != 'POST':
        raise Http404('Request method is not GET or POST.')

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        raise Http404('Username or password is not set.')

    user = authenticate(request, username=username, password=password)
    print(username)

    if user is None:
        return render(request, 'blog/login.html', {'error_message': 'Incorrect username or password.'})

    login(request, user)
    return HttpResponseRedirect('../list')


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect('../login/')

def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'blog/register.html')
    elif request.method != 'POST':
        raise Http404('Request method is not GET or POST.')

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError as e:
        raise Http404(e)

    try:
        user = models.User.objects.create_user(username=username, password=password)
    except IntegrityError as e:
        raise Http404(f'Username {username} is already registered. Please register another username.')

    login(request, user)
    return HttpResponseRedirect('../list')

def check_book_request(request: HttpRequest) -> None:
    if request.method != 'POST':
        raise Http404('Request method is not POST.')

    user=request.user
    if not user.is_authenticated:
        raise Http404('User is not authenticated.')



def bookshelf_update(request, pk):
    # bookshelf = Bookshelf.objects.get(pk=pk)
    # books = Book.objects.filter(target__exact=pk).all()
    # title = request.POST.get('title')
    # if title is None:
    #     Http404('Task id or name is not set.')
    # context = {'bookshelf': bookshelf,
    #            'books': books}
    # return render(request, 'blog/post_detail.html', context)
    # check_book_request(request=request)
    # books = Bookshelf.objects.get(pk=pk)
    # title = request.POST.get('title')
    # if title is None:
    #     Http404('Task id or name is not set.')
    #     post = get_object_or_404(Post, pk=pk)
    form = BookshelfForm(request.POST or None)
    if request.method == "POST"and form.is_valid():
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('book_detail', pk=post.pk)
        else:
            form =  BookshelfForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


