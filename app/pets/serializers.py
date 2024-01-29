# pets/serializers.py
from rest_framework import serializers
from pets.models import Species, Pet, PetOwner
from datetime import datetime


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"


class PetOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetOwner
        fields = "__all__"


class PetSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(required=False)

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "species",
            "has_birthday",
            "birthday",
            "age",
            "owner",
        ]
        read_only_fields = [
            "owner",
        ]

    def create(self, validated_data):
        has_birthday = validated_data.get("has_birthday", False)
        birthday = validated_data.get("birthday")
        age = validated_data.pop("age", None)
        if all([not has_birthday, not birthday, age]):
            today = datetime.today().date()
            birth_year = today.year - age
            birthday = datetime(birth_year, 1, 1).date()
            validated_data["birthday"] = birthday

        return super().create(validated_data)
