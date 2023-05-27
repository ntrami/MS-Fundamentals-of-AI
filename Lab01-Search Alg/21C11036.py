# IDE: Visual Studio Code
# Name: Nguyen Thi Ngoc Tram
# Student ID: 21C11036

import string
from tkinter import *
from time import sleep 
import random

from executing import Source

def getInput(path):
    li = []
    f=open(path, "r")
    li = f.read().splitlines()
    f.close()
    mazeSize = [int(ele) for ele in li[0].split()]
    SGPos = [int(ele) for ele in li[1].split()]
    nObstacle = int(li[2])

    obstacleList = []
    for i in range(3, 3+nObstacle):
        obs = [int(ele) for ele in li[i].split()]
        verticeLs = []
        for i in range(0, len(obs), 2):
            vertice = (obs[i], obs[i+1])
            verticeLs.append(vertice)
        obstacleList.append(verticeLs)
    return mazeSize, SGPos, nObstacle, obstacleList

# Read Input File
path = "O:/POSTGRAD/HK2/1. AI_BTKT - Mon/HW1/input.txt"
mazeSz, SGPos, nObstacle, obstacleList = getInput(path)

# Create MAZE 
cellSz = int(700/(mazeSz[0]+1))
master = Tk()
master.title("VISUALIZATION OF SEARCH ALGORITHMS")
mazeWidth = mazeSz[0]+1 
mazeHeight = mazeSz[1]+1 
maze = Canvas(master, width=mazeWidth*cellSz, height=mazeHeight*cellSz)

def createCell(x, y, cellSz, mazeHeight, color):
    return maze.create_rectangle(x*cellSz, (mazeHeight-y-1)*cellSz, (x+1)*cellSz,  (mazeHeight-y)*cellSz, fill=color, outline = 'black')

def createMaze(maze, mazeWidth, mazeHeight, cellSz):
    for i in range(mazeHeight):
        for j in range(mazeWidth):
            if (i==0 or i==mazeHeight-1 or j==0 or j==mazeWidth-1):
                maze.create_rectangle(j*cellSz, i*cellSz, (j+1)*cellSz, (i+1)*cellSz, fill="silver", outline = 'black')
            else:
                maze.create_rectangle(j*cellSz, i*cellSz, (j+1)*cellSz, (i+1)*cellSz, fill="white", outline = 'black')
    for i in range(mazeWidth):
        maze.create_text((int(cellSz/2), int(cellSz/2)+i*cellSz), text=mazeHeight-i-1, fill="black", font=('Arial 10'))
    for i in range(1, mazeWidth):
        maze.create_text((int(0.5*cellSz) + int(i+0.5)*cellSz, (mazeHeight-0.5)*cellSz), text=i, fill="black", font=('Arial 10'))

class POINT:
    def __init__(self, abscissa, ordinate):
        self.x, self.y = abscissa, ordinate
    def printPoint(self):
        print(self.x, " ", self.y)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def get_next_nodes(point):
    check_next_node = lambda x,y: True if 0 <= x < mazeSz[0] and 0 <= y < mazeSz[1] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(point.x+dx, point.y+dy) for dx, dy in ways if check_next_node(point.x+dx, point.y+dy)]

