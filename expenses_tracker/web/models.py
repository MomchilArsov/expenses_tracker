from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

# Create your models here.
from django.utils.deconstruct import deconstructible

VALIDATE_ONLY_LETTERS_EXEPTION_MESSAGE = "Ensure this value contains only letters."


def validate_only_letters(value):
    if not value.isalpha():
        raise ValidationError(VALIDATE_ONLY_LETTERS_EXEPTION_MESSAGE)

@deconstructible  # ползваме тoзи деконструктор(декоратор) заради миграциите в базата. пази с какви стойности е извикан max_size в init-a и после ги подава същите. Така възпроизвежда същият обект. Не може да се направи просто с функция. Валидаторите, които са цласове трябва да има този декоратор. Грешката при миграция е can not serialise...., ако не се използва. Първите две функции!! долните две са за да не се харкодват мегабайтите и ерърмесиджа
class MaxFileSizeInMbValidator(): # правим го с клас, за да може неговата инстанция да се вика като метод. използва се '__call__' и __init__ и стойността се подава в инита!! __call__ етода ни позволява да извикаме инстанцията на класа като функция!!
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        filesize = value.file.size
        if filesize > self.__megabytes_to_bytes(self.max_size):
            raise ValidationError(self.__get_exception_message())

    @staticmethod                            # може и да не е статик, но никъде не ползваме селф и за това
    def __megabytes_to_bytes(value):
        return value * 1024 * 1024

    def __get_exception_message(self):
        return f'Max file size is {self.max_size:.2f} MB'


class Profile(models.Model):
    FIRST_NAME_MIN_LEN = 2
    FIRST_NAME_MAX_LEN = 15

    LAST_NAME_MIN_LEN = 2
    LAST_NAME_MAX_LEN = 15

    BUDGET_DEFAULT_VALUE = 0
    BUDGET_MIN_VALUE = 0

    IMAGE_MAX_SIZE_IN_MB = 5
    IMAGE_UPLOAD_TO_DIR = 'profiles/'

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LEN),
            validate_only_letters
        ),
    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LEN),
            validate_only_letters,
        ),
    )

    budget = models.FloatField(
        default=BUDGET_DEFAULT_VALUE,
        validators=(
            MinValueValidator(BUDGET_MIN_VALUE),
        )
    )

    image = models.ImageField(
        upload_to=IMAGE_UPLOAD_TO_DIR,
        null=True,
        blank=True,
        validators=(
            MaxFileSizeInMbValidator(IMAGE_MAX_SIZE_IN_MB),
        ),
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}' # това пропърти го ползваме в profile темплейта  за да поакзва името


class Expense(models.Model):
    TITLE_MAX_LEN = 30

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
    )

    price = models.FloatField()

    image = models.URLField(
        verbose_name='Link to image' # как да се покаже
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('title', 'price')

