from rest_framework import serializers
from .models import Task, FinancialRecord, RecurrentRecord

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
    
class FinancialRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = '__all__'

    
class RecurrentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurrentRecord
        fields = '__all__'
