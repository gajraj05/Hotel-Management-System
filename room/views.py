from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Room

# Create your views here.

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_room(request):
    user = request.user

    # ✅ Only admins/staff can create rooms
    if not user.role == "admin" or user.role == "Admin":
        return Response(
            {"error": "Only admins can create rooms"},
            status=status.HTTP_403_FORBIDDEN,
        )

    data = request.data
    try:
        room = Room.objects.create(
            number=data["number"],
            room_type=data.get("room_type", "single"),
            price=data.get("price", 1000.00),
            is_available=data.get("is_available", True),
            created_by=user,
        )

        return Response(
            {
                "message": "Room created successfully",
                "room": {
                    "id": room.id,
                    "number": room.number,
                    "room_type": room.room_type,
                    "price": str(room.price),
                    "is_available": room.is_available,
                },
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_room(request, room_id):
    # ✅ Only admins can update
    if request.user.role == "admin" or request.user.role == "Admin":
        room = get_object_or_404(Room, id=room_id)
        data = request.data

        # ✅ Update fields
        room.number = data.get("number", room.number)
        room.room_type = data.get("type", room.room_type)
        room.price = data.get("price", room.price)
        room.is_available = data.get("is_available", room.is_available)

        room.save()

        return Response({
            "message": "Room updated successfully",
            "room": {
                "id": room.id,
                "number": room.number,
                "type": room.room_type,
                "price": room.price,
                "is_available": room.is_available
            }
        })
    else:
        return Response({"error": "Only admin can update rooms"}, status=403)
    

# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Room

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_rooms(request):
    user = request.user  

    if user.role == "admin" or user.role == "Admin":
        # Admin sees all rooms
        rooms = Room.objects.all()
    else:
        # Guests/normal users see only available rooms
        rooms = Room.objects.filter(is_available=True)

    # Optional: allow searching by room type or number
    room_type = request.GET.get("room_type")
    if room_type:
        rooms = rooms.filter(room_type__icontains=room_type)

    number = request.GET.get("number")
    if number:
        rooms = rooms.filter(number=number)

    data = [
        {
            "id": room.id,
            "number": room.number,
            "room_type": room.room_type,
            "price": str(room.price),
            "is_available": room.is_available,
        }
        for room in rooms
    ]

    return Response({"rooms": data})