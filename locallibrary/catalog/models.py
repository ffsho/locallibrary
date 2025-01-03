from django.db import models

from django.urls import reverse
import uuid
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

from django.contrib.auth.models import User
from datetime import date
# Create your models here.



class Genre(models.Model):

    name = models.CharField(max_length=200, help_text="Введите жанр книги")

    def __str__(self) -> str:
        return self.name
    

class Language(models.Model):
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]



class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True)

    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN', max_length=13, help_text="13-ти символьный isbn код")
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр книги")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)


    def __str__(self) -> str:
        return self.title
    

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    

    def display_genre(self):
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')


    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)



class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

   
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    
    class Meta:
        ordering = ['last_name']


