import pygame  # imports the pygame module, used for creating games (importiert das pygame-Modul, das für die Erstellung von Spielen verwendet wird)
import random  # imports the random module, used for generating random numbers (importiert das random-Modul, das zur Erzeugung von Zufallszahlen verwendet wird)
from enum import Enum  # imports the Enum class from the enum module to create enumerations (importiert die Enum-Klasse aus dem enum-Modul zur Erstellung von Aufzählungen)
from collections import namedtuple  # imports namedtuple from collections for creating simple classes (importiert namedtuple aus collections zur Erstellung von einfachen Klassen)

pygame.init()  # initializes the pygame module (initialisiert das pygame-Modul)
font = pygame.font.Font('arial.ttf', 25)  # initializes the font for displaying text (initialisiert die Schriftart für die Textanzeige)
# font = pygame.font.SysFont('arial', 25)  # alternative way to set font (alternative Möglichkeit, die Schriftart festzulegen)

class Direction(Enum):  # creates an enumeration for the four possible directions (erstellt eine Aufzählung für die vier möglichen Richtungen)
    RIGHT = 1  # right direction (Rechte Richtung)
    LEFT = 2  # left direction (Linke Richtung)
    UP = 3  # up direction (Obere Richtung)
    DOWN = 4  # down direction (Untere Richtung)
    
Point = namedtuple('Point', 'x, y')  # defines a named tuple 'Point' with x and y coordinates (definiert ein benanntes Tupel 'Point' mit den Koordinaten x und y)

# rgb colors  (rgb Farben)
WHITE = (255, 255, 255)  # white color (weiße Farbe)
RED = (200, 0, 0)  # red color (rote Farbe)
BLUE1 = (0, 0, 255)  # blue color (blaue Farbe)
BLUE2 = (0, 100, 255)  # darker blue color (dunklere blaue Farbe)
BLACK = (0, 0, 0)  # black color (schwarze Farbe)

BLOCK_SIZE = 20  # size of each block in the snake (Größe jedes Blocks in der Schlange)
SPEED = 20  # game speed (Spielgeschwindigkeit)

