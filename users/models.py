import uuid
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.urls import reverse
from PIL import Image
class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(qs)
        print("#########")

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)
        print("#########")

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        print("#########")
        return available
        

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bgimage = models.ImageField(default='default.jpg', upload_to='bg_pics')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True,default=uuid.uuid1)
    forget_password_token= models.CharField(max_length=100)
    updated = models.DateTimeField( auto_now=True)
    created = models.DateTimeField( auto_now_add=True)
    objects = ProfileManager()
    def get_absolute_url(self):
        return reverse("profile-detail-view", kwargs={"slug": self.slug})
    
    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"    

    def get_friends(self):
        return self.friends.all()
    def get_friends2(self):
        return self.user.friends.all()
    def get_friends_no(self):
        return self.friends.all().count()
    
    def get_posts_no(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value=='Like':
                total_liked += 1
        return total_liked

    def get_likes_recieved_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked
    def save(self,*args,**kwargs):
        super().save(*args , **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)    
STATUS_CHOICES=(
    ('send',"send"),
    ('accepted','accepted')
)
class RelationshipManager(models.Manager):
    def invatations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs
    
class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices = STATUS_CHOICES)
    updated = models.DateTimeField( auto_now=True)
    created = models.DateTimeField( auto_now_add=True)
    objects = RelationshipManager()
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"