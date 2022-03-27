from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    category = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.category}"
        

class Author(models.Model):
    name = models.ForeignKey(User, related_name="name_author", on_delete=models.CASCADE)
    note = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='news/static/images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} : {self.note}"


class Reader(models.Model):
    name = models.ForeignKey(User, related_name="name_reader", on_delete=models.CASCADE)
    following = models.ManyToManyField(Author, related_name="following")

    def __str__(self):
        return f"{self.name}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name="author", on_delete=models.CASCADE)
    content = models.TextField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    published = models.BooleanField(default=False)
    

    class Meta:
        ordering = ['-created']


    def __str__(self):
        return f"{self.title} : {self.content} by {self.author.name} on {self.created}"

    def serialize(self):
        return { "article_id" : self.id,
                "content" : self.content 
                }
    