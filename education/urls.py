from django.urls import path

from .views import *


urlpatterns = [
    # Notes Path
    path('notes/', NoteList.as_view(), name='notes'),
    path('create-note/', NoteCreate.as_view(), name='create-note'),
    path('update-note/<int:pk>/', NoteUpdate.as_view(), name='update-note'),
    path('delete-note/<int:pk>/', NoteDelete.as_view(), name='delete-note'),

    # YouTube Path
    path('udemy/', UdemyView, name='udemy'),

    # YouTube Path
    path('youtube/', YouTubeView, name='youtube'),

    # Books Path
    path('books/', BooksView, name='books'),

    # Dictionary Path
    path('dictionary/', DictionaryView, name='dictionary'),

    # Wiki Path
    path('wiki/', WikiView, name='wiki'),
]
