from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Post, Group, Comment, Follow
from .forms import PostForm, CommentForm

User = get_user_model()


def index(request):
    post_list = Post.objects.select_related('author')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "index.html",
        {"page": page, "paginator": paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post = group.posts.all()
    paginator = Paginator(post, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  "group.html",
                  {"page": page, "paginator": paginator, "group": group}
                  )


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")
    return render(request, "new_post_form.html", {"form": form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()
    paginator = Paginator(post_list, 10)
    page_namber = request.GET.get('page')
    page = paginator.get_page(page_namber)
    follower = user.follower.all().count()
    following = user.following.all().count()
    return render(request, 'profile.html', {
        "page": page,
        "users": user,
        "paginator": paginator,
        "follower": follower,
        "following": following})


def post_view(request, username, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             author__username=username
                             )
    post_count = post.author.posts.all()
    comments = post.comments.all()
    follower = post.author.follower.all().count()
    following = post.author.following.all().count()
    form = CommentForm()
    return render(request,
                  'post.html',
                  {"post": post,
                   "post_count": post_count,
                   "form": form,
                   "comments": comments,
                   "follower": follower,
                   "following": following
                   }
                  )


def post_edit(request, username, post_id):
    post = get_object_or_404(Post.objects.select_related('author'),
                             id=post_id,
                             author__username=username
                             )
    if post.author != request.user:
        return redirect(reverse("post", args=[username, post_id]))
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post
                    )
    if form.is_valid():
        form.save()
        return redirect(reverse("post", args=[username, post_id]))
    return render(request, "edit_post_form.html",
                  {"form": form, "post": post}
                  )


def delete_post(request, username, post_id):
    post = get_object_or_404(Post.objects.select_related('author').filter(
        author__username=username, id=post_id))
    if post.author == request.user:
        post.delete()
    return redirect(reverse("profile", args=[post.author]))


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post.objects.select_related("author"),
                             id=post_id,
                             author__username=username
                             )
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.post = post
        form.save()
        return redirect(reverse("post", args=[username, post_id]))
    return redirect(reverse("post", args=[username, post_id]))


@login_required
def follow_index(request):
    post_list = Post.objects.select_related('author').filter(
        author__following__user=request.user
    )
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "follow.html",
        {"page": page, "paginator": paginator})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    user = Follow.objects.filter(user=request.user, author=author)
    if not user.exists() and request.user != author:
        Follow.objects.create(user=request.user, author=author)
        return redirect(reverse("profile", args=[username]))
    return redirect(reverse("profile", args=[username]))


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.filter(user=request.user, author=author).delete()
        return redirect(reverse("profile", args=[username]))
    return redirect(reverse("profile", args=[username]))
