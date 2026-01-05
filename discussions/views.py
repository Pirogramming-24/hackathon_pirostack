from django.shortcuts import render, get_object_or_404
from .models import DiscussionPost

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