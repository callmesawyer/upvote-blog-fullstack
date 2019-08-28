from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, full_name=None):
        user = self.model(username=username,
                          full_name=full_name,
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def by_group(self, group_name):
        try:
            group = Group.objects.get(name=group_name)
            return self.filter(group=group)
        except Group.DoesNotExist:
            return False

    def create_superuser(self, username, password=None, full_name=None):
        user = self.create_user(username,
                                password=password,
                                full_name=full_name,
                                )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    # objects = UserManager()




class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='authors')
    title = models.CharField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title) + '-----' + str(self.author)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Like(models.Model):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author) + '-----' + str(self.post.title)


class Comment(models.Model):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.text) + '-----' + str(self.author)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.post_id)])
