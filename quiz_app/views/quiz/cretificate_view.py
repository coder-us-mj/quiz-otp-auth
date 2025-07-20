from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from io import BytesIO

from common.models.quiz.certificate import CertificateTemplate, GeneratedCertificate
from common.models.quiz.pre_quiz_question import  PreQuizQuestion
from common.models.quiz.pre_quiz_answer import PreQuizAnswer
from common.models.quiz.quiz import Quiz
from common.serializers.certificate_serializer import CertificateTemplateSerializer
from common.response_handler import ResponseHandler  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_certificate_template(request):
    serializer = CertificateTemplateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(uploaded_by=request.user)
        return ResponseHandler.handle_200_success(serializer.data)
    return ResponseHandler.handle_400_error(serializer.errors)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_certificate(request):
    try:
        # Validate input
        required_fields = ['template_id', 'quiz_id', 'pre_quiz_question_id', 'pre_quiz_answer_id', 'x', 'y']
        for field in required_fields:
            if field not in request.data:
                return ResponseHandler.handle_400_error(f"{field} is required.")

        # Extract and fetch related objects
        template = get_object_or_404(CertificateTemplate, id=request.data['template_id'])
        quiz = get_object_or_404(Quiz, id=request.data['quiz_id'])
        pre_q = get_object_or_404(PreQuizQuestion, id=request.data['pre_quiz_question_id'])
        pre_a = get_object_or_404(PreQuizAnswer, id=request.data['pre_quiz_answer_id'])

        # Certificate generation
        image = Image.open(template.template_image)
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype("arial.ttf", 50) 
        x = int(request.data['x'])
        y = int(request.data['y'])
        text = pre_a.answer

        draw.text((x, y), text, font=font, fill='black')

        buffer = BytesIO()
        image.save(buffer, format='PNG')
        image_file = ContentFile(buffer.getvalue(), f'cert_{request.user.id}_{quiz.id}.png')

        # Save certificate record
        cert = GeneratedCertificate.objects.create(
            template=template,
            user=request.user,
            quiz=quiz,
            pre_quiz_question=pre_q,
            pre_quiz_answer=pre_a,
            text_drawn=text,
            position_x=x,
            position_y=y,
            generated_image=image_file
        )

        return ResponseHandler.handle_200_success({
            'message': 'Certificate generated successfully.',
            'certificate_id': str(cert.id)
        })

    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_certificate(request, certificate_id):
    certificate = get_object_or_404(GeneratedCertificate, id=certificate_id, user=request.user)
    return Response({
        "certificate_url": request.build_absolute_uri(certificate.generated_image.url)
    })