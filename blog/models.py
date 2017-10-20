from django.db import models

# Create your models here.

from datetime import date

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User  # Blog author or commenter


class BlogAuthor(models.Model):
    """
    Model representing a blogger.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='profile')
    #bio = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='profile'))
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True,default=date.today)
    email_confirmed = models.BooleanField(default=False)


    def get_absolute_url(self):
        """
        Returns the url to access a particular blog-author instance.
        """
        return reverse('blogs-by-author', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        if self.user is None:
            return 'User doesnt Exist !'
        else:
            return self.user.username



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        BlogAuthor.objects.create(user=instance)
    instance.profile.add()




class Blog(models.Model):
    """
    Model representing a blog post.
    """
    name = models.CharField(max_length=200)
    author = models.ForeignKey(BlogAuthor, on_delete=models.SET_NULL, null=True)
    category = models.CharField(max_length=50,default="Not Defined")
    # author = models.ForeignKey(User)
    # Foreign Key used because Blog can only have one author/User, but bloggsers can have multiple blog posts.
    description = models.TextField( help_text="Enter you blog text here.",)
    post_date = models.DateField(default=date.today)
    othercontributors=models.ManyToManyField(BlogAuthor, related_name='+',)

    def __str__(self):
        return self.othercontributors

    class Meta:
        ordering = ["-post_date"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog instance.
        """
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class BlogComment(models.Model):
    """
    Model representing a comment against a blog post.
    """
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because BlogComment can only have one author/User, but users can have multiple comments
    post_date = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        ordering = ["post_date"]

    def __str__(self):
        """
        String for representing the Model object.
        """
        len_title = 75
        if len(self.description) > len_title:
            titlestring = self.description[:len_title] + '...'
        else:
            titlestring = self.description
        return titlestring
