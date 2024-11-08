from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        # Validate file type if needed
        if not value.name.endswith(('.csv', '.xlsx')):
            raise serializers.ValidationError("Only CSV and Excel files are supported.")
        return value
