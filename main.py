
import sys
import time
import copy

# Ensure there are 4 arguments
if len(sys.argv) != 4:
    raise ValueError("Please provide three file names: songs.txt, albums.txt, commands.txt")

sys.argv[0] = sys.argv[0][0:len(sys.argv[0]) - sys.argv[0][::-1].find("/")]
inFile1 = sys.argv[0] + sys.argv[1]
inFile2 = sys.argv[0] + sys.argv[2]
inFile3 = sys.argv[0] + sys.argv[3]
print("\nThe files that will be used for input are {0}, {1}, and {2}"
      .format(sys.argv[1], sys.argv[2], sys.argv[3]))

start = time.time()


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


# File 1: for each song in each album, there is a node made with prev/next pointers.
album1List = LinkedList()
album2List = LinkedList()
album3List = LinkedList()

key1 = 0
inputFile1 = open(sys.argv[1], "r")
for line in inputFile1:
    if line[:6] == 'Album:':
        key1 += 1
        continue
    if line[:8] == 'Playlist':
        break
    if line != '\n':
        if key1 == 1:
            album1List.append(Node(line.strip()))
        elif key1 == 2:
            album2List.append(Node(line.strip()))
        elif key1 == 3:
            album3List.append(Node(line.strip()))
inputFile1.close()

print("Unordered doubly linked list Album #1")
album1List.printList()
print("\nUnordered doubly linked list Album #2")
album2List.printList()
print("\nUnordered doubly linked list Album #3")
album3List.printList()

# File 2: As the file is traversed, each song is removed from the doubly linked album.
# The removed song is then appended to the end of the list.
print("\n>>> Creating in-order version of each Album")
inputFile2 = open(sys.argv[2], "r")
key2 = 0
for line in inputFile2:
    if line[:6] == 'Album:':
        key2 += 1
        continue
    if line[:8] == 'Playlist':
        break
    if line != '\n':
        if key2 == 1:
            album1List.remove(line.strip())
            album1List.append(album1List.nowAt)

        elif key2 == 2:
            album2List.remove(line.strip())
            album2List.append(album2List.nowAt)
        elif key2 == 3:
            album3List.remove(line.strip())
            album3List.append(album3List.nowAt)
inputFile2.close()

print("Ordered doubly linked list Album #1")
album1List.printList()
print("\nOrdered doubly linked list Album #2")
album2List.printList()
print("\nOrdered doubly linked list Album #3")
album3List.printList()


# File 3: As the file is traversed, each command for each album is passed into its command method.
# The class then processes the command as previously noted.
print("\n\nStarting to process play commands")
inputFile3 = open(sys.argv[3], "r")
key3 = 0
for line in inputFile3:
    if line[:8] == 'Playlist':
        break
    if line[:6] == 'Album:':
        key3 += 1
        print("\n\nExecuting commands for Album #{}".format(key3))
        continue
    if line != '\n':
        if key3 == 1:
            album1List.command(line.strip())
        elif key3 == 2:
            album2List.command(line.strip())
        elif key3 == 3:
            album3List.command(line.strip())
        else:
            print("Program intended for three albums as per instructions.")
            break
inputFile3.close()
print()

# The playlist songs are read in from file1.
# Each song is searched in its album and then appended to the playlist.
inputFile1 = open(sys.argv[1], "r")
key4 = False
playList = LinkedList()
for line in inputFile1:
    if line[:8] == 'Playlist':
        key4 = True
        continue
    if key4:
        if int(line[:1]) == 1:
            if album1List.find(line[1:].strip()):
                nodeCopy = copy.copy(album1List.nowAt)
                playList.append(nodeCopy)
        if int(line[:1]) == 2:
            if album2List.find(line[1:].strip()):
                nodeCopy = copy.copy(album2List.nowAt)
                playList.append(nodeCopy)
        if int(line[:1]) == 3:
            if album3List.find(line[1:].strip()):
                nodeCopy = copy.copy(album3List.nowAt)
                playList.append(nodeCopy)


inputFile1.close()

print("\nSongs on the doubly linked playlist: ")
playList.printList()

# The list of commands are read and executed for the playlist.
print("\n\nStarting to process playlist commands\n\nExecuting commands for Playlist")
inputFile3 = open(sys.argv[3], "r")
key5 = False
for line in inputFile3:
    if line[:8] == 'Playlist':
        key5 = True
        continue
    if key5:
        playList.command(line.strip())
inputFile3.close()

end = time.time()
time = end - start

# Below are the statistics.
# The commands take all 3 album linked lists and 1 playlist linked list into account.
print("\n**********************")
print("***** Statistics *****")
print("**********************")
print("Total Songs Read:", Node.counter)
forwardCount = album1List.forwardCount + album2List.forwardCount + album3List.forwardCount + playList.forwardCount
print("Number of Skip Forward commands:", forwardCount)
backwardCount = album1List.backwardCount + album2List.backwardCount + album3List.backwardCount + playList.backwardCount
print("Number of Skip Backward commands:", backwardCount)
playCount = album1List.playCount + album2List.playCount + album3List.playCount + playList.playCount
print("Number of Play Next Track commands:", playCount)
print("Number of Append commands:", Node.counter)
beginCount = album1List.beginCount + album2List.beginCount + album3List.beginCount + playList.beginCount
print("Number of Beginning Forward commands: ", beginCount)
endCount = album1List.endCount + album2List.endCount + album3List.endCount + playList.endCount
print("Number of End Forward commands: ", endCount)
print("Total time of program: {0:.8f} milliseconds".format(time))
