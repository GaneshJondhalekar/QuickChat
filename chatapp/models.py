from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    email=models.CharField(max_length=100,blank=True,null=True)
    first_name=models.CharField(max_length=100,blank=True,null=True)
    last_name=models.CharField(max_length=100,blank=True,null=True)
    profile_pic=models.ImageField(upload_to='profile',blank=True,null=True)
    friends=models.ManyToManyField(User,blank=True,null=True,related_name='friends')

    def __str__(self):
        return self.email

class FriendRequest(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='requests')
    status=models.CharField(max_length=10,choices=(('ACCEPTED','Accepted'),('REJECTED','Rejected'),('PENDING','Pending')))

    def __str__(self):
        return f'{self.receiver} have friend request from {self.sender}'


class ChatMessage(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_messages')
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='received_messages')
    message=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    seen=models.BooleanField(default=False)

    def __str__(self):
        return f'message from {self.sender} to {self.receiver}'