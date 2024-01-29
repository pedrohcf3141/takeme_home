from django.urls import reverse
from rest_framework import status
from datetime import datetime, timedelta
from pets.models import Species, Pet, PetOwner


def test_species_list_url_resolves_not_auth(client, db):
    response = client.get(
        reverse(
            "species-list",
        )
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_species_list_url_resolves_found_dog(api_client, species_dog):
    response = api_client.get(
        reverse(
            "species-list",
        )
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == species_dog.name

def test_species_list_url_resolves_found_dog_not_auth(client, species_dog):
    response = client.get(
        reverse(
            "species-list",
        )
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_species_get_url_resolves(api_client, species_dog):
    response = api_client.get(
        reverse(
            "species-detail",
            args=[species_dog.id],
        )
    )
    assert response.status_code == status.HTTP_200_OK


def test_species_get_url_resolves_not_auth(client, species_dog):
    response = client.get(
        reverse(
            "species-detail",
            args=[species_dog.id],
        )
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_species_create_url_resolves(api_client):
    data = {
        "name": "Cat",
    }
    response = api_client.post(reverse("species-list"), data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Cat"

def test_species_create_url_resolves_not_auth(client):
    data = {
        "name": "Cat",
    }
    response = client.post(reverse("species-list"), data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_species_url_resolves(api_client, species_dog):
    data = {
        "name": "Cat",
    }
    response = api_client.put(
        reverse(
            "species-detail",
            args=[species_dog.id],
        ),
        data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Cat"

def test_update_species_url_resolves_not_auth(client, species_dog):
    data = {
        "name": "Cat",
    }
    response = client.put(
        reverse(
            "species-detail",
            args=[species_dog.id],
        ),
        data,
        format="json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_species_url_resolves(api_client, species_dog):
    response = api_client.delete(
        reverse(
            "species-detail",
            args=[species_dog.id],
        )
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Species.objects.count() == 0

def test_delete_species_url_resolves_not_auth(client, species_dog):
    response = client.delete(
        reverse(
            "species-detail",
            args=[species_dog.id],
        )
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_pet_list_url_resolves(api_client, pet_dog):
    response = api_client.get(
        reverse(
            "pets-list",
        )
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == pet_dog.name

def test_pet_list_url_resolves_not_auth(client, db):
    response = client.get(
        reverse(
            "pets-list",
        )
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_pet_get_url_resolves(api_client, pet_dog):
    response = api_client.get(
        reverse(
            "pets-detail",
            args=[pet_dog.id],
        )
    )
    assert response.status_code == status.HTTP_200_OK


def test_pet_create_url_resolves_with_owner_with_birthday(
    api_client, species_dog, pet_owner
):
    birthday = datetime.now() - timedelta(days=365 * 2)

    data = {
        "name": "Mac",
        "species": species_dog.id,
        "has_birthday": True,
        "birthday": birthday.date(),
        "owner": pet_owner.id,
    }
    response = api_client.post(reverse("pets-list"), data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Mac"
    assert response.data["age"] == 2

def test_pet_create_url_resolves_with_owner_with_birthday_not_auth(
    client, species_dog, pet_owner
):

    birthday = datetime.now() - timedelta(days=365 * 2)

    data = {
        "name": "Mac",
        "species": species_dog.id,
        "has_birthday": True,
        "birthday": birthday.date(),
        "owner": pet_owner.id,
    }
    response = client.post(reverse("pets-list"), data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_pet_create_url_resolves_with_owner_without_birthday(
    api_client, species_dog, pet_owner
):
    data = {
        "name": "Mac",
        "species": species_dog.id,
        "has_birthday": False,
        "age": 7,
        "owner": pet_owner.id,
    }
    response = api_client.post(reverse("pets-list"), data, format="json")
    today = datetime.today().date()
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Mac"
    assert response.data["age"] == 7
    assert response.data["birthday"] == datetime(today.year - 7, 1, 1).date().strftime(
        "%Y-%m-%d"
    )

def test_update_pet_url_resolves(api_client, pet_dog):
    data = {
        "name": "Murphy",
        "birthday": pet_dog.birthday,
        "has_birthday": pet_dog.has_birthday,
        "species": pet_dog.species.id,
    }
    response = api_client.put(
        reverse(
            "pets-detail",
            args=[pet_dog.id],
        ),
        data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Murphy"


def test_partial_update_pet_url_resolves(api_client, pet_dog):
    data = {
        "name": "Murphy",
    }
    response = api_client.patch(
        reverse(
            "pets-detail",
            args=[pet_dog.id],
        ),
        data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Murphy"


def test_delete_pet_url_resolves(api_client, pet_dog):
    response = api_client.delete(
        reverse(
            "pets-detail",
            args=[pet_dog.id],
        )
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Pet.objects.count() == 0


def test_pet_owner_list_url_resolves(api_client, pet_owner):
    response = api_client.get(
        reverse(
            "pet-owners-list",
        )
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == pet_owner.name


def test_pet_owner_list_url_resolves_not_auth(client, db):
    response = client.get(
        reverse(
            "pet-owners-list",
        )
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_pet_owner_get_url_resolves(api_client, pet_owner):
    response = api_client.get(
        reverse(
            "pet-owners-detail",
            args=[pet_owner.id],
        )
    )
    assert response.status_code == status.HTTP_200_OK


def test_pet_owner_create_url_resolves(api_client):
    data = {
        "name": "Jerry",
        "email": "jerry@j.com",
    }
    response = api_client.post(reverse("pet-owners-list"), data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Jerry"
    assert response.data["email"] == "jerry@j.com"


def test_pet_owner_update_url_resolves(api_client, pet_owner):
    data = {
        "name": "Jerry",
        "email": pet_owner.email,
    }
    response = api_client.put(
        reverse(
            "pet-owners-detail",
            args=[pet_owner.id],
        ),
        data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Jerry"


def test_pet_owner_partial_update_url_resolves(api_client, pet_owner):
    data = {
        "name": "Jerry",
    }
    response = api_client.patch(
        reverse(
            "pet-owners-detail",
            args=[pet_owner.id],
        ),
        data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Jerry"


def test_pet_owner_delete_url_resolves(api_client, pet_owner):
    response = api_client.delete(
        reverse(
            "pet-owners-detail",
            args=[pet_owner.id],
        )
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert PetOwner.objects.count() == 0
