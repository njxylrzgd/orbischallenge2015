from __future__ import generators
from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.MapOutOfBoundsException import *
from math import *


class PlayerAI:
    isInEnemyLOS = False
    isInBulletTrajectory = False
    isInTurretLaserTrajectory = False
    isInTurretLOS = False
    isGettingHit = False
    isEnemyInLOS = False
    map = {}
    initself = False
    closest_turret = None
    desiredPath = []
    pathToTurret = []

    def __init__(self):
        # Initialize any objects or variables you need here.
        isInEnemyLOS = False
        isInBulletTrajectory = False
        isInTurretLaserTrajectory = False
        isInTurretLOS = False
        isGettingHit = False
        isEnemyInLOS = False

    def get_move(self, gameboard, player, opponent):
        '''
        First step of any turn is to refresh the values of each tile on the board. 
        Tile values are affected by things like turret firing in an upcoming turn, walls, power-ups, and opponent.
        
        The following is a weighted FSM. Our AI values safety over aggression.
        The AI selects the next move in the following order, depending on opportunity:
        
        1. Check if you’re in the line of sight of your enemy
        2. Check for bullets in your two tiles proximity S
        3. Avoid getting shot by turrets S
        4. Check for power ups nearby
        4. Look if you can get in the line of sight of a turret
        5. See if power up available/necessary
        
        '''

        #check if in enemy line of sight, then get out of the way
        if(isInLineOfSight(opponent, player.x, player.y, gameboard)):
            return dipLah(opponent.direction, player.direction, self.map[(player.x,player.y)])
                
        #check if in bullet or laser intercept trajectory, then get out of the way
        for turret in gameboard.turrets:
            if(isInProximity(turret, player.x, player.y, 5, gameboard)):
                if(isInLineOfSight(turret, player.x, player.y, gameboard)):
                    if(turret.x == player.x):
                        return dipLah('LEFT' if turret.x > player.x else 'RIGHT', player.direction, self.map[(player.x,player.y)])
                    if(turret.y == player.y):
                        return dipLah('UP' if turret.y < player.y else 'DOWN', player.direction, self.map[(player.x,player.y)])
        
        for bullet in gameboard.bullets:
            if(isInProximity(bullet, player.x, player.y, 2, gameboard)):
                if(isInLineOfSight(bullet, player.x, player.y, gameboard)):
                    return dipLah(bullet.direction, player.direction, self.map[(player.x,player.y)])

        #check if laser is in line of sight, then shoot
        for turret in gameboard.turrets:
            if(isInLineOfSight(player, turret.x, turret.y, gameboard)):
                return Move.SHOOT

        #if there's a power up nearby
        for powerUp in gameboard.power_ups:
            if(isInProximity(powerUp, player.x, player.y, 2, gameboard)):
                moves = shortestPath(map, (player.x, player.y), (powerUp.x, powerUp.y))
                return determineDirection(player, moves[0])
        for powerUp in gameboard.power_ups:
            if(isInProximity(powerUp, player.x, player.y, 6, gameboard)):
                moves = shortestPath(map, (player.x, player.y), (powerUp.x, powerUp.y))
                return determineDirection(player, moves[0])
        for powerUp in gameboard.power_ups:
            if(isInProximity(powerUp, player.x, player.y, 9, gameboard)):
                moves = shortestPath(map, (player.x, player.y), (powerUp.x, powerUp.y))
                return determineDirection(player, moves[0])
        for powerUp in gameboard.power_ups:
            moves = shortestPath(map, (player.x, player.y), (powerUp.x, powerUp.y))
            return determineDirection(player, moves[0])
            #compute shortest path to it
        #if there's a power up in the map

            #compute shortest path to it
        
        if not self.initself:        
            self.initself = True
            for x in range(gameboard.width):
                for y in range(gameboard.height):
                    self.map[(x,y)] = {}
                    if not gameboard.is_wall_at_tile((x + 1) % gameboard.width, y):
                        self.map[(x,y)][(1,0)] = 1
                    if not gameboard.is_wall_at_tile((x - 1 + gameboard.width) % gameboard.width, y):
                        self.map[(x,y)][(-1,0)] = 1
                    if not gameboard.is_wall_at_tile(x, (y + 1) % gameboard.height):
                        self.map[(x,y)][(0,1)] = 1
                    if not gameboard.is_wall_at_tile(x, (y - 1 + gameboard.height) % gameboard.height):
                        self.map[(x,y)][(0,-1)] = 1
        
        if not gameboard.is_wall_at_tile((player.x + 1) % gameboard.width, player.y):
            if player.direction == 'RIGHT':
                self.map[(player.x,player.y)][(1,0)] = 1
            else:
                self.map[(player.x,player.y)][(1,0)] = 2
        if not gameboard.is_wall_at_tile((player.x - 1 + gameboard.width) % gameboard.width, player.y):
            if player.direction == 'LEFT':
                self.map[(player.x,player.y)][(-1,0)] = 1
            else:
                self.map[(player.x,player.y)][(-1,0)] = 2
        if not gameboard.is_wall_at_tile(player.x, (player.y - 1 + gameboard.height) % gameboard.height):
            if player.direction == 'UP':
                self.map[(player.x,player.y)][(0, -1)] = 1
            else:
                self.map[(player.x,player.y)][(0, -1)] = 2
        if not gameboard.is_wall_at_tile(player.x, (player.y + 1) % gameboard.height):
            if player.direction == 'DOWN':
                self.map[(player.x,player.y)][(0,1)] = 1
            else:
                self.map[(player.x,player.y)][(0,1)]  = 2
        

        
        return Move.NONE

    def isInProximity(currentCoordinate, targetCoordinateX, targetCoordinateY, radius, gameboard):
        '''
        check if the current object and target object are within radius of each other
        '''
        euclideanDistance = math.pow(math.pow(currentCoordinate.x - targetCoordinateX, 2) + \
            math.pow(currentCoordinate.y - targetCoordinateY, 2), 0.5)
        wrapAroundDistance = math.pow(math.pow((gameboard.height - (currentCoordinate.x - targetCoordinateX)), 2) + \
            math.pow((gameboard.height - (currentCoordinate.y - targetCoordinateY)), 2), 0.5)

        if euclideanDistance < radius or wrapAroundDistance < radius:
            return True
        return False

    def determineDirection(player, targetCoordinate):
        '''
        target coordinate - (x, y)
        player - player obj
        determines next move for player to get to the target 
        '''
        if player.x == targetCoordinate[0]:
            if player.x > targetCoordinate[0]:
                if player.direction != 'LEFT':
                    return Move.FACE_LEFT
                else:
                    return Move.FORWARD
            else:
                if player.direction != 'RIGHT':
                    return Move.FACE_RIGHT
                else:
                    return Move.FORWARD
        if player.y == targetCoordinate[1]:
            if player.y > targetCoordinate[1]:
                if player.direction != 'DOWN':
                    return Move.FACE_DOWN
                else:
                    return Move.FORWARD
            else:
                if player.direction != 'UP':
                    return Move.FACE_UP
                else:
                    return Move.FORWARD

    def isInLineOfSight(player, targetCoordinateX, targetCoordinateY, gameboard):
        if(isinstance(player, 'Player') or isinstance(player,'Bullet')):
            if(player.direction == 'RIGHT'):
                for i in range(0, gameboard.width - player.x):
                    if((player.x + i) == targetCoordinateX):
                        return True
                    if(gameboard.is_wall_at_tile(player.x + i, player.y) or gameboard.is_turret_at_tile(player.x + i, player.y)):
                        return False
            if(player.direction == 'LEFT'):
                for i in range(0, player.x):
                    if((player.x - i) == targetCoordinateX):
                        return True
                    if(gameboard.is_wall_at_tile(player.x - i, player.y) or gameboard.is_turret_at_tile(player.x - i, player.y)):
                        return False
            if(player.direction == 'UP'):
                for i in range(0, gameboard.height  - player.y):
                    if((player.y + i) == targetCoordinateY):
                        return True
                    if(gameboard.is_wall_at_tile(player.x, player.y + i) or gameboard.is_turret_at_tile(player.x, player.y + i)):
                        return False
            if(player.direction == 'DOWN'):
                for i in range(0, player.y):
                    if((player.y - i) == targetCoordinateY):
                        return True
                    if(gameboard.is_wall_at_tile(player.x, player.y - i) or gameboard.is_turret_at_tile(player.x, player.y - i)):
                        return False
        elif (isinstance(player, 'Turret')):
            if(player.x == targetCoordinateX):
                for i in range(0, gameboard.width - player.x if (gameboard.width - player.x < 5) else 5):
                    if((player.x + i) == targetCoordinateX):
                        return True
                    if(gameboard.is_wall_at_tile(player.x + i, player.y)):
                        return False
                for i in range(0, player.x if (player.x < 5) else 5):
                    if((player.x - i) == targetCoordinateX):
                        return True
                    if(gameboard.is_wall_at_tile(player.x - i, player.y)):
                        return False
            if(player.y == targetCoordinateY):
                for i in range(0, gameboard.height  - player.y  if (gameboard.height - player.y < 5) else 5):
                    if((player.y + i) == targetCoordinateY):
                        return True
                    if(gameboard.is_wall_at_tile(player.x, player.y + i)):
                        return False
                for i in range(0, player.y if (player.y < 5) else 5):
                    if((player.y - i) == targetCoordinateY):
                        return True
                    if(gameboard.is_wall_at_tile(player.x, player.y - i)):
                        return False
        return False

