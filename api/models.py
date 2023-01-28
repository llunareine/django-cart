from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=False)
    password = models.TextField()
    items = models.ManyToManyField('Item', related_name='users')
    def __str__(self):
        return self.username

class Item(models.Model):
    item = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self):
        return f'{type(self).__name__}({self.item!r}, {self.item!r})'

