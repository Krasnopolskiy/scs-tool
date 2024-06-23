from rest_framework import serializers

from backend.contracts import models


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    reports = ReportSerializer(many=True, read_only=True)

    class Meta:
        model = models.Contract
        fields = "__all__"
        read_only_fields = ("address", "source")
