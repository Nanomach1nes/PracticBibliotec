  
from django.db import models
from apps.authors.models import Author
from apps.publishers.models import Publisher
from apps.genres.models import Genre

class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name="Издательство")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Жанр")
    publication_year = models.IntegerField(verbose_name="Год издания")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    pages = models.IntegerField(verbose_name="Количество страниц")
    description = models.TextField(blank=True, verbose_name="Описание")
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name="Обложка")
    total_copies = models.IntegerField(default=1, verbose_name="Всего экземпляров")
    available_copies = models.IntegerField(default=1, verbose_name="Доступно экземпляров")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"