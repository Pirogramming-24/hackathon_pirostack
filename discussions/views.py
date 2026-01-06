from django.shortcuts import render, redirect, get_object_or_404
from .models import DiscussionPost, DiscussionComment
from django.http import HttpResponseForbidden
from django.db.models import Q
from users.models import Profile


# Create your views here.
def get_current_profile(request):
    """세션에서 현재 프로필을 가져오는 헬퍼 함수"""
    # 미들웨어에서 추가한 프로필 객체가 있으면 우선 사용
    if getattr(request, "user_profile", None):
        return request.user_profile

    # 기존 세션 키(profile_id)와 현재 세션 키(user_id)를 모두 확인
    profile_id = request.session.get("user_id") or request.session.get("profile_id")
    if not profile_id:
        return None

    try:
        return Profile.objects.get(pk=profile_id)
    except Profile.DoesNotExist:
        return None


def post_list(request):
    sort = request.GET.get("sort", "latest")
    if sort == "oldest":
        posts = DiscussionPost.objects.order_by("created_at")
    else:
        posts = DiscussionPost.objects.order_by("-created_at")

    q = request.GET.get("q", "").strip()
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))

    return render(
        request,
        "discussions/post_list.html",
        {
            "posts": posts,
            "sort": sort,
            "q": q,
            "show_search_bar": not request.is_staff,
            "current_profile": get_current_profile(request),
        },
    )


def post_detail(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    comments = post.comments.order_by("created_at")

    current_profile = get_current_profile(request)

    return render(
        request,
        "discussions/post_detail.html",
        {"post": post, "comments": comments, "current_profile": current_profile},
    )


def post_create(request):
    profile = get_current_profile(request)

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        link = request.POST.get("link")
        image = request.FILES.get("image")

        DiscussionPost.objects.create(
            author=profile, title=title, content=content, link=link, image=image
        )
        return redirect("discussions:post_list")

    return render(request, "discussions/post_form.html")


def comment_create(request, post_id):
    profile = get_current_profile(request)

    post = get_object_or_404(DiscussionPost, id=post_id)
    if request.method == "POST":
        content = request.POST.get("content")

        DiscussionComment.objects.create(post=post, author=profile, content=content)
    return redirect("discussions:post_detail", post_id=post_id)


def post_edit(request, post_id):
    profile = get_current_profile(request)
    if not profile:
        return redirect("users:login")

    post = get_object_or_404(DiscussionPost, id=post_id)

    if post.author != profile:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.link = request.POST.get("link")
        if request.FILES.get("image"):
            post.image = request.FILES.get("image")
        post.save()
        return redirect("discussions:post_detail", post_id=post.id)
    return render(request, "discussions/post_form.html", {"post": post})


def post_delete(request, post_id):
    profile = get_current_profile(request)
    if not profile:
        return redirect("users:login")

    post = get_object_or_404(DiscussionPost, id=post_id)

    if post.author != profile:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    if request.method == "POST":
        post.delete()
    return redirect("discussions:post_list")


def comment_delete(request, comment_id):
    profile = get_current_profile(request)
    if not profile:
        return redirect("users:login")

    comment = get_object_or_404(DiscussionComment, id=comment_id)
    post_id = comment.post.id

    if comment.author != profile:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    if request.method == "POST":
        comment.delete()
    return redirect("discussions:post_detail", post_id=post_id)


def comment_edit(request, comment_id):
    profile = get_current_profile(request)
    if not profile:
        return redirect("users:login")

    comment = get_object_or_404(DiscussionComment, id=comment_id)
    post_id = comment.post.id

    if comment.author != profile:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == "POST":
        comment.content = request.POST.get("content")
        comment.save()
        return redirect("discussions:post_detail", post_id=post_id)

    return render(
        request,
        "discussions/comment_form.html",
        {"comment": comment, "post_id": post_id},
    )
