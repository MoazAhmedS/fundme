from rest_framework import serializers
from ..models import Report, ReportComment, ReportProject


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"

class ReportCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportComment
        fields = "__all__"


class ReportProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportProject
        fields = "__all__"

