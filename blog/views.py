from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login

# Create your views here.
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.views import generic

from blog.tokens import account_activation_token
from .models import Blog, BlogAuthor, BlogComment
from django.contrib.auth.models import User  # Blog author or commenter
from .forms import inputform, SignUpForm, editform


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[to_email])
            email.send()
            #user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return render(request, 'account_invalid.html')


def post_new(request):
    if request.method == "POST":
        form = inputform(data=request.POST)


        if form.is_valid():

                blog = form.save(commit=False)
                length=len((blog.description.split()))
                if length<10:
                    # form = inputform()
                # blog.author = request.user
                    my_p = BlogAuthor.objects.get(user=request.user)
                    blog.author = my_p
                    blog.post_date = timezone.now()
                    blog.save()
                    return redirect('blog-detail', pk=blog.pk)

    else:
        form = inputform()
    return render(request, 'blog/post_edit.html', {'form': form})


def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = editform(request.POST)
        if form.is_valid():
            #blog = form.save(commit=False)
            #blog.author = request.user
            #blog.podt_date = timezone.now()
            currentblogauthor= BlogAuthor.objects.get(user=request.user)
            if (currentblogauthor not in blog.othercontributors.all()) and (currentblogauthor != blog.author):
                contenttobeadded = form.cleaned_data['Edit']
                blog.description+=" "+contenttobeadded
                blog.save()


                if (currentblogauthor !=blog.author):
                    blog.othercontributors.add(currentblogauthor)
                return redirect('blog-detail', pk=blog.pk)
            else:
                return HttpResponse("you can't update further")

    else:
        form = editform()
    context={
      'blog':blog,
      'form' : form
    }
    return render(request, 'blog/editcontribute.html', context )


def index(request):
    """
    View function for home page of site.
    """

    # Render the HTML template index.html
    blog_list = Blog.objects.all()
    return render(
        request,
        'index.html',{'blog_list':blog_list}
    )


class BlogListView(generic.ListView):
    """
    Generic class-based view for a list of all blogs.
    """
    model = Blog
    paginate_by = 5


from django.shortcuts import get_object_or_404


class BlogListbyAuthorView(generic.ListView):
    """
    Generic class-based view for a list of blogs posted by a particular BlogAuthor.
    """
    model = Blog
    paginate_by = 5
    template_name = 'blog/blog_list_by_author.html'

    def get_queryset(self):
        """
        Return list of Blog objects created by BlogAuthor (author id specified in URL)
        """
        id = self.kwargs['pk']
        target_author = get_object_or_404(BlogAuthor, pk=id)
        return Blog.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        """
        Add BlogAuthor to context so they can be displayed in the template
        """
        # Call the base implementation first to get a context
        context = super(BlogListbyAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['blogger'] = get_object_or_404(BlogAuthor, pk=self.kwargs['pk'])
        return context


class BlogDetailView(generic.DetailView):
    """
    Generic class-based detail view for a blog.
    """
    model = Blog


class BloggerListView(generic.ListView):
    """
    Generic class-based view for a list of bloggers.
    """
    model = BlogAuthor
    paginate_by = 5


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse


class BlogCommentCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a blog comment. Requires login.
    """
    model = BlogComment
    fields = ['description', ]

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self):
        """
        After posting comment return to associated blog.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'], })
