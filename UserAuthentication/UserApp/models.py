from django.db import models

class EvaluationRequest(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    object_details = models.TextField()
    contact_method = models.CharField(max_length=20, choices=[('phone', 'Phone'), ('email', 'Email')])
    photo = models.ImageField(upload_to='evaluation_photos/', null=True, blank=True)

    def _str_(self):
        return f'Request by {self.user.username}'