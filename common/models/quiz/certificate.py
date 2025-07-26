# common/models/certificate.py
import uuid
from django.db import models
from django.conf import settings
from common.models.quiz.quiz import Quiz
from common.models.quiz.pre_quiz_question import PreQuizQuestion
from common.models.quiz.pre_quiz_answer import PreQuizAnswer

class CertificateTemplate(models.Model):
    """
    Represents a reusable certificate template uploaded by a user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template_image = models.ImageField(upload_to='certificates/templates/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'certificate_template'
class GeneratedCertificate(models.Model):
    """
    Represents a personalized certificate generated for a user based on a template,
    quiz, and pre-quiz answer.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(CertificateTemplate, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    pre_quiz_question = models.ForeignKey(PreQuizQuestion, on_delete=models.CASCADE)
    pre_quiz_answer = models.ForeignKey(PreQuizAnswer, on_delete=models.CASCADE)
    
    # Text content drawn on the certificate 
    text_drawn = models.CharField(max_length=255)
    
    # Coordinates on the template where text is drawn
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    
    # The final image generated after drawing text on the template
    generated_image = models.ImageField(upload_to='certificates/generated/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'generated_certificate'