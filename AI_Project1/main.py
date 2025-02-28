#A* algorithm for romanian cities
import csv
from tkinter import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

#Ensures points are relative to the canvas center
CENTER_X = CANVAS_WIDTH // 2
CENTER_Y = CANVAS_HEIGHT // 2

#Zooms in and out
MULTIPLIER = 20

#All city names can be found in folder Heuristics.csv
START_CITY = "Arad"
END_CITY =  "Bucuresti"





class City:
    def __init__(self, name):
        self.name = name
        self.connections = {}
        self.heuristics = None
        self.x = 0
        self.y = 0
        self.getData()
        self.gScore = float('inf')
        self.fScore = float('inf')


    def __repr__(self):
        return f"<City {self.name}>"

    def getHeuristics(self):
        return self.heuristics

    def getName(self):
        return self.name

    def getConnections(self):
        return self.connections

    def getfScore(self):
        return self.fScore

    def getgScore(self):
        return self.gScore


    #Retrieves city data (connections) from the Data.csv file
    def getData(self):
        #Accepted csv format: cityA,cityB,road_distance(number)
        with open('Data.csv', 'r',newline='\n') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] == self.name:
                    self.connections.update({row[1]: int(row[2])})
                elif row[1] == self.name:
                    self.connections.update({row[0]: int(row[2])})


        with open('Heuristics.csv','r',newline='\n') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] == self.name:
                    self.heuristics = int(row[1])
                    self.x = float(row[2])
                    self.y = float(row[3])

#Uses City type as nodes
class Graph:
    def __init__(self,Cities):
        self.Cities = Cities
        self.connections = {}
        self.addCites()


    def addCites(self):
        for city in self.Cities:
            #Dict keys (strings) to dict values (City)

            currentCity = self.Cities[city] #City object

            self.connections[currentCity] = {}

            keys = currentCity.connections.keys()
            for key in keys:
                self.connections[currentCity][self.Cities[key]] = currentCity.getConnections()[key]

    def printGraph(self):
        print(self.connections)

    def getCities(self):
        return self.connections


#Uses City type as elements of the minHeap
class MinHeap:
    def __init__(self,cities = None):
        self.list = []

        if cities != None:
            for city in cities:
                self.add(cities[city])

    def __contains__(self, node):
        return node in self.list

    def add(self,node):
        self.list.append(node)

        if(len(self.list) > 1):
            self.bubbleUp()

    def update(self,node,value):
        if node.getfScore() < value:
            node.fScore = value
            self.bubbleDown()

    def bubbleUp(self):

        #(i-1)//2 parent
        #2*i + 1 left child
        #2*i + 2 right child

        index = len(self.list)-1 #last element
        parent = (index-1) // 2  #parent



        while index > 0 and self.list[parent].getfScore() > self.list[index].getfScore():

            #Do the swap
            temp = self.list[index]
            self.list[index] = self.list[parent]
            self.list[parent] = temp

            index = parent
            parent = (index-1) // 2

    def bubbleDown(self,index = None):
        if index is None:
            index = 0


        #First compare the children
        while True:
            childL = index * 2 + 1
            childR = index * 2 + 2
            smaller_index = index


            #Has no left child
            if childL > len(self.list) - 1:
                break

            #Has left child but no right child
            if childR > (len(self.list) - 1):
                    if self.list[childL].getfScore() < self.list[index].getfScore():

                        temp = self.list[index]
                        self.list[index] = self.list[childL]
                        self.list[childL] = temp
                    break


            #Has both left and right (find the smallest between the children)
            if self.list[childL].getfScore() <= self.list[childR].getfScore():
                smaller_index = childL
            else:
                smaller_index = childR


            #Compare smaller index with the parent
            if self.list[smaller_index].fScore < self.list[index].fScore:
                temp = self.list[index]
                self.list[index] = self.list[smaller_index]
                self.list[smaller_index] = temp
                index = smaller_index

            else:
                break

    def heapify(self):
        start_index = (len(self.list) // 2) - 1

        for index in range(start_index, -1, -1):
            self.bubbleDown(index)

    def pop(self):

        if len(self.list) == 0:
            return None

        if len(self.list) == 1:
            return self.list.pop()

        to_return = self.list[0]

        self.list[0] = self.list[-1]
        self.list.pop()

        self.bubbleDown()

        return to_return

    def printMinHeap(self):
        print("\n------minHeap-----")
        for node in self.list:
            print(node, node.fScore)
        print("------minHeap-----\n")

class MapPoint:
    def __init__(self,x,y):
        self.x = x
        self.y = y
#Generate the cities based on the city list
def generateCities(city_list):
    return_list = {}
    for city in city_list:
        return_list.update({city: City(city)})
    return return_list

#Get the heuristics (the distance from each city to Bucharest)
def getHeuristics():
    return_dic = {}
    with open('Heuristics.csv', 'r',newline='\n') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            return_dic.update({row[0]: row[1]})

    return return_dic

#Get the names of the city from the heuristics dictionary
def getCityList(dictionary):
    return_list = []
    for city in dictionary:
        return_list.append(city)

    return return_list


def reconstructPath(dict,current):
    path = [current]
    while current in dict:
        current = dict[current]
        path.insert(0, current)
    return path



def A_Star(start_city, end_city,cities):



    graphClass = Graph(cities)      #Graph is {City : {City: Distance}} style
    graph = graphClass.getCities()
    prev = {}  # {City : City}

    openList = MinHeap()
    openList.add(start_city)


    start_city.gScore = 0
    start_city.fScore = start_city.getHeuristics()


    #Yield is used to pass the required values in order to update the visualizer at every step

    while len(openList.list) > 0:
        openList.printMinHeap()
        current = openList.pop()
        print(current.getName(), current.getfScore())

        yield None, reconstructPath(prev, current), None

        if current == end_city:

            yield reconstructPath(prev, current), None , None

        for neighbor in graph[current].keys():

            distance = graph[current][neighbor]               #Distance from current to neighbor
            tentative_gScore =  current.getgScore() + distance

            yield current, neighbor, reconstructPath(prev, current)

            if tentative_gScore < neighbor.getgScore():


                prev[neighbor] = current
                neighbor.gScore = tentative_gScore
                neighbor.fScore = tentative_gScore + neighbor.getHeuristics()

                yield current,neighbor,reconstructPath(prev, current)

                if neighbor not in openList:
                    openList.add(neighbor)
                else:
                    openList.heapify()


def plotPoint(city,canvas,color = "blue",size = 12):
    #Compute the coordinates relative to the canvas center
    canvas_x = CENTER_X + city.x * MULTIPLIER
    canvas_y = CENTER_Y - city.y * MULTIPLIER


    canvas.create_oval(canvas_x + size/2, canvas_y + size/2, canvas_x - size/2, canvas_y - size/2, fill=color)
    canvas.create_text(canvas_x - 10, canvas_y - 15, text=city.getName())
    canvas.create_text(canvas_x -20, canvas_y + 20, text=city.fScore)


def plotCityPoints(cities,canvas):
    for city in cities.values():
        plotPoint(city,canvas)


def drawLine(city1,city2,canvas,color = "black",width = 1):
    canvas_x1 = CENTER_X + city1.x * MULTIPLIER
    canvas_y1 = CENTER_Y - city1.y * MULTIPLIER
    canvas_x2 = CENTER_X + city2.x * MULTIPLIER
    canvas_y2 = CENTER_Y - city2.y * MULTIPLIER

    canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill=color,width=width)


