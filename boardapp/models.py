from django.db import models

# Create your models here.

class BoardModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=50)
    sns_image = models.ImageField(upload_to='')#画像の保存場所を引数に指定する。何も設定しない場合：settings.pyで設定された場所に保存される
    good = models.IntegerField(null=True, blank=True, default=1)#データベースにnullのデータが入ってきてもいいようにする
    read = models.IntegerField(null=True, blank=True, default=1)#blank=Trueはfromで受け付けるときの処理　null=Trueの時にはつけるようにする
    readtext = models.TextField(null=True, blank=True, default='a')