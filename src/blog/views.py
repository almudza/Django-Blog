from django.shortcuts import render, get_object_or_404

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView

# Create your views here.
from .models import Post, Comment

from .forms import EmailPostForm, CommentForm

from django.core.mail import send_mail

# Taggit view
from taggit.models import Tag

from django.db.models import Count





# list view
def post_list(request, tag_slug=None):
	object_list = Post.published.all()
	tag = None


	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])


	paginator = Paginator(object_list, 3) # 3 post in each page 
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# if page is not an integer deliver the first page
		posts = paginator.page(1)
	except EmptyPage:
		# if page is not of range deliver last_page of results
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


#view all post
# class PostListView(ListView):
# 	queryset = Post.published.all()
# 	context_object_name = 'posts'
# 	paginate_by = 3
# 	template_name = 'blog/post/list.html'




#view post detail
def post_detail(request, year, month, day, post) :
	post  = get_object_or_404(Post, slug=post, 
									status='published',
									publish__year= year,
									publish__month= month,
									publish__day= day)
	# list of active comments for this post
	comments = post.comments.filter(active=True)

	if request.method == 'POST':
	# A comment was posted
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			# Created Comment object but don't save to database yet

			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.post = post
			# Save the comment to the database
			new_comment.save()
	else:
		comment_form = CommentForm()

	# List similar posts
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

	return render(request, 
				'blog/post/detail.html', {'post': post, 'comments':comments, 'comment_form': comment_form, 'similar_posts': similar_posts})


# Email forms from forms.py

def post_share(request, post_id):
	# Retrieve post by id
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False

	if request.method == 'POST':
		# Form was submited
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# Form fields passed validation
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reeading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, 'alifulmudzakir@gmail.com', [cd['to']])
			sent = True
			# . . . send email
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
		