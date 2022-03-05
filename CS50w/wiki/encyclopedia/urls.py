from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    # st:entry means any string that we are going to give the variable entry to
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("new_page", views.create_new_page, name='new_page'),
    path("edit/<str:entry>", views.edit, name='edit'),
    path("random",views.random, name='random')
]
