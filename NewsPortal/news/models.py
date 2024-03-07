from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    rating_author = models.IntegerField(default=0)
    user_link = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        posts_rating = self.post_set.aggregate(posts_sum_rating=Sum('rating_post'))
        posts_rating_result = 0
        posts_rating_result += posts_rating.get('posts_sum_rating')

        com_aut_rating = self.user_link.comment_set.aggregate(com_aut_sum=Sum('rating_comment'))
        com_aut_result = 0
        com_aut_result += com_aut_rating.get('com_aut_sum')

        com_post_result = 0
        posts_author = self.post_set.all()
        for i in posts_author:
            com_post_rating = i.comment_set.aggregate(com_post_sum=Sum('rating_comment'))
            com_post_result += com_post_rating.get('com_post_sum')

        self.rating_author = (3 * posts_rating_result) + com_aut_result + com_post_result
        self.save()
        pass


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):

    news = 'NE'
    article = 'AR'

    TYPE_CHOICE = [
        (news, 'Новость'),
        (article, 'Статья'),
    ]

    type_post = models.CharField(max_length=2, choices=TYPE_CHOICE, default=news)
    time_add = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=10000)
    rating_post = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField(max_length=1000)
    time_add = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()