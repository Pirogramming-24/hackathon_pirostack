from django.shortcuts import render, redirect, get_object_or_404
from .models import DiscussionPost
from django.contrib.auth import get_user_model # 임시
# from django.contrib.auth.decorators import login_required
User = get_user_model() # 임시

# Create your views here.
def post_list(request):
    sort = request.GET.get('sort','latest')
    if sort == 'oldest':
        posts = DiscussionPost.objects.order_by('created_at')
    else:
        posts = DiscussionPost.objects.order_by('-created_at')

    return render(request,'discussions/post_list.html',{
        'posts':posts,
        'sort':sort}
    )

def post_detail(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    return render(request,'discussions/post_detail.html',{'post':post})

# @login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        link = request.POST.get('link')
        image = request.FILES.get('image')

        DiscussionPost.objects.create(
            author=User.objects.first(), # 임시 -> author=request.user
            title=title,
            content=content,
            link=link,
            image=image
        )
        return redirect('discussions:post_list')
    
    return render(request,'discussions/post_form.html')