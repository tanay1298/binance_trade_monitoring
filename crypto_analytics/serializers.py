from rest_framework import serializers

class LatestPriceSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    timestamp = serializers.DateTimeField()

class ErrorResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=False)
    message = serializers.CharField()

class HistoricalPriceSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

class StatisticalAnalysisSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    average_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    median_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    standard_deviation = serializers.DecimalField(max_digits=10, decimal_places=2)