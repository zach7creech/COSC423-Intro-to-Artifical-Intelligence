"""
Author: Zachery Creech.

This file 'main.py' contains the implementation for class PathPlanner as well as
the driving code in main() to accept command line arguments to utilize the class.
The class contains 3 search functions, two uninformed BFS and DFS, and one informed
A* that utlizes Euclidean distance as its heuristic. It also contains two helper
functions, inBounds to determine if a node has already been visited, is outside the
grid, or is a 'wall' (a 1), and printPath that will print the path returned by each
of the search functions. This file also contains implementation for class Node that
each traversed pair of indices is stored as. Contains a node's i,j coordinates and
a pointer to its parent, which is helpful for printing the final path.
"""

import sys
import math

class PathPlanner:
    """
    Contains 3 search functions, BFS, DFS, and A* and helper functions inBounds and printPath.

    Two uninformed BFS and DFS, and one informed A* that utilizes Euclidean distance as its 
    heuristic. It also contains two helper functions for determining node validity and printing 
    the final path returned by the search functions.
    """

    def inBounds(self, i, j, grid):
        """
        Given a node's i,j coordinates and a grid, determine if a node is valid to examine.

        A node is valid if its coordinates lie within the grid, it has not already been visited,
        and there is not a wall at its coordinates.

        @param i: i coordinate in grid. j: j coordinate in grid. grid: grid provided from main.
        @return True if the node is valid
        """
        if i < 0 or i > len(grid) - 1 or j < 0 or j > len(grid[0]) - 1:
            return False
        if grid[i][j] == 1:
            return False
        return True

    def printPath(self, path):
        """
        Given a list of tuples representing coordinate pairs, print the list with required formatting.

        @param path: list of nodes returned by each search method
        @return nothing, simply print the provided list
        """
        print('Path: [', end='')
        if(path):
            print(*path, end='')
        print(']')
        print('Traversed: ' + str(self.traversed))

    def breadth_first_search(self, start, goal, grid):
        """
        Given starting coordinates, goal coordinates, and a grid to traverse, perform a breadth first search to determine a path from start to goal.

        Grid is expanded as a tree, and each 'layer' of the tree is traversed in order.
        Traverse each subtree's valid neighbors in order bottom, right, top, left.

        @param start: list of size two containing start i,j. goal: list of size two containing goal i,j. grid: 2D list representing grid
        @return a list of tuples representing pairs of coordinates ordered from start node to goal node
        """
        path = []
        self.traversed = 0
        tree = []
        # root has no parent
        root = Node(None, start[0], start[1])

        tree.append(root)
        grid[root.i][root.j] = 1

        while len(tree) > 0:
            
            self.traversed += 1

            # pop off the front of the 'tree', next node in the layer
            curNode = tree.pop(0)

            # found the goal node
            if curNode.i == goal[0] and curNode.j == goal[1]:
                # go back up the tree through parent pointers to find the path
                while curNode != None:
                    path.append((curNode.i, curNode.j))
                    curNode = curNode.parent
                # path must be reversed because the last tuple pushed on it is the start node
                path.reverse()
                return path

            # for bottom, right, top, then left neighbor, add the node to the 'tree' if its a valid location
            # also mark each valid node as visited before restarting loop to pop off next node in the layer

            bottomNode = Node(curNode, curNode.i + 1, curNode.j)
            if self.inBounds(bottomNode.i, bottomNode.j, grid):
                tree.append(bottomNode)
                grid[bottomNode.i][bottomNode.j] = 1
            
            rightNode = Node(curNode, curNode.i, curNode.j + 1)
            if self.inBounds(rightNode.i, rightNode.j, grid):
                tree.append(rightNode)
                grid[rightNode.i][rightNode.j] = 1
            
            topNode = Node(curNode, curNode.i - 1, curNode.j)
            if self.inBounds(topNode.i, topNode.j, grid):
                tree.append(topNode)
                grid[topNode.i][topNode.j] = 1
            
            leftNode = Node(curNode, curNode.i, curNode.j - 1)
            if self.inBounds(leftNode.i, leftNode.j, grid):
                tree.append(leftNode)
                grid[leftNode.i][leftNode.j] = 1
            
    def depth_first_search(self, start, goal, grid):
        """
        Given starting coordinates, goal coordinates, and a grid to traverse, perform a depth first search to determine a path from start to goal.

        Grid is expanded as a tree, and tree is traversed as 'deep' as possible in order for each node.
        Traverse each subtree's valid neighbors in order bottom, right, top, left.

        @param start: list of size two containing start i,j. goal: list of size two containing goal i,j. grid: 2D list representing grid
        @return a list of tuples representing pairs of coordinates ordered from start node to goal node
        """
        path = []
        self.traversed = 0
        tree = []
        # root has no parent
        root = Node(None, start[0], start[1])

        tree.append(root)

        while len(tree) > 0:

            # pop off the back of the 'tree', the next deepest node
            curNode = tree.pop()
            
            # found the goal node
            if curNode.i == goal[0] and curNode.j == goal[1]:
                self.traversed += 1
                # go back up through parent pointers to find the path
                while curNode != None:
                    path.append((curNode.i, curNode.j))
                    curNode = curNode.parent
                # path must be reversed because the last tuple pushed on it is the start node
                path.reverse()
                return path

            # if the node is not valid, ignore it and check the next one
            if not self.inBounds(curNode.i, curNode.j, grid):
                continue

            # mark visited
            self.traversed += 1
            grid[curNode.i][curNode.j] = 1

            # for left, top, right, then bottom neighbor, add the node to the 'tree'
            # backwards order because the node is popped off the back each time, want to start with bottom each time

            leftNode = Node(curNode, curNode.i, curNode.j - 1)
            tree.append(leftNode)
            topNode = Node(curNode, curNode.i - 1, curNode.j)
            tree.append(topNode)
            rightNode = Node(curNode, curNode.i, curNode.j + 1)
            tree.append(rightNode)
            bottomNode = Node(curNode, curNode.i + 1, curNode.j)
            tree.append(bottomNode)

    def a_star_search(self, start, goal, grid):
        """
        Given starting coordinates, goal coordinates, and a grid to traverse, perform an A* search to determine a path from start to goal.

        Grid is expanded as a tree, and tree is traversed based on heuristic hx that is Euclidean distance of node from goal.
        Check each subtree's valid neighbors in order bottom, right, top, left.

        @param start: list of size two containing start i,j. goal: list of size two containing goal i,j. grid: 2D list representing grid
        @return a list of tuples representing pairs of coordinates ordered from start node to goal node
        """
        path = []
        self.traversed = 1
        gx = 0
        # root has no parent
        root = Node(None, start[0], start[1])
        curNode = root

        while curNode.i != goal[0] or curNode.j != goal[1]:

            grid[curNode.i][curNode.j] = 1
            self.traversed += 1

            # 'initialize' fx as a large number that will always be greater than every node's fx for comparison later
            fx = len(grid) * len(grid[0])

            # check in bottom, right, top, left order if each neighboring node is valid. If it is, calculate its Euclidean distance from the goal
            # Euclidean distance is found using Pythagorean theorem
            # if it isn't valid, still assign it an hx value for later comparison

            bottomNode = Node(curNode, curNode.i + 1, curNode.j)
            if self.inBounds(bottomNode.i, bottomNode.j, grid):
                bottomNode.hx = math.sqrt((bottomNode.i - goal[0]) * (bottomNode.i - goal[0]) + (bottomNode.j - goal[1]) * (bottomNode.j - goal[1]))
                grid[bottomNode.i][bottomNode.j] = 1
            else:
                bottomNode.hx = fx

            rightNode = Node(curNode, curNode.i, curNode.j + 1)
            if self.inBounds(rightNode.i, rightNode.j, grid):
                rightNode.hx = math.sqrt((rightNode.i - goal[0]) * (rightNode.i - goal[0]) + (rightNode.j - goal[1]) * (rightNode.j - goal[1]))
                grid[rightNode.i][rightNode.j] = 1
            else:
                rightNode.hx = fx

            topNode = Node(curNode, curNode.i - 1, curNode.j)
            if self.inBounds(topNode.i, topNode.j, grid):
                topNode.hx = math.sqrt((topNode.i - goal[0]) * (topNode.i - goal[0]) + (topNode.j - goal[1]) * (topNode.j - goal[1]))
                grid[topNode.i][topNode.j] = 1
            else:
                topNode.hx = fx

            leftNode = Node(curNode, curNode.i, curNode.j - 1)
            if self.inBounds(leftNode.i, leftNode.j, grid):
                leftNode.hx = math.sqrt((leftNode.i - goal[0]) * (leftNode.i - goal[0]) + (leftNode.j - goal[1]) * (leftNode.j - goal[1]))
                grid[leftNode.i][leftNode.j] = 1
            else:
                leftNode.hx = fx

            # no neighbor is a valid next node, so return an empty path
            if bottomNode.hx == fx and rightNode.hx == fx and topNode.hx == fx and leftNode.hx == fx:
                return path

            # gx in this case is just the total distance traveled from the start node, which is the same for every next node
            # find the next node with lowest fx based on heuristic hx

            if bottomNode.hx + gx < fx:
                fx = bottomNode.hx + gx
                nextNode = bottomNode
            if rightNode.hx + gx < fx:
                fx = rightNode.hx + gx
                nextNode = rightNode
            if topNode.hx + gx < fx:
                fx = topNode.hx + gx
                nextNode = topNode
            if leftNode.hx + gx < fx:
                fx = leftNode.hx + gx
                nextNode = leftNode

            curNode = nextNode
            gx += 1

        # found the goal node, go back up the tree through parent pointers to find the path
        while curNode != None:
            path.append((curNode.i, curNode.j))
            curNode = curNode.parent
        
        # path must be reversed because the last tuple pushed on it is the start node
        path.reverse()
        return path

