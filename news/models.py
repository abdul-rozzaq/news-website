from django.db import models



class News(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    body = models.TextField()
    
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    
    
    def __str__(self) -> str:
        return f"{self.user} : {self.title}"

