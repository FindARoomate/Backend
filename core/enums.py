from django.db.models import TextChoices


class Gender(TextChoices):

    MALE = "MALE"
    FEMALE = "FEMALE"


class Personality(TextChoices):

    INTROVERT = "INTROVERT"
    EXTROVERT = "EXTROVERT"


class Religion(TextChoices):

    ISLAM = "ISLAM"
    CHRISTIANITY = "CHRISTIANITY"

