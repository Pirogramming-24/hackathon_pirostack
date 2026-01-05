from django.shortcuts import render
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