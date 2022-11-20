from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(default='default.jpg',upload_to="profile_images")

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, null=False)
    text = models.TextField(max_length=1000,null=False)
    commentors = models.ManyToManyField(User,related_name='commentors',blank=True)
    image = models.ImageField(upload_to="post-images",blank=True,null=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)
    text = models.TextField(max_length=200,null=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.text
    


class ProfileFollowing(models.Model):
    profile = models.ForeignKey(Profile,related_name='following',on_delete=models.CASCADE)
    follower = models.ForeignKey(Profile,related_name="followers",on_delete=models.CASCADE)

    def __str__(self):
        return self.follower.user.username