class OBSTACLE:
    def __init__(self, verticeLs, obsticleCells):
        color = ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
        for i in range(-1, len(verticeLs)-1):
            createCell(verticeLs[i][0], verticeLs[i][1], cellSz, mazeHeight, color)
            obsticleCells.append(verticeLs[i])
            # Same column or row => go straight
            if (verticeLs[i][1] - verticeLs[i+1][1] == 0):
                step = int((verticeLs[i+1][0]-verticeLs[i][0])/abs(verticeLs[i+1][0]-verticeLs[i][0]))
                for abscissa in range(verticeLs[i][0]+step, verticeLs[i+1][0], step):
                    point = (abscissa, verticeLs[i][1])
                    obsticleCells.append(point)
                    createCell(point[0], point[1], cellSz, mazeHeight, "#CAFF70")
            if (verticeLs[i][0] - verticeLs[i+1][0] == 0):
                step = int((verticeLs[i+1][1]-verticeLs[i][1])/abs(verticeLs[i+1][1]-verticeLs[i][1]))
                for ordinate in range(verticeLs[i][1]+step, verticeLs[i+1][1], step):
                    point = (verticeLs[i][0], ordinate)
                    obsticleCells.append(point)
                    createCell(point[0], point[1], cellSz, mazeHeight, "#CAFF70")
            # 1 unit difference => 1 cell move different 1 unit
            if (abs(verticeLs[i][1] - verticeLs[i+1][1]) == 1):
                step = int((verticeLs[i+1][0]-verticeLs[i][0])/abs(verticeLs[i+1][0]-verticeLs[i][0]))
                for abscissa in range(verticeLs[i][0]+step, verticeLs[i+1][0], step):
                    if (abscissa==verticeLs[i][0]+step):
                        point = (abscissa, verticeLs[i][1])
                        obsticleCells.append(point)
                        createCell(point[0], point[1], cellSz, mazeHeight, "#CAFF70")
                    else:
                        point = (abscissa, verticeLs[i+1][1])
                        obsticleCells.append(point)
                        createCell(point[0], point[1], cellSz, mazeHeight, "#CAFF70")
            
            if (abs(verticeLs[i][0] - verticeLs[i+1][0]) == 1):
                step = int((verticeLs[i+1][1]-verticeLs[i][1])/abs(verticeLs[i+1][1]-verticeLs[i][1]))
                for ordinate in range(verticeLs[i][1]+step, verticeLs[i+1][1], step):
                    if (i==0):
                        point = (verticeLs[i][0], ordinate)
                        obsticleCells.append(point)
                        createCell(point[0], point[1], cellSz, mazeHeight, "#CAFF70")
                    elif (i==2):
                        point = (verticeLs[i+1][0], ordinate)
                        obsticleCells.append(point)
                        createCell(point[0], point[1], cellSz, mazeHeight, "#CAFF70")
            # n unit difference => n cell move different 1 unit
            if (verticeLs[i][0] - verticeLs[i+1][0])==-(verticeLs[i][1] - verticeLs[i+1][1]):
                step = int((verticeLs[i+1][0]-verticeLs[i][0])/abs(verticeLs[i+1][0]-verticeLs[i][0]))
                y=verticeLs[i][1]-step
                for ord in range(verticeLs[i][0]+step, verticeLs[i+1][0], step):             
                    point = (ord, y)
                    obsticleCells.append(point)
                    createCell(point[0], point[1], cellSz, mazeHeight, "#CAFF70")
                    y-=step
            if (verticeLs[i][0] - verticeLs[i+1][0])==(verticeLs[i][1] - verticeLs[i+1][1]):
                step = int((verticeLs[i+1][0]-verticeLs[i][0])/abs(verticeLs[i+1][0]-verticeLs[i][0]))
                y=verticeLs[i][1]+step
                for ord in range(verticeLs[i][0]+step, verticeLs[i+1][0], step):             
                    point = (ord, y)
                    obsticleCells.append(point)
                    createCell(point[0], point[1], cellSz, mazeHeight, "#CAFF70")
                    y+=step

# Create SOURCE Point
def createSource():
    source = (SGPos[0], SGPos[1])
    createCell(source[0], source[1], cellSz, mazeHeight, "blue")
    maze.create_text((int(0.5*cellSz) + int(source[0]+0.5)*cellSz, int(cellSz/2)+(mazeHeight-source[1]-1)*cellSz), text='S', fill="white", font=('Arial 12 bold'))
    return source
# Create GOAL Point
def createGoal():
    goal = (SGPos[2], SGPos[3])
    createCell(goal[0], goal[1], cellSz, mazeHeight, "blue")
    maze.create_text((int(0.5*cellSz) + int(goal[0]+0.5)*cellSz, int(cellSz/2)+(mazeHeight-goal[1]-1)*cellSz), text='G', fill="white", font=('Arial 12 bold'))
    return goal

def drawPath(source, goal, path):
        pathCells = []
        if goal == source:
            print(source)
            return
        if path[goal] == -1:
            print("NO PATH")
            return
        while True:
            pathCells.append(goal)
            goal = path[goal]
            if goal == source:
                pathCells.append(source)
                break
        for i in range(len(pathCells)-1, -1, -1):
            createCell(pathCells[i][0], pathCells[i][1], cellSz, mazeHeight, "orange")
            maze.create_text((int(0.5*cellSz) + int(pathCells[i][0]+0.5)*cellSz, int(cellSz/2)+(mazeHeight-pathCells[i][1]-1)*cellSz), text='+', fill="blue", font=('Arial 12 bold'))
            createSource()
            createGoal()
            # print(pathCells[i], end=" ")
        return (len(pathCells))

