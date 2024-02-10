from django.contrib.auth.models import User
from django.db import models
from PIL import Image

class UserProfile(models.Model):
    avatar= models.ImageField(upload_to='profile_image/', null=True, blank=True)
    bio= models.TextField(max_length=500, blank=True)
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    profile_status= models.BooleanField(default=False)
    following = models.ManyToManyField('UserProfile', related_name='followers', blank=True)


    def __str__(self):
        return str(self.user.username)

    #resize image avatar
def save(self, *args, **kwargs):
    super(UserProfile, self).save(*args, **kwargs)

    img = Image.open(self.profile_pic.path)

    if img.height > 100 or img.width > 100:
        output_size = (100, 100)
        img.thumbnail(output_size)
        img.save(self.profile_pic.path)
