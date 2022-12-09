class FileSystemTree:
    def __init__(self, name: str,  contentSize: int = 0) -> None:
        self.name = name
        self.contentSize = contentSize
        self.leaves: list[FileSystemTree.Tree] = list()

    def addSubDir(self, tree) -> None:
        self.leaves.append(tree)
        
    def addFile(self, size: int) -> None:
        self.contentSize += size

import sys

if __name__ == "__main__":
    root = FileSystemTree("/")
    currentDir = [root]
    for line in sys.stdin:
        lineParts = line[:-1].split(" ")
        # Parse commands
        if line[0] == "$":
            if "ls" == lineParts[1]: continue
            elif "/" == lineParts[2]:
                currentDir = [root]
                continue
            elif ".." in line:
                # calculate subDirSize and add to parent dirs' size
                subDirSize = currentDir[-1].contentSize
                currentDir.pop()
                currentDir[-1].contentSize += subDirSize
                continue
            newSubDir = FileSystemTree(lineParts[2])
            currentDir[-1].addSubDir(newSubDir)
            currentDir.append(newSubDir)
        
        # Parse listing
        elif lineParts[0] == "dir": continue
        currentDir[-1].addFile(int(lineParts[0]))
    while len(subDirSize) > 1:
        subDirSize = currentDir[-1].contentSize
        currentDir[-1].pop()
        currentDir[-1].contentSize += subDirSize