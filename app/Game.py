"""Process all game data. Handles getting in new board states, analyzing snake
health, and providing Main with the best next move."""

from Snake import Snake
from Board import Board


class Game:
    """Allow for several Battlesnake games to be played at once by providing
    several different Game objects.

    Has following attributes:
    weightGrid      (board)     - Board object
    width           (int)       - Board width
    height          (int)       - Board height
    you             (string)    - UUID representing what our snake's ID is
    food   (array)     - array of coord arrays
    turn            (int)       - 0-indexed int representing completed turns
    dead_snakes     (array)     - array of Snake objects that no longer compete"""

    def __init__(self, data):
        """Initialize the Game class.

        param1: dictionary - all data from /start POST.
        """
        self.weightGrid = Board(data['width'], data['height'])
        self.width = data['width']
        self.height = data['height']

        self.snakes = {}
        self.you = ''
        self.food = []
        self.turn = 0
        self.deadSnakes = []

    def update(self, data):
        """Update game with current board from server.

        param1: dictionary - all data from response. See Battlesnake docs
        for more info."""
        for snakeData in data['snakes']:
            if snakeData['id'] in self.snakes:
                self.snakes[snakeData['id']].update(snakeData)
            else:
                self.snakes[snakeData['id']] = Snake(snakeData)

        self.food = data['food']
        self.you = data['you']
        if 'dead_snakes' in data:
            self.deadSnakes = data['dead_snakes']


    def getNextMove(self):
        """"Use all algorithms to determine the next best move for our snake."""
        bestNode = self.weightGrid.getNodeWithPriority(1)

        return bestNode

        #TODO
            #Run each algorithm to make decisions
            #Find best route to desired square
            #Ensure boundary is not selected (shouldn't be an issue since we
            # would only head towards positively weighted squares anyway and
            # boundary square do not exist according to algorithm)
            #If several candidates, pick one at random
            #Return decision


    def weightNotHitSnakes(self):
        """Weight grid to avoid snake hitting other snakes and it self"""
        us = self.snakes[self.you] #Represents our snakes
        ourSnakePos = us.getAllPositions()
        ourTail = ourSnakePos[-1] #[[x, y],[x,y]]=
        ourTailX = ourTail[0]
        ourTailY = ourTail[1]

        for s in self.snakes:
            positions = s.getAllPositions()
            for x in positions:
                for y in positions[x]:
                    pos = x+','+y
                    self.weightGrid.setWeight(pos, 0)
        #TODO
        #Weight self as 0
        #Are we getting food this move? (Do we need to weight our tail 0)
            #Check if head position is in old food positions.
        #Weight other snakes as 0
        #Are they getting food this move? (Do we need to weigh their tails 0)
        #Are they dying this move?
        #How big are they? Don't block heads of small snakes

    def weightFood(self):
        """Weight grid with food necessity"""
        #TODO
            #How desperately do we need food
            #Goes through all food and returns the closest according to optimumPath
        foodCoord = 0
        pathLength = 500
        shortestPath = 0
        closestFoodCoord = 0
        oursnake = self.snakes[self.you]
        head = oursnake.getHeadPosition()
        health = oursnake.getHealth()
        for foodCoords in self.food:
            pathLength = len(self.weightGrid.optimumPath(head, foodCoords))
            if pathLength < shortestPath:
                shortestPath = pathLength
                closestFoodCoord = foodCoord

            foodCoord += 1
            foodWeight = 100 - health - pathLength
            self.weightGrid.setWeight(foodCoords,foodWeight)
        if health > 30:
            return False


        return self.weightGrid.optimumPath(head, self.food[closestFoodCoord])




    def weightSmallSnakes(self):
        """Positively weight smaller snakes for murdering purposes"""
        #TODO
            #Compare size
            #How long will it take to get to the snake?
            #How much food is around for the snake to grow?


    def weightLargeSnakes(self):
        """Negativly weight squares where large snake heads could move to next round"""
        #TODO
            #Compare size
            #Can we get food and grow bigger?


    def weightEnclosedSpaces(self):
        """Do not kill ourselves by picking a corner where we trap ourselves"""
        #TODO
            #How long are we?
            #Are we giving other people the opportunity to block off our exit?
            #What is the optimal traversal path to maximize future space opportunities
            #Don't limit our moves (against a surface) unless advantageous or necessary


    def weightTrapSnakes(self):
        """Positively weight squares that will allow us to block other snakes off"""
        #TODO
            #How long are they?
            #How much traversal room are we leaving them?
            #Do they need food? Do they have it in the trapped location?
            #How long are we? Can we effectively block them for long enough?

# Example code testing
if __name__ == '__main__':
    INITDATA = {"width": 20, "height": 20, "game_id": "b1dadee8-a112-4e0e-afa2-2845cd1f21aa"}
    b = Game(INITDATA)
    b.weightGrid.showCombiner(b.getNextMove(), True, False)
    print b.getNextMove()