#taken from http://code.activestate.com/recipes/117228-priority-dictionary/
class priorityDictionary(dict):
    def __init__(self):
        '''Initialize priorityDictionary by creating binary heap
        of pairs (value,key).  Note that changing or removing a dict entry will
        not remove the old pair from the heap until it is found by smallest() or
        until the heap is rebuilt.'''
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        '''Find smallest item after removing deleted items from heap.'''
        if len(self) == 0:
            raise IndexError
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while 1:
                smallChild = 2*insertionPoint+1
                if smallChild+1 < len(heap) and \
                        heap[smallChild] > heap[smallChild+1]:
                    smallChild += 1
                if smallChild >= len(heap) or lastItem <= heap[smallChild]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild
        return heap[0][1]

    def __iter__(self):
        '''Create destructive sorted iterator of priorityDictionary.'''
        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]
        return iterfn()

    def __setitem__(self,key,val):
        '''Change value stored in dictionary and add corresponding
        pair to heap.  Rebuilds the heap if the number of deleted items grows
        too large, to avoid memory leakage.'''
        dict.__setitem__(self,key,val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v,k) for k,v in self.iteritems()]
            self.__heap.sort()  # builtin sort likely faster than O(n) heapify
        else:
            newPair = (val,key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and \
                    newPair < heap[(insertionPoint-1)//2]:
                heap[insertionPoint] = heap[(insertionPoint-1)//2]
                insertionPoint = (insertionPoint-1)//2
            heap[insertionPoint] = newPair

    def setdefault(self,key,val):
        '''Reimplement setdefault to call our customized __setitem__.'''
        if key not in self:
            self[key] = val
        return self[key]

# Dijkstra's algorithm for shortest paths
# David Eppstein, UC Irvine, 4 April 2002

# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228
def Dijkstra(G,start,end=None):
	"""
	Find shortest paths from the  start vertex to all vertices nearer than or equal to the end.

	The input graph G is assumed to have the following representation:
	A vertex can be any object that can be used as an index into a dictionary.
	G is a dictionary, indexed by vertices.  For any vertex v, G[v] is itself a dictionary,
	indexed by the neighbors of v.  For any edge v->w, G[v][w] is the length of the edge.
	This is related to the representation in <http://www.python.org/doc/essays/graphs.html>
	where Guido van Rossum suggests representing graphs as dictionaries mapping vertices
	to lists of outgoing edges, however dictionaries of edges have many advantages over lists:
	they can store extra information (here, the lengths), they support fast existence tests,
	and they allow easy modification of the graph structure by edge insertion and removal.
	Such modifications are not needed here but are important in many other graph algorithms.
	Since dictionaries obey iterator protocol, a graph represented as described here could
	be handed without modification to an algorithm expecting Guido's graph representation.

	Of course, G and G[v] need not be actual Python dict objects, they can be any other
	type of object that obeys dict protocol, for instance one could use a wrapper in which vertices
	are URLs of web pages and a call to G[v] loads the web page and finds its outgoing links.
	
	The output is a pair (D,P) where D[v] is the distance from start to v and P[v] is the
	predecessor of v along the shortest path from s to v.
	
	Dijkstra's algorithm is only guaranteed to work correctly when all edge lengths are positive.
	This code does not verify this property for all edges (only the edges examined until the end
	vertex is reached), but will correctly compute shortest paths even for some graphs with negative
	edges, and will raise an exception if it discovers that a negative edge has caused it to make a mistake.
	"""

	D = {}	# dictionary of final distances
	P = {}	# dictionary of predecessors
	Q = priorityDictionary()	# estimated distances of non-final vertices
	Q[start] = 0
	
	for v in Q:
		D[v] = Q[v]
		if v == end: break
		
		for w in G[v]:
			vwLength = D[v] + G[v][w]
			if w in D:
				if vwLength < D[w]:
					raise ValueError
			elif w not in Q or vwLength < Q[w]:
				Q[w] = vwLength
				P[w] = v
	
	return (D,P)
			
def shortestPath(G,start,end):
	"""
	Find a single shortest path from the given start vertex to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along the shortest path.
	"""

	D,P = Dijkstra(G,start,end)
	Path = []
	while 1:
		Path.append(end)
		if end == start: break
		end = P[end]
	Path.reverse()
	return Path