def Breadth_first_search():
    print ("---------- Breadth-first Search ----------")
    createMaze(maze, mazeWidth, mazeHeight, cellSz)
    source = createSource()
    goal = createGoal()

    # Create OBSTACLES
    obsLs = []
    for obs in obstacleList:
        obstacleCells = []
        obstacle = OBSTACLE(obs, obstacleCells)
        obsLs.append(obstacleCells)
    # BFS Algorithm    
    graph = {}
    for i in range (mazeWidth):
        for j in range (mazeHeight):    
            graph[(i,j)] = get_next_nodes(POINT(i, j))
    # print(len(graph))

    # Remove obstacle points from graph
    for obs in obsLs:          
        for node in obs:
            graph.pop((node[0], node[1]))

    # print(graph)
    # print(len(graph))

    # BFS Settings
    from queue import Queue
    print("source: ", source)
    print("Goal: ", goal)
    queue = Queue()
    visited = {k: False for k in graph}
    path = {k: -1 for k in graph}

    visited[source] = True
    queue.put(source)
    expendedNodeCost = 0
    while not queue.empty():
        # print(list(queue.queue))
        cur_node = queue.get()
        expendedNodeCost+=1
        createCell(cur_node[0], cur_node[1], cellSz, mazeHeight, "lightblue")
        for next_node in graph[cur_node]:
            # print("next_node: ", next_node)
            if next_node in graph and not visited[next_node]:
                visited[next_node] = True
                queue.put(next_node)
                path[next_node] = cur_node

    # Draw path
    cost = drawPath(source, goal, path)
    print("Cost Of Path from Source to Goal: ", cost-1)
    print("Cost of the expanded node: ", expendedNodeCost)

    maze.pack()
    master.mainloop()

def Uniform_cost_search():
    print ("---------- Uniform-cost Search ----------")
    createMaze(maze, mazeWidth, mazeHeight, cellSz)
    source = createSource()
    goal = createGoal()

    # Create OBSTACLES
    obsLs = []
    for obs in obstacleList:
        obstacleCells = []
        obstacle = OBSTACLE(obs, obstacleCells)
        obsLs.append(obstacleCells)

    # Graph to save node and next node
    graph = {}
    for i in range (mazeWidth):
        for j in range (mazeHeight):    
            graph[(i,j)] = get_next_nodes(POINT(i, j))
    # Remove obstacle points from graph
    for obs in obsLs:          
        for node in obs:
            graph.pop((node[0], node[1]))
    # _______________________
    # Begin Search Algorithm
    import queue
    INF = int(1e9)
    print("Source: ", source)
    print("Goal: ", goal)
    dist = {k: INF for k in graph}
    path = {k: -1 for k in graph}
    pq = queue.PriorityQueue()
    pq.put([source, 0])
    dist[source] = 0
    expendedNodeCost = 0
    while pq.empty() == False:
        top = pq.get()
        cur_node = top[0]
        expendedNodeCost += 1
        # createCell(cur_node[0], cur_node[1], cellSz, mazeHeight, "lightblue")
        w = top[1]
        for next_node in graph[cur_node]:
            if next_node in graph and w + 1 < dist[next_node]:
                dist[next_node] = w+1
                pq.put([next_node, dist[next_node]])
                path[next_node] = cur_node

    # Draw path
    cost = drawPath(source, goal, path)
    print("Cost Of Path from Source to Goal: ", cost-1)
    print("Cost of the expanded node: ", expendedNodeCost)
    maze.pack()
    master.mainloop()

