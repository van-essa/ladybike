from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post


class PostList(generic.ListView):
    """Post List"""
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = 'articles.html'
    paginate_by = 6


class PostDetail(View):
    """Post Detail"""
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'article_detail.html',
            {
                'post': post,
                'liked': liked
            },
        )


class PostLike(View):
    """Like post"""
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('article_detail', args=[slug]))
