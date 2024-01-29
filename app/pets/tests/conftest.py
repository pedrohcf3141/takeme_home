import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from pets.models import Species, Pet, PetOwner


@pytest.fixture
def api_client(db):
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpassword")
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def species_dog(db):
    return Species.objects.create(name="Dog")


@pytest.fixture
def pet_owner(db):
    return PetOwner.objects.create(name="Tom", email="tom@t.com")


@pytest.fixture
def pet_dog(species_dog, pet_owner):
    return Pet.objects.create(
        name="Mac",
        species=species_dog,
        has_birthday=True,
        birthday="2023-02-02",
        owner=pet_owner,
    )
