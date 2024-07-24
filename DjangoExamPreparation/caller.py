import os
import django
from django.db.models import Q, Count, Avg, Max
from main_app.models import Author, Article, Review

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_email = Q(email__icontains=search_email)

    if search_name is not None and search_email is not None:
        query = query_name & query_email

    elif search_email is None:
        query = query_name

    else:
        query = query_email

    authors = Author.objects.filter(query).order_by('-full_name')
    result = []

    for a in authors:
        result.append(f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}")

    return '\n'.join(result)


def get_top_publisher():
    top_author = Author.objects.get_authors_by_article_count().first()

    if not top_author or top_author.num_articles == 0:
        return ""

    return f"Top Author: {top_author.full_name} with {top_author.num_articles} published articles."


def get_top_reviewer():
    author = Author.objects.annotate(num_reviews=Count('author_reviews')).order_by('-num_reviews', 'email').first()

    if not author or author.num_reviews == 0:
        return ""

    return f"Top Reviewer: {author.full_name} with {author.num_reviews} published reviews."


def get_latest_article():
    last_article = Article.objects.all().order_by('-published_on').first()

    if not last_article:
        return ""

    num_reviews = last_article.article_reviews.count()
    authors = ', '.join([a.full_name for a in last_article.authors.all().order_by('full_name')])
    average_rating = sum([r.rating for r in last_article.article_reviews.all()]) / num_reviews if num_reviews else 0.0

    return (f"The latest article is: {last_article.title}. Authors: {authors}. "
            f"Reviewed: {num_reviews} times. Average Rating: {average_rating:.2f}.")


def get_top_rated_article():
    best_article = Article.objects.annotate(avg_rating=Avg('article_reviews__rating')) \
        .order_by('-avg_rating', 'title') \
        .first()

    num_reviews = best_article.article_reviews.count()
    avg_rating = best_article.avg_rating

    if not best_article or num_reviews == 0:
        return ""

    return (f"The top-rated article is: {best_article.title}, with an average rating of {avg_rating:.2f}, "
            f"reviewed {num_reviews} times.")


def ban_author(email=None):
    author = Author.objects.prefetch_related('author_reviews').filter(email__exact=email).first()
    if email is None or author is None:
        return "No authors banned."

    num_reviews_deleted = author.author_reviews.count()

    author.is_banned = True
    author.save()
    author.author_reviews.all().delete()

    return f"Author: {author.full_name} is banned! {num_reviews_deleted} reviews deleted."

#def ban_author(email=None):
    #author = Author.objects.prefetch_related('author_reviews').filter(email__exact=email).first()

    #if email is None or not author:
        #return "No authors banned."

    #num_reviews = author.author_reviews.count()
    #author.is_banned = True
    #author.save()
    #author.author_reviews.all().delete()

    #return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."
# Create queries within functions
