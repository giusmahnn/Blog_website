from django.db import models
from django.conf import settings
from django.utils.text import slugify

from accounts.models import CustomUser

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)




class Post(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True) 
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    body = models.TextField()
    featured_image = models.ImageField(upload_to='featured_images/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    liked = models.ManyToManyField(CustomUser, blank=True, null=True, related_name='likes')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def num_likes(self):
        return self.liked.all().count()

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.BooleanField(default=False)

    def __str__(self):
        return str(self.post)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    # parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    # parents = models.ManyToManyField('self', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

'''
The slugify changes text like (hello world) to something like (hello-world or hello+world)
'''