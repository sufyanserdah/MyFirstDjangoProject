from django.db import models
from django.urls import reverse
from django.utils import timezone
from users.models import Profile
from PIL import Image
from django.contrib.auth.models import User  
class Post(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post_image = models.ImageField(null=True, blank=True, upload_to="images/")
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    updated = models.DateTimeField( default = timezone.now)
    created = models.DateTimeField( default = timezone.now)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    def num_comments(self):
        return self.comment_set.all().count()
    def num_likes(self):
        print(timezone.now)
        return self.liked.all().count()    
    def get_absolute_url(self):
        return reverse("blog-home")
    def save(self):
        super().save()
        if Post.post_image == None:
            img = Image.open(self.post_image.path)
            if img.height > 300 or img.width>300:
                output_size=(300,300)
                img.thumbnail(output_size)
                img.save(self.post_image.path)
    class Meta:
        ordering = ('-created',)
class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    liked = models.ManyToManyField(Post, blank=True, related_name='likes')

    updated = models.DateTimeField(default = timezone.now )
    created = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.pk)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(default = timezone.now)
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

   