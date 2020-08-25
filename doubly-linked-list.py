# Class Node is used for each Song title.
class Node:
    counter = 0

    def __init__(self, value):
        Node.counter += 1
        self.value = value
        self.next = None
        self.prev = None


# Class LinkedList is used for each album and once for the Playlist.
class LinkedList:
    def __init__(self):
        self.head = self.tail = None
        # The below count variables keep track of the commands in the command file.
        self.forwardCount = self.backwardCount = self.playCount = self.beginCount = self.endCount = 0
        # nowAt and playing keep track of where the player is at and what is actively playing.
        self.nowAt = None
        self.playing = None

    # append takes a newNode and adds it to the end of the list or to the beginning if list is empty.
    def append(self, newNode):
        newNode.next = None
        newNode.prev = None
        if self.head is None:
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.next = newNode
            newNode.prev = self.tail
            self.tail = newNode

    # printList is is used to traverse and print the linked list.
    def printList(self):
        curNode = self.head
        while curNode is not None:
            print("-", curNode.value)
            curNode = curNode.next

    # finds node with matching key
    def find(self, node_key):
        self.nowAt = self.head
        while self.nowAt is not None:
            if self.nowAt.value == node_key:
                return True
            self.nowAt = self.nowAt.next
        return False

    # removes node that is found based on matching key
    def remove(self, node_key):
        self.find(node_key)
        successor_node = self.nowAt.next
        predecessor_node = self.nowAt.prev

        if successor_node is not None:
            successor_node.prev = predecessor_node
        if predecessor_node is not None:
            predecessor_node.next = successor_node

        if self.nowAt is self.head:
            self.head = successor_node
        if self.nowAt is self.tail:
            self.tail = predecessor_node

    # command takes any command from the file and process it using the nowAt and playing.
    # an if else structure facilitates this processing while incrementing the count variables for each command.
    def command(self, request):
        if request == 'Beginning':
            self.nowAt = self.head
            self.beginCount += 1
            print("Now At:", self.nowAt.value)
        elif request == 'Skip Forward':
            self.nowAt = self.nowAt.next
            self.forwardCount += 1
            print("Now At:", self.nowAt.value)
        elif request == 'Skip Backward':
            self.nowAt = self.nowAt.prev
            self.backwardCount += 1
            print("Now At:", self.nowAt.value)
        elif request == 'Play Track':
            self.playing = self.nowAt
            self.playCount += 1
            print("Now Playing:", self.playing.value)
        elif request == 'End':
            self.nowAt = self.tail
            self.endCount += 1
            print("Now At:", self.nowAt.value)
        else:
            print("Unrecognised", request)
