from django.db import models


class Contract(models.Model):
    address = models.CharField(max_length=42)
    source = models.TextField()


class Report(models.Model):
    class Analyzer(models.TextChoices):
        SEMGREP = "semgrep"
        OPENAI = "openai"
        MYTHRIL = "mythril"
        SLITHER = "slither"

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="reports")
    report = models.JSONField()
    analyzer = models.CharField(max_length=7, choices=Analyzer.choices)
