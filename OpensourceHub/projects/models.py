from email.policy import default
from tkinter.tix import Tree
from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Project(models.Model):
    owner=models.ForeignKey(Profile,null=True,on_delete=models.SET_NULL)
    title=models.CharField(max_length=200)
    featured_image=models.ImageField(default="",null=True, blank=True)
    description=models.TextField(null=True,blank=True)
    demo_link=models.CharField(max_length=2000, null=True, blank=True)
    source_link=models.CharField(max_length=2000, null=True, blank=True)
    tags=models.ManyToManyField("Tag", blank=True)
    vote_total=models.IntegerField(default=0,null=True,blank=True)
    vote_ratio=models.IntegerField(default=0,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.title

    @property
    def imageurl(self):
        try:
            img=self.featured_image.url
        except:
            img=""
        return img

class Review(models.Model):
    VOTE_TYPE=(
        ("up","Up_vote"),
        ("down","Down_vote"),
    )

    Project=models.ForeignKey(Project,on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    value=models.CharField(max_length=200,choices=VOTE_TYPE)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        self.value

class Tag(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
