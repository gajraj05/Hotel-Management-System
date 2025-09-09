from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Booking
from room.models import Room
from datetime import datetime

# Create your views here.

# ✅ Create booking
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_booking(request):
    user = request.user
    room_id = request.data.get("room_id")
    check_in = request.data.get("check_in")
    check_out = request.data.get("check_out")

    room = get_object_or_404(Room, id=room_id)

    if not room.is_available:
        return Response({"error": "Room is not available"}, status=400)
    
    # Convert string (e.g. "2025-09-06") to date object
    check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
    check_out = datetime.strptime(check_out, "%Y-%m-%d").date()

    # Calculate price
    total_days = (check_out - check_in).days
    if total_days < 1:
        total_days = 1  # At least 1 day
    amount = room.price * total_days


    # Create booking
    booking = Booking.objects.create(
        user=user,
        room=room,
        check_in=check_in,
        check_out=check_out,
        amount =amount
    )

    # Mark room unavailable
    room.is_available = False
    room.save()

    return Response({
        "message": "Booking created successfully",
        "booking_id": booking.id,
        "room_number": room.number,
        "check_in": str(booking.check_in),
        "check_out": str(booking.check_out),
        "amount": booking.amount,
        "status": booking.status
    })

# ✅ Checkout booking
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status != "Booked":
        return Response({"error": "Booking is not active"}, status=400)

    # Update booking status
    booking.status = "CheckedOut"
    booking.save()

    # Make room available again
    room = booking.room
    room.is_available = True
    room.save()

    return Response({"message": "Checked out successfully", "room_number": room.number})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status != "Booked":
        return Response({"error": "Booking is not active"}, status=400)

    # Update booking status
    booking.status = "Cancelled"
    booking.save()

    # Make room available again
    room = booking.room
    room.is_available = True
    room.save()

    return Response({"message": "Booking Cancelled successfully", "room_number": room.number})
