from django.db import models
from datetime import datetime


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Species(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PetOwner(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Pet(BaseModel):
    name = models.CharField(max_length=255)
    has_birthday = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(PetOwner, on_delete=models.CASCADE, null=True, blank=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def age(self):
        if self.birthday:
            today = datetime.today().date()
            age = (
                today.year
                - self.birthday.year
                - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            )
            return age
        return None
