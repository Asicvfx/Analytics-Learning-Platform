from rest_framework import serializers

from .models import LearningMaterial


class LearningMaterialSerializer(serializers.ModelSerializer):
    dashboardId = serializers.IntegerField(source="dashboard_id", read_only=True)
    videoUrl = serializers.CharField(source="video_url", required=False,
                                     allow_blank=True)
    presentationUrl = serializers.CharField(source="presentation_url",
                                            required=False, allow_blank=True)
    faq = serializers.JSONField(source="faq_json", required=False)

    class Meta:
        model = LearningMaterial
        fields = ["id", "dashboardId", "title", "content", "videoUrl",
                  "presentationUrl", "faq"]
