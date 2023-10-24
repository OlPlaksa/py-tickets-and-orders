from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import User, Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date is not None:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket.get("movie_session"),
                row=ticket.get("row"),
                seat=ticket.get("seat"),
            )

        return order


def get_orders(username: User = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
