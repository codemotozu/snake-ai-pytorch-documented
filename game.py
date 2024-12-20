import pygame  # Import the Pygame library, which is used for game development  # Importiere die Pygame-Bibliothek, die für die Spieleentwicklung verwendet wird
import random  # Import the random library for generating random numbers, used for food placement  # Importiere die random-Bibliothek zum Erzeugen zufälliger Zahlen, die für die Platzierung von Nahrung verwendet werden
from enum import Enum  # Import Enum class for defining directions as enumerations  # Importiere die Enum-Klasse zur Definition von Richtungen als Enumeration
from collections import namedtuple  # Import namedtuple from collections to create lightweight objects for points  # Importiere namedtuple aus collections, um leichtgewichtige Objekte für Punkte zu erstellen
import numpy as np  # Import NumPy for handling arrays, specifically for movement actions  # Importiere NumPy für den Umgang mit Arrays, insbesondere für Bewegungsaktionen

pygame.init()  # Initialize all Pygame modules  # Initialisiere alle Pygame-Module
font = pygame.font.Font('arial.ttf', 25)  # Load the Arial font at size 25 for rendering text  # Lade die Arial-Schriftart in der Größe 25 zum Darstellen von Text
#font = pygame.font.SysFont('arial', 25)  # Alternative font loading method (commented out)  # Alternative Methode zum Laden der Schriftart (auskommentiert)

class Direction(Enum):  # Define an enumeration for movement directions  # Definiere eine Enumeration für Bewegungsrichtungen
    RIGHT = 1  # Right direction  # Rechte Richtung
    LEFT = 2   # Left direction  # Linke Richtung
    UP = 3     # Up direction  # Oben Richtung
    DOWN = 4   # Down direction  # Unten Richtung

Point = namedtuple('Point', 'x, y')  # Create a named tuple for points with x and y coordinates  # Erstelle ein benanntes Tupel für Punkte mit x- und y-Koordinaten

# rgb colors  # RGB-Farben
WHITE = (255, 255, 255)  # Define the color white  # Definiere die Farbe weiß
RED = (200, 0, 0)        # Define the color red  # Definiere die Farbe rot
BLUE1 = (0, 0, 255)      # Define the color blue (light blue)  # Definiere die Farbe blau (hellblau)
BLUE2 = (0, 100, 255)    # Define a darker blue  # Definiere ein dunkleres Blau
BLACK = (0, 0, 0)        # Define the color black  # Definiere die Farbe schwarz

BLOCK_SIZE = 20  # Set the size of each block in the snake game  # Setze die Größe jedes Blocks im Snake-Spiel
SPEED = 40       # Set the speed of the game (frames per second)  # Setze die Geschwindigkeit des Spiels (Bilder pro Sekunde)

