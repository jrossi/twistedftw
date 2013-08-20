class AlreadyInTheRoom(Exception): pass
class NotInRoom(Exception): pass


from uuid import uuid4



class Room(object):
    """
    I am a room where things can gather and pass around messages.
    """


    def __init__(self):
        self._contents = {}


    def enter(self, name, thing):
        """
        C{thing} is entering this room under the alias C{name}.

        @param name: Name of the thing entering this room.  This must be unique
            within this room.
        @param thing: Some object with C{setRoom(room)} and
            C{messageReceived(message)} methods.
        """
        if name in self._contents:
            raise AlreadyInTheRoom(name)
        thing.setRoom(self)
        self._contents[name] = thing
        self.broadcast({
            'event': 'enter',
            'who': name,
        })


    def leave(self, name):
        """
        The thing named C{name} is leaving this room.
        """
        try:
            thing = self._contents.pop(name)
        except KeyError:
            raise NotInRoom(name)
        thing.setRoom(None)
        self.broadcast({
            'event': 'leave',
            'who': name,
        })


    def kick(self, name):
        """
        The thing named C{name} is being kicked out of the room.
        """
        self.broadcast({
            'event': 'kick',
            'kicked': name,
        })
        self.leave(name)


    def contents(self):
        """
        List all the things in the room.
        """
        return self._contents


    def broadcast(self, message):
        """
        Send a message to all things in this room.
        """
        for name,thing in self._contents.items():
            thing.messageReceived(message)



class Building(object):
    """
    I am a building full of rooms.
    """


    def __init__(self):
        self._rooms = {}


    def createRoom(self):
        """
        Provision a new room.

        @return: A C{key} to be used when calling L{getRoom} and L{destroyRoom}.
        """
        key = str(uuid4())
        self._rooms[key] = Room()
        return key


    def getRoom(self, key):
        """
        Get the L{Room} associated with a C{key}.
        """
        return self._rooms[key]


    def destroyRoom(self, key):
        """
        Destroy a room (kicking everyone out of it)
        """
        room = self.getRoom(key)
        del self._rooms[key]
        for thing in room.contents():
            room.kick(thing)


