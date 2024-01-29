from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import SpeciesViewSet, PetViewSet, PetOwnerViewSet

router = DefaultRouter()
router.register(r"species", SpeciesViewSet, basename="species")
router.register(r"pets", PetViewSet, basename="pets")
router.register(r"pet-owners", PetOwnerViewSet, basename="pet-owners")

urlpatterns = [
    path("", include(router.urls)),
]
