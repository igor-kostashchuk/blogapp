from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .forms import BlogEntryForm
from .models import BlogEntry, Category



# Create your views here.
def index(request):
    posts = BlogEntry.objects.order_by("-created_at").all()
    top_rated_posts = BlogEntry.objects.order_by("-rating").all()

    if request.method == "POST":
        email = request.POST.get("email")
        print(email)
        if email:
            user = User.objects.filter(email=email).first()
            if not user:
                return redirect("registration")
            profile = user.profile
            profile.newsletter_subscription = True
            profile.save()

            messages.success(request, "Subscription created successfully!")
            return redirect("home")
        else:
            return redirect("registration")

    return render(request, "index.html", context={"posts": posts, "top_rated_posts": top_rated_posts})


@login_required
def create_blog(request):
    from django.template.loader import render_to_string
    from users.views import send_email
    from users.models import Profile
    from django.urls import reverse
    form = BlogEntryForm()
    if request.method == "POST":
        form = BlogEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()

            absolute_url = request.build_absolute_uri(
                reverse("blog_details", kwargs={"blog_id": entry.id})
            )
            html_message = render_to_string(
                "new_blog_entry.html",
                context={"post": entry, "absolute_url": absolute_url},
            )

            subscribers = Profile.objects.filter(newsletter_subscription=True)
            recipient_list = [sub.user.email for sub in subscribers if sub.user.email]
            if recipient_list:
                send_email(request,
                    "BlogApp: A new post you might be interested in!",
                    f"New post: {entry.title}",
                    html_message,
                    recipient_list,
                )
            
            messages.success(request, "Blog entry created successfully!")
            form = BlogEntryForm()
            
    return render(request, "create_blog.html", {"form": form })

def blog_list(request):
    sort = request.GET.get("sort", "date")  # за замовчуванням - по даті

    if sort == "rating":
        posts = BlogEntry.objects.all().order_by("-average_rating")  # сортування за рейтингом
    else:
        posts = BlogEntry.objects.all().order_by("-created_at")  # сортування за датою

    return render(request, "blog_list.html", {"posts": posts, "sort": sort})

def all_blog_entries(request):
    category_name = request.GET.get("category")
    print("filter_category", category_name)
    if category_name:
        posts = (
            BlogEntry.objects.filter(category__title=category_name)
            .order_by("-created_at")
            .all()
        )
    else:
        posts = BlogEntry.objects.order_by("-created_at").all()

    categories = Category.objects.all()
    return render(
        request, "blog_list.html", context={"posts": posts, "categories": categories}
    )

@login_required
def blog_details(request, blog_id):
    from .forms import CommentForm
    from django.db.models import Avg
    post = get_object_or_404(BlogEntry, id=blog_id)
    categories = Category.objects.all()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog_entry = post
            comment.user = request.user
            comment.save()
            post.rating = post.comments.aggregate(Avg("stars"))["stars__avg"]
            post.save()
            comment_form = CommentForm()  # Reset the form after saving
    else:
        comment_form = CommentForm()

    


    # Get recommended posts from the same category, excluding the current one
    recommended_posts = (
        BlogEntry.objects.filter(category=post.category)
        .exclude(id=post.id)
        .order_by("-created_at")[:4]
    )
    is_post_saved = post.savers.filter(user = request.user).exists()

    return render(
        request,
        "blog_details.html",
        context={
            "post": post,
            "categories": categories,
            "is_post_saved": is_post_saved,
            "recommended_posts": recommended_posts,
            "form": comment_form,
            "comments": post.comments.all(),
        },
    )

@login_required
def delete_blog_entry(request, blog_id):
    """
    Deletes a blog entry if the request user is the owner.
    """
    post = get_object_or_404(BlogEntry, id=blog_id)
    if post.user != request.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect("home")

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
    
    return redirect("profile/")
@login_required
def update_blog_entry(request, blog_id):
    from .forms import BlogEntryForm
    from django.shortcuts import get_object_or_404, redirect
    from .models import BlogEntry
    from django.contrib import messages

    post = get_object_or_404(BlogEntry, id=blog_id)
    if request.user != post.user:
        messages.error("You don't have permissions to edit this blog entry!")
        return redirect("home")

    if request.method == "POST":
        form = BlogEntryForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog entry updated successfully!")
            return redirect("blog_details", blog_id=post.id)
    else:
        form = BlogEntryForm(instance=post)

    return render(request, "create_blog.html", {"form": form, "title": "Update Blog Entry", "update_blog_entry": True})