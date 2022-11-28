from django.conf import settings
from django.db import models
from django.utils import timezone
from . import globalvalue as g
category = (
    (0,"指定なし"),
    (1,"マンガ"),
    (2,"文芸"),
    (3,"参考書"),
    (4,"実用書"),
    (5,"専門書"),
    (6,"雑誌"),
    (7,"絵本"),
)

# class Post(models.Model):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     text = models.TextField()
#     # bookimage = models.ImageField()
#     created_date = models.DateTimeField(default=timezone.now)
#     published_date = models.DateTimeField(blank=True, null=True)


#     def publish(self):
#         self.published_date = timezone.now()
#         self.save()

#     def __str__(self):
#         return self.title

class Bookshelf(models.Model):
    title = models.CharField(verbose_name="本棚タイトル", 
                             max_length=20)
    cat = models.PositiveIntegerField(
        verbose_name="カテゴリ",
        choices=category, default=0)
    name = models.CharField(verbose_name="制作者", 
                              max_length=30,default="ログインしているアカウント")
    
    def __str__(self):
        return self.title

class Book(models.Model):
    target = models.ForeignKey(
        Bookshelf, verbose_name='紐づく本棚',
        blank=True, null=True,
        on_delete=models.SET_NULL)
    title = models.CharField(verbose_name="本タイトル", 
                             max_length=100)
    isbn = models.CharField(verbose_name="ISBNコード", 
                             max_length=13)
    comment = models.CharField(verbose_name="コメント", 
                               blank=True, null=True, max_length=100)

    def __str__(self):
        return self.title

