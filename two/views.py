from django.shortcuts import render , get_object_or_404,redirect
from django.utils import timezone
from two.models import Post,Comment
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from two.forms import CommentForm,PostForm
from django.http import HttpResponseRedirect


class AboutView(TemplateView):
    template_name = 'two/about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'two/post_detail.html'
    form_class = PostForm
    model = Post



class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'two/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')




class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'tow/post_list.html'
    model = Post

    template_name = "two/post_draft_list.html"

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


#######################################
#######################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    #return redirect('post_detail',pk=pk)
    return HttpResponseRedirect(reverse('post_detail',kwargs={'pk':pk}))








def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'GET':
        form = CommentForm(request.GET)
        if form.is_valid():
            Comment = form.save(commit=False)
            Comment.post= post
            Comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form =CommentForm()
    return render(request,'two/comment_form.html',{'form':form})




@login_required
def comment_approve(request,pk):
    comment= get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)




@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)