from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps
from django.urls import reverse


class Profile(models.Model):
    '''
    Extension for User model. Include photo, subscription option and absolute_url
    user - link to standard User model
    photo - profile photo of user
    subscribed - if user subscribed to news
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users_photo/%Y/%m/%d/', blank=True, verbose_name='Фото')
    is_subscribed = models.BooleanField(default=True, verbose_name='В рассылке')
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk':self.user.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            # PIL rotates photo after thumbnail meth, 
            # if it was in album orientation
            # delete exif for cancel this
            img = ImageOps.exif_transpose(img)      
            if img.height > 250 or img.width > 250:
                new_img = (250, 250)
                img.thumbnail(new_img, resample=Image.Resampling.LANCZOS)
                img.save(self.photo.path)
