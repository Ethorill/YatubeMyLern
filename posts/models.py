from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import TextField

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50,
                            unique=True
                            )
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text: TextField = models.TextField()
    pub_date = models.DateTimeField('date published',
                                    auto_now_add=True
                                    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts'
                               )
    group = models.ForeignKey(Group,
                              related_name='posts',
                              blank=True, null=True,
                              on_delete=models.SET_NULL
                              )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']

    image = models.ImageField(upload_to='posts/',
                              blank=True,
                              null=True
                              )


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE,
                             )
    author = models.ForeignKey(User, related_name='comments',
                               on_delete=models.CASCADE
                               )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follower',
                             on_delete=models.CASCADE
                             )
    author = models.ForeignKey(User, related_name='following',
                               on_delete=models.CASCADE
                               )
