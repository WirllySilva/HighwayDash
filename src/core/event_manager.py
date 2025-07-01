class EventManager:
    """
    A simple implementation of the Observer pattern.
    Allows objects to subscribe and respond to custom events.
    """
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, listener_fn):
        """
        Registers a listener for a specific event.
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener_fn)

    def notify(self, event_type, data=None):
        """
        Notifies all listeners about an event.
        """
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(data)
