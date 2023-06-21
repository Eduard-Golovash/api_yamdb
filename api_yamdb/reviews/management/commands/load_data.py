import os
import csv
from django.core.management.base import BaseCommand
from reviews.models import Category, Review, User, Title, Genre, Comment


class Command(BaseCommand):
    help = 'Загружаемые данные из CSV-файлов в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            type=str,
            help='Путь к директории содержащей CSV-файлы'
        )

    def handle(self, *args, **options):
        path = options['path']
        try:
            self.load_users(path)
            self.load_category(path)
            self.load_genre(path)
            self.load_titles(path)
            self.load_review(path)
            self.load_comments(path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"Ошибка при загрузке данных: {str(e)}"))

    def load_users(self, path):
        try:
            with open(os.path.join(path, 'users.csv'), encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    User.objects.create(
                        username=row['username'],
                        email=row['email'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        bio=row['bio'],
                        role=row['role'],
                    )
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING(f"Файл не найден"))
        except csv.Error as e:
            self.stdout.write(self.style.ERROR(
                f"Ошибка при чтении файла: {str(e)}"))

    def load_category(self, path):
        try:
            with open(os.path.join(path, 'category.csv')) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    Category.objects.create(
                        name=row['name'],
                        slug=row['slug'],
                    )
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING(f"Файл не найден"))
        except csv.Error as e:
            self.stdout.write(self.style.ERROR(
                f"Ошибка при чтении файла: {str(e)}"))

    def load_genre(self, path):
        try:
            with open(os.path.join(path, 'genre.csv')) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    Genre.objects.create(
                        name=row['name'],
                        slug=row['slug'],
                    )
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING(f"Файл не найден"))
        except csv.Error as e:
            self.stdout.write(self.style.ERROR(
                f"Ошибка при чтении файла: {str(e)}"))

    def load_titles(self, path):
        try:
            with open(os.path.join(path, 'titles.csv')) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    category = Category.objects.get(
                        name=row['category_name'])
                    Title.objects.create(
                        name=row['name'],
                        year=row['year'],
                        description=row['description'],
                        category=category
                    ).genre.set(row['genre_ids'].split(','))
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING(f"Файл не найден"))
        except csv.Error as e:
            self.stdout.write(self.style.ERROR(
                f"Ошибка при чтении файла: {str(e)}"))

    def load_review(self, path):
        try:
            with open(os.path.join(path, 'review.csv')) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    Review.objects.create(
                        title_id=row['title_id'],
                        text=row['text'],
                        author_id=row['author_id'],
                        score=row['score'],
                        pub_date=row['pub_date']
                    )
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING(f"Файл не найден"))
        except csv.Error as e:
            self.stdout.write(self.style.ERROR(
                f"Ошибка при чтении файла: {str(e)}"))

    def load_comments(self, path):
        try:
            with open(os.path.join(path, 'comments.csv')) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    Comment.objects.create(
                        author_id=row['author_id'],
                        review_id=row['review_id'],
                        text=row['text'],
                        pub_date=row['pub_date']
                    )
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING(f"Файл не найден"))
        except csv.Error as e:
            self.stdout.write(self.style.ERROR(
                f"Ошибка при чтении файла: {str(e)}"))