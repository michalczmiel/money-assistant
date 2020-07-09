from rest_framework import serializers

from money_assistant.budgets.models import Budget, BudgetCategory


class BudgetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = (
            "id",
            "value",
            "category",
            "priority",
            "modified_at",
            "created_at",
        )


class BudgetSerializer(serializers.ModelSerializer):
    categories = BudgetCategorySerializer(many=True)

    class Meta:
        model = Budget
        fields = (
            "id",
            "name",
            "account",
            "categories",
            "start_time",
            "end_time",
            "modified_at",
            "created_at",
        )

    def create(self, validated_data: dict) -> Budget:
        budget_categories = validated_data.pop("categories")
        budget = Budget.objects.create(**validated_data)
        for budget_category in budget_categories:
            BudgetCategory.objects.create(budget=budget, **budget_category)
        return budget
