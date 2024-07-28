import graphene
from graphene_django import DjangoObjectType
from .models import Book

class BookType(DjangoObjectType):
  class Meta:
    model = Book
    fields = "__all__"


# Query is like a get request
class Query(graphene.ObjectType):
  all_books = graphene.List(BookType) # becomes camel case (allBooks) when query
  book_by_title = graphene.Field(BookType, title=graphene.String(required=True))
  
  def resolve_all_books(root, info):
    # We can easily optimize query count in the resolve method
    return Book.objects.all()
  
  def resolve_book_by_title(root, info, title):
    try:
      return Book.objects.get(title=title)
    except Book.DoesNotExist:
      return None


class CreateBook(graphene.Mutation):
  class Arguments:
    # The input arguments for this mutation
    title = graphene.String()
    author = graphene.String()
    
  book = graphene.Field(BookType)
  
  def mutate(root, info, title, author):
    book = Book(title=title, author=author)
    book.save()
    return CreateBook(book=book)


class UpdateBook(graphene.Mutation):
  class Arguments:
    id = graphene.ID()
    title = graphene.String()
    author = graphene.String()
    
  book = graphene.Field(BookType)
  
  def mutate(root, info, id, title=None, author=None):
    book = Book.objects.get(id=id)
    if title is not None:
      book.title = title
    if author is not None:
      book.author = author
    book.save()
    return UpdateBook(book=book)
  

class DeleteBook(graphene.Mutation):
  class Arguments:
    id = graphene.ID()
    
  book = graphene.Field(BookType)
  
  def mutate(root, info, id):
    book = Book.objects.get(id=id)
    book.delete()
    return DeleteBook(book=book)


class Mutation(graphene.ObjectType):
  create_book = CreateBook.Field()
  update_book = UpdateBook.Field()
  delete_book = DeleteBook.Field()