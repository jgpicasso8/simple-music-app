import doubly_linked_list as linked_list
import sys
import time
import copy

# Ensure there are 4 arguments
if len(sys.argv) != 4:
    raise ValueError("Please provide three file names.")

sys.argv[0] = sys.argv[0][0:len(sys.argv[0]) - sys.argv[0][::-1].find("/")]
inFile1 = sys.argv[0] + sys.argv[1]
inFile2 = sys.argv[0] + sys.argv[2]
inFile3 = sys.argv[0] + sys.argv[3]
print("\nThe files that will be used for input are {0}, {1}, and {2}"
      .format(sys.argv[1], sys.argv[2], sys.argv[3]))

start = time.time()


# File 1: for each song in each album, there is a node made with prev/next pointers.
album1List = linked_list.LinkedList()
album2List = linked_list.LinkedList()
album3List = linked_list.LinkedList()

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
            album1List.append(linked_list.Node(line.strip()))
        elif key1 == 2:
            album2List.append(linked_list.Node(line.strip()))
        elif key1 == 3:
            album3List.append(linked_list.Node(line.strip()))
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
playList = linked_list.LinkedList()
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
print("Total Songs Read:", linked_list.Node.counter)
forwardCount = album1List.forwardCount + album2List.forwardCount + album3List.forwardCount + playList.forwardCount
print("Number of Skip Forward commands:", forwardCount)
backwardCount = album1List.backwardCount + album2List.backwardCount + album3List.backwardCount + playList.backwardCount
print("Number of Skip Backward commands:", backwardCount)
playCount = album1List.playCount + album2List.playCount + album3List.playCount + playList.playCount
print("Number of Play Next Track commands:", playCount)
print("Number of Append commands:", linked_list.Node.counter)
beginCount = album1List.beginCount + album2List.beginCount + album3List.beginCount + playList.beginCount
print("Number of Beginning Forward commands: ", beginCount)
endCount = album1List.endCount + album2List.endCount + album3List.endCount + playList.endCount
print("Number of End Forward commands: ", endCount)
print("Total time of program: {0:.8f} milliseconds".format(time))
