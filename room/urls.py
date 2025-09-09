from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_room, name='create_room'),
    path('update/<int:room_id>/', views.update_room, name='update_room'),
    path("search/", views.search_rooms, name="search_rooms"),
    #We can also search rooms by room type and number of rooms
    #GET http://127.0.0.1:8000/rooms/search/?room_type=deluxe
    #GET http://127.0.0.1:8000/rooms/search/?number=101
]