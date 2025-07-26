# common/serializers/certificate_serializer.py
from rest_framework import serializers
from common.models.quiz.certificate import CertificateTemplate, GeneratedCertificate

class CertificateTemplateSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of CertificateTemplate,
    while keeping id, uploaded_by, and uploaded_at read-only.
    """
    class Meta:
        model = CertificateTemplate
        fields = '__all__'
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at']

class GeneratedCertificateSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of GeneratedCertificate,
    with id, generated_image, created_at, and user marked read-only.
    """
    class Meta:
        model = GeneratedCertificate
        fields = '__all__'
        read_only_fields = ['id', 'generated_image', 'created_at', 'user']
        