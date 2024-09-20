
from typing import Callable


class Event():
    """
    A class that implements the Observer pattern.

    This class acts as a central hub for events, allowing multiple subscribers to be notified when an event occurs.
    Subscribers can register to receive notifications using the subscribe method, and unregister using the unsubscribe method. 
    When the event is triggered, the invoke method will call all subscribed functions with the provided arguments.
    """

    subscribers: list[Callable] = []

    @classmethod
    def subscribe(cls, subscriber: Callable):
        """
        Subscribes a function to this event.

        Args:
            subscriber (Callable): The function to be called when the event is invoked.
        """
        cls.subscribers.append(subscriber)

    @classmethod
    def unsubscribe(cls, subscriber: Callable):
        """
        Unsubscribes a function from this event.

        Args:
            subscriber (Callable): The function to unsubscribe.
        """
        cls.subscribers.remove(subscriber)

    @classmethod
    def invoke(cls, *args):
        """
        Invokes the event, calling all subscribed functions with the provided arguments.

        Args:
            *args: Arguments to be passed to the subscribed functions.
        """
        for subscriber in cls.subscribers:
            subscriber(*args)