def Iterative_deeping_search(maxDepth):
    print ("---------- Iterative deepining Search ----------")
    createMaze(maze, mazeWidth, mazeHeight, cellSz)
    source = createSource()
    goal = createGoal()

    # Create OBSTACLES
    obsLs = []
    for obs in obstacleList:
        obstacleCells = []
        obstacle = OBSTACLE(obs, obstacleCells)
        obsLs.append(obstacleCells)
    # _______________________
    # Begin Search Algorithm
    # Graph to save node and next node
    graph = {}
    for i in range (mazeWidth):
        for j in range (mazeHeight):    
            graph[(i,j)] = get_next_nodes(POINT(i, j))
    # Remove obstacle points from graph
    for obs in obsLs:          
        for node in obs:
            graph.pop((node[0], node[1]))

    visited = {k: False for k in graph}
    path = {k: -1 for k in graph}
    stack = []
    visited[source] = True
    stack.append(source)
    expendedNodeCost = 0
    # while len(stack) > 0:
    for i in range(maxDepth):
        cur_node = stack.pop()
        expendedNodeCost += 1
        for next_node in graph[cur_node]:
            if next_node in graph and not visited[next_node]:
                visited[next_node] = True
                stack.append(next_node)
                path[next_node] = cur_node
                if (next_node == goal):
                    print("Maximum depth: ", maxDepth)
                    print("Depth to stop algorithm: ", expendedNodeCost)
                    drawPath(source, goal, path)
                    cost = drawPath(source, goal, path)
                    print("Source: ", source)
                    print("Goal: ", goal)
                    print("Cost Of Path from Source to Goal: ", cost-1)
                    print("Cost of the expanded node: ", expendedNodeCost)
                    maze.pack()
                    master.mainloop()
                    return

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def Greedy_best_first_search():
    print ("---------- Greedy best first search ----------")
    createMaze(maze, mazeWidth, mazeHeight, cellSz)
    source = createSource()
    goal = createGoal()

    # Create OBSTACLES
    obsLs = []
    for obs in obstacleList:
        obstacleCells = []
        obstacle = OBSTACLE(obs, obstacleCells)
        obsLs.append(obstacleCells)
    
    graph = {}
    for i in range (mazeWidth):
        for j in range (mazeHeight):    
            graph[(i,j)] = get_next_nodes(POINT(i, j))
    # Remove obstacle points from graph
    for obs in obsLs:          
        for node in obs:
            graph.pop((node[0], node[1]))
    # _______________________
    # Begin Search Algorithm
    import queue
    INF = int(1e9)
    print("Source: ", source)
    print("Goal: ", goal)
    dist = {k: INF for k in graph}
    path = {k: -1 for k in graph}
    pq = queue.PriorityQueue()
    pq.put([source, 0])
    dist[source] = 0

    expendedNodeCost = 0
    while pq.empty() == False:
        top = pq.get()
        cur_node = top[0]
        cur_cost = top[1]
        expendedNodeCost += 1
        # createCell(cur_node[0], cur_node[1], cellSz, mazeHeight, "lightblue")
        if cur_node == goal:
            queue = []
            continue

        min = heuristic(graph[cur_node][0], goal)
        for i in range (1, len(graph[cur_node])):
            next_node = graph[cur_node][i]
            if next_node in graph and heuristic(next_node, goal) < min: 
                dist[next_node] = heuristic(next_node, goal) 
                pq.put([next_node, dist[next_node]])
                path[next_node] = cur_node
            

    # Draw path
    cost = drawPath(source, goal, path)
    print("Cost Of Path from Source to Goal: ", cost-1)
    print("Cost of the expanded node: ", expendedNodeCost)

    maze.pack()
    master.mainloop()

def A_star():
    print ("---------- Graph Search A* ----------")
    createMaze(maze, mazeWidth, mazeHeight, cellSz)
    source = createSource()
    goal = createGoal()

    # Create OBSTACLES
    obsLs = []
    for obs in obstacleList:
        obstacleCells = []
        obstacle = OBSTACLE(obs, obstacleCells)
        obsLs.append(obstacleCells)
    
    graph = {}
    for i in range (mazeWidth):
        for j in range (mazeHeight):    
            graph[(i,j)] = get_next_nodes(POINT(i, j))
    # Remove obstacle points from graph
    for obs in obsLs:          
        for node in obs:
            graph.pop((node[0], node[1]))
    # _______________________
    # Begin Search Algorithm
    import queue
    INF = int(1e9)
    print("Source: ", source)
    print("Goal: ", goal)
    dist = {k: INF for k in graph}
    path = {k: -1 for k in graph}
    pq = queue.PriorityQueue()
    pq.put([source, 0])
    dist[source] = 0

    expendedNodeCost = 0
    while pq.empty() == False:
        top = pq.get()
        cur_node = top[0]
        cur_cost = top[1]
        expendedNodeCost += 1
        # createCell(cur_node[0], cur_node[1], cellSz, mazeHeight, "lightblue")
        if cur_node == goal:
            queue = []
            continue
        for next_node in graph[cur_node]:
            next_cost = heuristic(source, next_node)
            new_cost = cur_cost + next_cost
            if next_node in graph and new_cost < dist[next_node]: 
                dist[next_node] = next_cost + heuristic(next_node, goal) 
                pq.put([next_node, dist[next_node]])
                path[next_node] = cur_node
            

    # Draw path
    cost = drawPath(source, goal, path)
    print("Cost Of Path from Source to Goal: ", cost-1)
    print("Cost of the expanded node: ", expendedNodeCost)

    maze.pack()
    master.mainloop()


if __name__ == '__main__':
    # Breadth_first_search()
    # Uniform_cost_search()
    # Iterative_deeping_search(50)
    # Greedy_best_first_search()
    A_star()

    # print ("Please enter: \n1: Breadth First Search \n2: Uniform Cost Search \n3: Iterative Deepening Search \n4: Greedy Best First Search \n5: A* \n0: Exit")
    # while (1):
    #     value = int(input())
    #     if value == 1:
    #         Breadth_first_search()
    #     elif value == 2:
    #         Uniform_cost_search()
    #     elif  value == 3:
    #         Iterative_deeping_search()
    #     elif value == 4:
    #         Greedy_best_first_search()
    #     elif value == 5:
    #         A_star()
    #     else:
    #         break