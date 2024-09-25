from rest_framework import serializers
from .models import ParsingRule


class ParsingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParsingRule
        fields = ['email_account', 'excel_column', 'db_column']