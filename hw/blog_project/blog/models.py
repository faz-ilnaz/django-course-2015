from django.db import models

class Post(models.Model):
    title = models.TextField()
    text = models.CharField(max_length=1000)
    p_date = models.DateTimeField()

    def __str__(self):
        return ":".join([self.title, self.text, str(self.p_date)])