class Node:
    """
    Node class for representing coordinates in the grid as nodes in a tree.

    Contains coordinates i,j and pointer to node's parent for printing path.
    """

    def __init__(self, parent, i, j):
        """
        Constructor for Node class.

        Set node's parent and i,j coordinates.
        """
        self.parent = parent
        self.i = i
        self.j = j

def main():
    """
    Driver code for using PathPlanner class.

    When running main.py, the user must provide arguments detailed in the usage prompt below.
    The user can choose to find a path through a grid using BFS, DFS, A*, or ALL search
    methods. The found path is printed in the terminal, along with the number of traversed
    nodes.
    """
    if len(sys.argv) != 9:
        print('usage: python3 main.py --input FILENAME --start START_NODE --goal GOAL_NODE --search SEARCH_TYPE')
        exit()
    
    if sys.argv[1] != '--input':
        print('usage: need --input FILENAME')
        exit()
    if sys.argv[3] != '--start':
        print('usage: need --start START_NODE')
        exit()
    if sys.argv[5] != '--goal':
        print('usage: need --goal GOAL_NODE')
        exit()
    if sys.argv[7] != '--search':
        print('usage: need --search SEARCH_TYPE')
        exit()
    
    # read in the grid from file specified by sys.argv[2]
    # remove commas and append integers
    bfsgrid = []
    dfsgrid = []
    agrid = []
    with open(sys.argv[2]) as f:
        i = 0
        filerows = f.readlines()
        for filerow in filerows:
            bfsgrid.append([])
            dfsgrid.append([])
            agrid.append([])
            for c in filerow.strip():
                if c == ',':
                    continue
                elif c == '0':
                   bfsgrid[i].append(0)
                   dfsgrid[i].append(0)
                   agrid[i].append(0)
                elif c == '1':
                    bfsgrid[i].append(1)
                    dfsgrid[i].append(1)
                    agrid[i].append(1)
                else:
                    print('File cannot contain character ' + c)
            i += 1

    """
    The grid is modified during each search to mark nodes as visited, rather than maintaining a separate visited array.
    The benefit of this is that isBounds can be used to check for walls and visited nodes in the same statement. The
    downside is that separate grids must be used for each search function if a user specifies 'ALL'.
    Normally reading in one grid that would be copied with deepcopy() would suffice, but I didn't want points taken off for importing another library.
    """

    start = []
    goal = []

    startStrings = sys.argv[4].split(',')
    goalStrings = sys.argv[6].split(',')

    try:
        # get start i,j 
        start.append(int(startStrings[0]))
        start.append(int(startStrings[1]))

        # get goal i,j
        goal.append(int(goalStrings[0]))
        goal.append(int(goalStrings[1]))
    except ValueError:
        print('Start and end coordinates must be i,j format')
        exit()

    pp = PathPlanner()

    # check that start and goal coordinates are within grid and not on a wall
    if not pp.inBounds(start[0], start[1], bfsgrid):
        print('Bad start position')
        exit()
    if not pp.inBounds(goal[0], goal[1], bfsgrid):
        print('Bad goal position')
        exit()

    if sys.argv[8] == 'BFS' or sys.argv[8] == 'ALL':
        path = pp.breadth_first_search(start, goal, bfsgrid)
        pp.printPath(path)
    if sys.argv[8] == 'DFS' or sys.argv[8] == 'ALL':
        path = pp.depth_first_search(start, goal, dfsgrid)
        pp.printPath(path)
    if sys.argv[8] == 'astar' or sys.argv[8] == 'ALL':
        path = pp.a_star_search(start, goal, agrid)
        pp.printPath(path)

if __name__ == "__main__":
    main()