class SnakeGame:  # defines the SnakeGame class (definiert die SnakeGame-Klasse)
    
    def __init__(self, w=640, h=480):  # constructor initializing the game dimensions (Konstruktor, der die Spielfeldgröße initialisiert)
        self.w = w  # width of the game screen (Breite des Spiels)
        self.h = h  # height of the game screen (Höhe des Spiels)
        # init display (initialisiert die Anzeige)
        self.display = pygame.display.set_mode((self.w, self.h))  # sets the game window size (legt die Fenstergröße des Spiels fest)
        pygame.display.set_caption('Snake')  # sets the window title (legt den Fenstertitel fest)
        self.clock = pygame.time.Clock()  # creates a clock object to control game speed (erstellt ein Uhr-Objekt, um die Spielgeschwindigkeit zu steuern)
        
        # init game state (initialisiert den Spielzustand)
        self.direction = Direction.RIGHT  # initial direction (anfängliche Richtung)
        
        self.head = Point(self.w / 2, self.h / 2)  # initial snake head position (anfängliche Position des Schlangenkopfes)
        self.snake = [self.head,  # list storing all the snake segments (Liste, die alle Segmente der Schlange speichert)
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        
        self.score = 0  # initialize score (initialisiert den Punktestand)
        self.food = None  # food position (Position des Essens)
        self._place_food()  # places the first food (platziert das erste Essen)
        
    def _place_food(self):  # places food at a random location (platziert das Essen an einer zufälligen Position)
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE  # random x-coordinate (zufällige x-Koordinate)
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE  # random y-coordinate (zufällige y-Koordinate)
        self.food = Point(x, y)  # assign food to a point (weist dem Essen einen Punkt zu)
        if self.food in self.snake:  # if food appears on snake's body, place again (wenn das Essen auf dem Körper der Schlange erscheint, platziere es erneut)
            self._place_food()
        
    def play_step(self):  # main game logic for each step (Hauptspiel-Logik für jeden Schritt)
        # 1. collect user input (1. Benutzer-Eingaben erfassen)
        for event in pygame.event.get():  # loop through all events (Schleife durch alle Ereignisse)
            if event.type == pygame.QUIT:  # if the user closes the window (wenn der Benutzer das Fenster schließt)
                pygame.quit()  # quit pygame (beendet pygame)
                quit()  # exit the program (beendet das Programm)
            if event.type == pygame.KEYDOWN:  # if a key is pressed (wenn eine Taste gedrückt wird)
                if event.key == pygame.K_LEFT:  # if left arrow key is pressed (wenn die linke Pfeiltaste gedrückt wird)
                    self.direction = Direction.LEFT  # change direction to left (ändert die Richtung nach links)
                elif event.key == pygame.K_RIGHT:  # if right arrow key is pressed (wenn die rechte Pfeiltaste gedrückt wird)
                    self.direction = Direction.RIGHT  # change direction to right (ändert die Richtung nach rechts)
                elif event.key == pygame.K_UP:  # if up arrow key is pressed (wenn die obere Pfeiltaste gedrückt wird)
                    self.direction = Direction.UP  # change direction to up (ändert die Richtung nach oben)
                elif event.key == pygame.K_DOWN:  # if down arrow key is pressed (wenn die untere Pfeiltaste gedrückt wird)
                    self.direction = Direction.DOWN  # change direction to down (ändert die Richtung nach unten)
        
        # 2. move (2. bewegen)
        self._move(self.direction)  # update the head position (aktualisiert die Position des Schlangenkopfes)
        self.snake.insert(0, self.head)  # add the new head to the snake (fügt den neuen Kopf zur Schlange hinzu)
        
        # 3. check if game over (3. prüfen, ob das Spiel vorbei ist)
        game_over = False  # set initial game over state (setzt den initialen Zustand "Spiel vorbei" auf False)
        if self._is_collision():  # check if collision occurs (prüft, ob eine Kollision auftritt)
            game_over = True  # if collision happens, game over (wenn eine Kollision passiert, Spiel vorbei)
            return game_over, self.score  # return the game over state and score (gibt den "Spiel vorbei"-Zustand und den Punktestand zurück)
            
        # 4. place new food or just move (4. neues Essen platzieren oder einfach bewegen)
        if self.head == self.food:  # if snake head reaches food (wenn der Schlangenkopf das Essen erreicht)
            self.score += 1  # increase score (erhöht den Punktestand)
            self._place_food()  # place new food (platziert neues Essen)
        else:
            self.snake.pop()  # remove the last segment of the snake (entfernt das letzte Segment der Schlange)
        
        # 5. update ui and clock (5. UI und Uhr aktualisieren)
        self._update_ui()  # update the game display (aktualisiert die Spielanzeige)
        self.clock.tick(SPEED)  # control the speed of the game (kontrolliert die Spielgeschwindigkeit)
        
        # 6. return game over and score (6. gibt "Spiel vorbei" und Punktestand zurück)
        return game_over, self.score
    
    def _is_collision(self):  # checks if there is a collision (prüft, ob eine Kollision vorliegt)
        # hits boundary (stößt an den Rand)
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True  # returns True if the snake hits the boundary (gibt True zurück, wenn die Schlange den Rand berührt)
        # hits itself (stößt gegen sich selbst)
        if self.head in self.snake[1:]:  # if head collides with any other part of the snake (wenn der Kopf mit einem anderen Teil der Schlange kollidiert)
            return True  # returns True if the snake hits itself (gibt True zurück, wenn die Schlange sich selbst trifft)
        
        return False  # returns False if no collision (gibt False zurück, wenn keine Kollision vorliegt)
        
    def _update_ui(self):  # updates the game display (aktualisiert die Spielanzeige)
        self.display.fill(BLACK)  # fill the screen with black color (füllt den Bildschirm mit schwarzer Farbe)
        
        for pt in self.snake:  # loop through all snake segments (Schleife durch alle Segmente der Schlange)
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))  # draw the snake body (zeichnet den Körper der Schlange)
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))  # draw snake inner body (zeichnet den inneren Körper der Schlange)
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))  # draw the food (zeichnet das Essen)
        
        text = font.render("Score: " + str(self.score), True, WHITE)  # render score as text (rendert den Punktestand als Text)
        self.display.blit(text, [0, 0])  # display the score on the screen (zeigt den Punktestand auf dem Bildschirm an)
        pygame.display.flip()  # update the display (aktualisiert die Anzeige)
        
    def _move(self, direction):  # moves the snake in the given direction (bewegt die Schlange in die gegebene Richtung)
        x = self.head.x  # get current x-coordinate (holt die aktuelle x-Koordinate)
        y = self.head.y  # get current y-coordinate (holt die aktuelle y-Koordinate)
        if direction == Direction.RIGHT:  # if the direction is right (wenn die Richtung nach rechts ist)
            x += BLOCK_SIZE  # move head to the right (bewegt den Kopf nach rechts)
        elif direction == Direction.LEFT:  # if the direction is left (wenn die Richtung nach links ist)
            x -= BLOCK_SIZE  # move head to the left (bewegt den Kopf nach links)
        elif direction == Direction.DOWN:  # if the direction is down (wenn die Richtung nach unten ist)
            y += BLOCK_SIZE  # move head down (bewegt den Kopf nach unten)
        elif direction == Direction.UP:  # if the direction is up (wenn die Richtung nach oben ist)
            y -= BLOCK_SIZE  # move head up (bewegt den Kopf nach oben)
            
        self.head = Point(x, y)  # update the head position (aktualisiert die Kopfposition)
            

if __name__ == '__main__':  # start the game (startet das Spiel)
    game = SnakeGame()  # create a new game object (erstellt ein neues Spielobjekt)
    
    # game loop (Spiel-Schleife)
    while True:  # infinite loop until the game is over (unendliche Schleife bis das Spiel vorbei ist)
        game_over, score = game.play_step()  # run a step of the game (führt einen Schritt des Spiels aus)
        
        if game_over == True:  # if the game is over (wenn das Spiel vorbei ist)
            break  # exit the loop (bricht die Schleife ab)
        
    print('Final Score', score)  # print the final score (zeigt den Endpunktestand an)
        
        
    pygame.quit()  # quit pygame (beendet pygame)
