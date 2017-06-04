from django.shortcuts import render, get_object_or_404

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
from .models import Post



#view all post
def post_list(request):
	object_list = Post.published.all()
	paginator = Paginator(object_list, 3) # 3 posts yang tampil perhalaman
	page = request.GET.get('page')
	try:
		posts= paginator.page(page)
	except PageNotAnInteger:
		# jika page is not integer deliver the first page
		posts = paginator.page(1)
	except EmptyPage:
		# if page is out of range deliver last page of results
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post/list.html', { 'page': page, 'posts': posts})



#view post detail
def post_detail(request, year, month, day, post) :
	post  = get_object_or_404(Post, slug=post, 
									status='published',
									publish__year= year,
									publish__month= month,
									publish__day= day)
	return render(request, 
				'blog/post/detail.html', {'post': post})