def plotCityConnections(connections,canvas):

    for city in connections:
        for connection in connections[city]:
            drawLine(city,connection,canvas)


def drawCurrentPath(path,canvas):
        for i in range(1, len(path)):
            drawLine(path[i - 1], path[i], canvas, color="blue", width=2)


def visualiser(generator, canvas, cities,connections):
#This will update the canvas at each step.


    try:
        arg1, arg2, arg3 = next(generator)  # Get the next step in the algorithm
        #Codes: arg1 = None => arg2 is a path to be drawn
            #   arg2 = None => algorithm finished.
            #   else: arg1 = current point, arg2 = neighbor
            #   arg3 is used to draw the shortest path known so far


        canvas.delete("all")
        plotCityConnections(connections,canvas)
        plotCityPoints(cities,canvas)


        if arg2 is None:
            #Get in this case when the A* is done with a path.
            for i in range(1,len(arg1)):
                drawLine(arg1[i-1],arg1[i],canvas,color="green",width=3)
            print("A* Algorithm Finished!")
            return


        elif arg1 is None:
            # This draws the path
            drawCurrentPath(arg2,canvas)

        else:

            plotPoint(arg1,canvas,color="yellow")
            drawCurrentPath(arg3, canvas)
            drawLine(arg1, arg2, canvas, "red",3)




        canvas.after(1000, visualiser, generator, canvas,cities,connections)

    except StopIteration:

        print("A* Algorithm Finished!")

#Helper functions
def modifyDistanceByPercentage(percentage):
    # relative to 0,0
    with open('Heuristics.csv', 'r',newline='\n') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            new_row = row[0]+","+row[1]+","+str(float(row[2])*percentage)+","+str(float(row[3])*percentage)
            print (new_row)
def shiftPositionOnAxis(axis,distance):
    if axis == 'x' or axis == 'X':
        with open('Heuristics.csv', 'r', newline='\n') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                new_row = row[0] +","+row[1]+","+str(float(row[2])+distance)+","+row[3]
                print(new_row)
    if axis == 'y' or axis == 'Y':
        with open('Heuristics.csv', 'r', newline='\n') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                new_row = row[0] +","+row[1]+","+row[2]+","+str(float(row[3])+distance)
                print(new_row)


def main():

    heuristics = getHeuristics()                        #Heuristics (type Strings)
    cities = generateCities(getCityList(heuristics))    #Nodes (type Cities)
    graph = Graph(cities)                               #Graph (Connections + Nodes)

    root = Tk()
    canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    heap_frame = Frame(root, width=200, height=CANVAS_HEIGHT)

    canvas.pack(side=LEFT)
    heap_frame.pack(side=RIGHT)

    plotCityPoints(cities,canvas)
    plotCityConnections(graph.connections,canvas)

    generator = A_Star(cities[START_CITY], cities[END_CITY], cities)

    canvas.after(1000,visualiser,generator,canvas,cities,graph.connections)

    root.mainloop()





if __name__ == '__main__':
    main()




