from django.db.models import TextChoices


class Gender(TextChoices):

    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHERS = "I_DON'T_MIND"


class Personality(TextChoices):

    INTROVERT = "INTROVERT"
    EXTROVERT = "EXTROVERT"
    OTHERS = "I_DON'T_MIND"


class Religion(TextChoices):

    ISLAM = "ISLAM"
    CHRISTIANITY = "CHRISTIANITY"
    OTHERS = "OTHERS"


class ConnectionStatus(TextChoices):

    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
