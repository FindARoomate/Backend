from django.db.models import TextChoices


class Gender(TextChoices):

    MALE = "MALE"
    FEMALE = "FEMALE"
   

class Personality(TextChoices):

    INTROVERT = "INTROVERT"
    EXTROVERT = "EXTROVERT"
    OTHERS = "DON'T MIND"

class Religion(TextChoices):

    ISLAM = "ISLAM"
    CHRISTIANITY = "CHRISTIANITY"
    OTHERS = "DON'T MIND"
