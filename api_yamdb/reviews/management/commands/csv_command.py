# csv_command.py
import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import Category, Genre, Title, User, Review, Comment

DATA_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')

class Command(BaseCommand):
    help = 'Загрузка данных из CSV файлов'

    def handle(self, *args, **options):
        self.load_categories()
        self.load_genres()
        self.load_titles()

    def load_categories(self):
        file_path = os.path.join(DATA_DIR, 'category.csv')
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write(self.style.SUCCESS('Категории успешно загружены.'))

    def load_genres(self):
        file_path = os.path.join(DATA_DIR, 'genre.csv')
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write(self.style.SUCCESS('Жанры успешно загружены.'))

    def load_titles(self):
        file_path = os.path.join(DATA_DIR, 'titles.csv')
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category'],
                )
        self.stdout.write(self.style.SUCCESS('Произведения успешно загружены.'))

    def load_reviews(self):
        file_path = os.path.join(DATA_DIR, 'review.csv')
        with open(file_path, encoding='utf-8') as file:
            for row in csv.DictReader(file):
                author = User.objects.get(id=row['author'])
                Review.objects.get_or_create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=author,
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
        self.stdout.write(self.style.SUCCESS('Отзывы успешно загружены.'))

    def load_comments(self):
        file_path = os.path.join(DATA_DIR, 'comments.csv')
        with open(file_path, encoding='utf-8') as file:
            for row in csv.DictReader(file):
                author = User.objects.get(id=row['author'])
                Comment.objects.get_or_create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=author,
                    pub_date=row['pub_date'],
                )
        self.stdout.write(self.style.SUCCESS('Комментарии успешно загружены.'))

    def load_users(self):
        file_path = os.path.join(DATA_DIR, 'users.csv')
        with open(file_path, encoding='utf-8') as file:
            for row in csv.DictReader(file):
                User.objects.get_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
        self.stdout.write(self.style.SUCCESS('Пользователи успешно загружены.'))
