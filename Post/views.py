import os

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Post
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required

ALLOWED_ATTACHMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.mp3', '.mp4'}


def _attachment_error(uploaded_file):
    if not uploaded_file:
        return None

    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext not in ALLOWED_ATTACHMENT_EXTENSIONS:
        return 'Only PDF, Word (.doc/.docx), MP3, and MP4 files are allowed.'

    return None


# Create your views here.

#Home view - index.html
def home(request, tag_slug=None):
    # Search logic
    query = request.GET.get("q")
    if query:
        # Filter by title containing the query (case-insensitive)
        posts = Post.objects.filter(status='published', title__icontains=query)
    else:
        # Default behavior: show latest 12 published posts
        posts = Post.objects.filter(status='published')[:12]
    
    post_count = Post.objects.count()
    user_count = User.objects.count()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # If searching within a tag, filter the already searched posts
        posts = posts.filter(tags__in=[tag])
    
    context = {
        "posts": posts, 
        "tag": tag, 
        "post_count": post_count, 
        "user_count": user_count,
        "query": query  # Pass query back to template to keep it in the search box
    }
    return render(request, "post/index.html", context)


#For post details
def detail(request, pk, slug):
    post = get_object_or_404(Post, id=pk, slug=slug)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(status='published', tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-published')[:4]

    attachment_ext = ''
    if post.attachment:
        attachment_ext = os.path.splitext(post.attachment.name)[1].lower()

    context = {"post": post, 'similar_posts': similar_posts, 'attachment_ext': attachment_ext}
    return render(request, "post/details.html", context)


#Create new blog-post
@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        detail = request.POST.get('detail')
        status = request.POST.get('status')
        
        # Force status to draft if user is not staff (Admin)
        if not request.user.is_staff:
            status = 'draft'
            
        attachment = request.FILES.get('attachment')

        error = _attachment_error(attachment)
        if error:
            return render(request, "post/create.html", {"error": error})

        if title and detail:
            p = Post.objects.create(
                title=title,
                slug=slug,
                detail=detail,
                status=status,
                author=request.user,
                attachment=attachment,
            )
            return redirect(p.get_absolute_url())
    return render(request, "post/create.html")

    
#Edit blog-post
@login_required
def edit(request, pk, slug):
    post = get_object_or_404(Post, id=pk, slug=slug)
    context = {'post': post}
    if request.method == "POST":
        title = request.POST.get('title')
        detail = request.POST.get('detail')
        status = request.POST.get('status')
        
        # Force status to draft if user is not staff (Admin)
        if not request.user.is_staff:
            status = 'draft'
            
        attachment = request.FILES.get('attachment')

        error = _attachment_error(attachment)
        if error:
            context['error'] = error
            return render(request, "post/edit.html", context)

        if title and detail:
            post.title = title
            post.detail = detail
            post.status = status
            if attachment:
                post.attachment = attachment
            post.save()
            return redirect(post.get_absolute_url())
        
    return render(request, "post/edit.html", context)


@login_required
def delete(request, pk, slug):
    post = get_object_or_404(Post, id=pk, slug=slug)
    context = {'post':post}
    if request.method == "POST":
        post.delete()
        return redirect("post:home")
        
    return render(request, "post/delete.html", context)


@login_required
def profile(request):
    drafts = request.user.posts.filter(status="draft")
    shouts = request.user.posts.filter(status="published")
    context = {"drafts":drafts, "shouts":shouts}

    return render(request, "post/profile.html", context)