class SnakeGameAI:  # Define the SnakeGameAI class  # Definiere die Klasse SnakeGameAI

    def __init__(self, w=640, h=480):  # Initialize the game with width (w) and height (h)  # Initialisiere das Spiel mit Breite (w) und Höhe (h)
        self.w = w  # Set the width of the screen  # Setze die Breite des Bildschirms
        self.h = h  # Set the height of the screen  # Setze die Höhe des Bildschirms
        # init display  # Initialisiere die Anzeige
        self.display = pygame.display.set_mode((self.w, self.h))  # Create the display window  # Erstelle das Anzeigefenster
        pygame.display.set_caption('Snake')  # Set the title of the window  # Setze den Titel des Fensters
        self.clock = pygame.time.Clock()  # Create a clock object to manage the frame rate  # Erstelle ein Uhrenobjekt zur Steuerung der Framerate
        self.reset()  # Call the reset method to initialize the game state  # Rufe die Methode reset auf, um den Spielzustand zu initialisieren

    def reset(self):  # Reset the game state for a new game  # Setze den Spielzustand für ein neues Spiel zurück
        # init game state  # Initialisiere den Spielzustand
        self.direction = Direction.RIGHT  # Set the initial direction of the snake to the right  # Setze die Anfangsrichtung der Schlange nach rechts

        self.head = Point(self.w/2, self.h/2)  # Set the starting point of the snake's head in the center  # Setze den Startpunkt des Schlangenkopfes in die Mitte
        self.snake = [self.head,  # Initialize the snake with three blocks: head and two body parts  # Initialisiere die Schlange mit drei Blöcken: Kopf und zwei Körperteile
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0  # Set the initial score to 0  # Setze den Anfangspunktestand auf 0
        self.food = None  # Initialize the food as None  # Initialisiere das Essen als None
        self._place_food()  # Call the _place_food method to place the first food  # Rufe die Methode _place_food auf, um das erste Essen zu platzieren
        self.frame_iteration = 0  # Initialize the frame iteration counter  # Initialisiere den Zähler für die Bildwiederholungen

    def _place_food(self):  # Method to randomly place food on the screen  # Methode zum zufälligen Platzieren von Nahrung auf dem Bildschirm
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE )*BLOCK_SIZE  # Generate a random x coordinate for the food  # Generiere eine zufällige x-Koordinate für das Essen
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE )*BLOCK_SIZE  # Generate a random y coordinate for the food  # Generiere eine zufällige y-Koordinate für das Essen
        self.food = Point(x, y)  # Assign the food's coordinates to the food variable  # Weise den Koordinaten des Essens der Variable food zu
        if self.food in self.snake:  # Check if the food is placed on the snake  # Überprüfe, ob das Essen auf der Schlange platziert wurde
            self._place_food()  # If so, recursively call the method again to place the food in another location  # Falls ja, rufe die Methode erneut auf, um das Essen an einer anderen Stelle zu platzieren

    def play_step(self, action):  # Main game loop for each step  # Hauptspielschleife für jeden Schritt
        self.frame_iteration += 1  # Increment the frame iteration  # Erhöhe die Bildwiederholungszahl
        # 1. collect user input  # 1. Benutzer-Eingaben sammeln
        for event in pygame.event.get():  # Get all the events from the Pygame event queue  # Hole alle Ereignisse aus der Pygame-Ereigniswarteschlange
            if event.type == pygame.QUIT:  # If the user closes the game window  # Wenn der Benutzer das Spiel-Fenster schließt
                pygame.quit()  # Quit Pygame  # Beende Pygame
                quit()  # Exit the program  # Beende das Programm
        
        # 2. move  # 2. Bewegung
        self._move(action)  # Call the _move method to update the snake's head position  # Rufe die Methode _move auf, um die Kopfposition der Schlange zu aktualisieren
        self.snake.insert(0, self.head)  # Insert the new head of the snake at the beginning of the snake list  # Füge den neuen Kopf der Schlange am Anfang der Schlangenliste ein
        
        # 3. check if game over  # 3. Überprüfen, ob das Spiel vorbei ist
        reward = 0  # Initialize reward as 0  # Initialisiere Belohnung mit 0
        game_over = False  # Initialize game_over as False  # Initialisiere game_over mit False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):  # If the snake collides with the boundary or itself  # Wenn die Schlange mit der Grenze oder sich selbst kollidiert
            game_over = True  # Set game_over to True  # Setze game_over auf True
            reward = -10  # Assign a negative reward for game over  # Weise eine negative Belohnung für das Spielende zu
            return reward, game_over, self.score  # Return the reward, game over status, and current score  # Gib die Belohnung, den Spielstatus und den aktuellen Punktestand zurück

        # 4. place new food or just move  # 4. Neues Essen platzieren oder nur bewegen
        if self.head == self.food:  # If the snake's head is on the food  # Wenn der Schlangenkopf auf dem Essen ist
            self.score += 1  # Increase the score  # Erhöhe den Punktestand
            reward = 10  # Assign a positive reward  # Weise eine positive Belohnung zu
            self._place_food()  # Place new food  # Platziere neues Essen
        else:
            self.snake.pop()  # Remove the last part of the snake (tail)  # Entferne den letzten Teil der Schlange (Schwanz)
        
        # 5. update ui and clock  # 5. Aktualisiere UI und Uhr
        self._update_ui()  # Update the game UI  # Aktualisiere die Spiel-Oberfläche
        self.clock.tick(SPEED)  # Control the frame rate  # Steuere die Framerate
        # 6. return game over and score  # 6. Gib Spielende und Punktestand zurück
        return reward, game_over, self.score  # Return the reward, game over status, and current score  # Gib die Belohnung, den Spielstatus und den aktuellen Punktestand zurück

    def is_collision(self, pt=None):  # Check for collisions with boundaries or the snake itself  # Überprüfe Kollisionen mit den Grenzen oder der Schlange selbst
        if pt is None:  # If no point is provided, use the snake's head  # Wenn kein Punkt angegeben ist, verwende den Schlangenkopf
            pt = self.head  # Set pt to the snake's head  # Setze pt auf den Schlangenkopf
        # hits boundary  # Kollision mit der Grenze
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:  # If the point hits the screen boundary  # Wenn der Punkt die Bildschirmgrenze trifft
            return True  # Return True for collision  # Gib True für eine Kollision zurück
        # hits itself  # Kollision mit sich selbst
        if pt in self.snake[1:]:  # If the point is part of the snake's body (excluding the head)  # Wenn der Punkt Teil des Körpers der Schlange ist (außer dem Kopf)
            return True  # Return True for collision  # Gib True für eine Kollision zurück

        return False  # Return False if no collision  # Gib False zurück, wenn keine Kollision vorliegt

    def _update_ui(self):  # Method to update the user interface  # Methode zum Aktualisieren der Benutzeroberfläche
        self.display.fill(BLACK)  # Fill the screen with black color  # Fülle den Bildschirm mit schwarzer Farbe

        for pt in self.snake:  # For each point in the snake  # Für jeden Punkt in der Schlange
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))  # Draw the snake's body part  # Zeichne das Körperteil der Schlange
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))  # Draw a smaller rectangle for the snake's body  # Zeichne ein kleineres Rechteck für das Körperteil der Schlange

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))  # Draw the food  # Zeichne das Essen

        text = font.render("Score: " + str(self.score), True, WHITE)  # Render the score text  # Render den Punktestand-Text
        self.display.blit(text, [0, 0])  # Blit the text onto the screen  # Blit den Text auf den Bildschirm
        pygame.display.flip()  # Update the display  # Aktualisiere die Anzeige

    def _move(self, action):  # Method to move the snake based on the action  # Methode zum Bewegen der Schlange basierend auf der Aktion
        # [straight, right, left]  # [gerade, rechts, links]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]  # List of directions in clockwise order  # Liste der Richtungen im Uhrzeigersinn
        idx = clock_wise.index(self.direction)  # Get the current direction index  # Hole den aktuellen Richtungsindex

        if np.array_equal(action, [1, 0, 0]):  # If action is straight (no change)  # Wenn die Aktion geradeaus (keine Veränderung) ist
            new_dir = clock_wise[idx]  # No change in direction  # Keine Änderung der Richtung
        elif np.array_equal(action, [0, 1, 0]):  # If action is right turn  # Wenn die Aktion ein Rechtsabbiegen ist
            next_idx = (idx + 1) % 4  # Move to the next direction in clockwise  # Bewege dich zur nächsten Richtung im Uhrzeigersinn
            new_dir = clock_wise[next_idx]  # Set the new direction  # Setze die neue Richtung
        else:  # If action is left turn  # Wenn die Aktion ein Linksabbiegen ist
            next_idx = (idx - 1) % 4  # Move to the previous direction in clockwise  # Bewege dich zur vorherigen Richtung im Uhrzeigersinn
            new_dir = clock_wise[next_idx]  # Set the new direction  # Setze die neue Richtung

        self.direction = new_dir  # Update the snake's direction  # Aktualisiere die Richtung der Schlange

        x = self.head.x  # Get the current x position of the head  # Hole die aktuelle x-Position des Kopfes
        y = self.head.y  # Get the current y position of the head  # Hole die aktuelle y-Position des Kopfes
        if self.direction == Direction.RIGHT:  # If the direction is right  # Wenn die Richtung nach rechts ist
            x += BLOCK_SIZE  # Move the head to the right  # Bewege den Kopf nach rechts
        elif self.direction == Direction.LEFT:  # If the direction is left  # Wenn die Richtung nach links ist
            x -= BLOCK_SIZE  # Move the head to the left  # Bewege den Kopf nach links
        elif self.direction == Direction.DOWN:  # If the direction is down  # Wenn die Richtung nach unten ist
            y += BLOCK_SIZE  # Move the head downwards  # Bewege den Kopf nach unten
        elif self.direction == Direction.UP:  # If the direction is up  # Wenn die Richtung nach oben ist
            y -= BLOCK_SIZE  # Move the head upwards  # Bewege den Kopf nach oben

        self.head = Point(x, y)  # Update the head's position  # Aktualisiere die Kopfposition
