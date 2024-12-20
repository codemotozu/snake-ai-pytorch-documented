# This code implements a reinforcement learning agent to play a Snake game. 
# It uses deep Q-learning with a neural network to predict optimal moves based on the game state. 
# The agent is trained continuously to improve its gameplay over time.

# Dieses Code implementiert einen Verstärkungslern-Agenten, der das Spiel Snake spielt. 
# Es nutzt Deep Q-Learning mit einem neuronalen Netzwerk, um optimale Züge basierend auf dem Spielzustand vorherzusagen. 
# Der Agent wird kontinuierlich trainiert, um sein Spiel zu verbessern.

import torch  # Importing the PyTorch library for deep learning functionalities / Importiert die PyTorch-Bibliothek für Deep-Learning-Funktionen
import random  # Importing the random library to generate random numbers / Importiert die random-Bibliothek zur Erzeugung zufälliger Zahlen
import numpy as np  # Importing NumPy for numerical operations / Importiert NumPy für numerische Operationen
from collections import deque  # Import deque from collections for a queue-like data structure / Importiert deque aus collections für eine warteschlangenartige Datenstruktur
from game import SnakeGameAI, Direction, Point  # Import classes for game logic (SnakeGameAI, Direction, Point) / Importiert Klassen für die Spiellogik (SnakeGameAI, Direction, Point)
from model import Linear_QNet, QTrainer  # Import Q-learning model and trainer / Importiert das Q-Learning Modell und den Trainer
from helper import plot  # Import the plot function for graphing the scores / Importiert die Plot-Funktion zur Darstellung der Ergebnisse

MAX_MEMORY = 100_000  # Maximum size of the memory / Maximale Größe des Speichers
BATCH_SIZE = 1000  # Size of mini-batch for training / Größe der Mini-Batches für das Training
LR = 0.001  # Learning rate for the model / Lernrate für das Modell

class Agent:  # Define the agent class that will control the snake / Definiert die Agentenklasse, die die Schlange steuert
    def __init__(self):  # Initialize the agent / Initialisiert den Agenten
        self.n_games = 0  # Number of games played / Anzahl der gespielten Spiele
        self.epsilon = 0  # Exploration rate (randomness) / Erkundungsrate (Zufälligkeit)
        self.gamma = 0.9  # Discount rate for future rewards / Diskontierungsrate für zukünftige Belohnungen
        self.memory = deque(maxlen=MAX_MEMORY)  # Memory to store previous states / Speicher, um vorherige Zustände zu speichern
        self.model = Linear_QNet(11, 256, 3)  # Neural network model with 11 inputs, 256 hidden units, and 3 outputs / Neuronales Netzwerkmodell mit 11 Eingaben, 256 verborgenen Einheiten und 3 Ausgaben
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)  # Q-learning trainer / Q-Learning-Trainer

    def get_state(self, game):  # Get the current state of the game / Holt den aktuellen Zustand des Spiels
        head = game.snake[0]  # Get the head of the snake / Holt den Kopf der Schlange
        point_l = Point(head.x - 20, head.y)  # Point left of the head / Punkt links vom Kopf
        point_r = Point(head.x + 20, head.y)  # Point right of the head / Punkt rechts vom Kopf
        point_u = Point(head.x, head.y - 20)  # Point above the head / Punkt oberhalb des Kopfes
        point_d = Point(head.x, head.y + 20)  # Point below the head / Punkt unterhalb des Kopfes
        
        # Check the direction of the snake's movement / Überprüft die Richtung der Bewegung der Schlange
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [  # Create the state based on the environment's conditions / Erzeugt den Zustand basierend auf den Bedingungen der Umgebung
            (dir_r and game.is_collision(point_r)) or  # Danger straight (right) / Gefahr geradeaus (rechts)
            (dir_l and game.is_collision(point_l)) or  # Danger straight (left) / Gefahr geradeaus (links)
            (dir_u and game.is_collision(point_u)) or  # Danger straight (up) / Gefahr geradeaus (oben)
            (dir_d and game.is_collision(point_d)),   # Danger straight (down) / Gefahr geradeaus (unten)

            # Danger right / Gefahr rechts
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left / Gefahr links
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction / Bewegungsrichtung
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location / Position der Nahrung
            game.food.x < game.head.x,  # Food is to the left of the snake / Nahrung ist links von der Schlange
            game.food.x > game.head.x,  # Food is to the right of the snake / Nahrung ist rechts von der Schlange
            game.food.y < game.head.y,  # Food is above the snake / Nahrung ist oberhalb der Schlange
            game.food.y > game.head.y  # Food is below the snake / Nahrung ist unterhalb der Schlange
            ]

        return np.array(state, dtype=int)  # Return the state as a NumPy array / Gibt den Zustand als NumPy-Array zurück

    def remember(self, state, action, reward, next_state, done):  # Store experience in memory / Speichert die Erfahrung im Speicher
        self.memory.append((state, action, reward, next_state, done))  # Add to memory, remove the oldest if max memory is reached / Fügt dem Speicher hinzu und entfernt das älteste Element, wenn die maximale Speichergröße erreicht ist

    def train_long_memory(self):  # Train the model with long-term memory / Trainiert das Modell mit langfristigem Gedächtnis
        if len(self.memory) > BATCH_SIZE:  # Check if memory size exceeds batch size / Überprüft, ob die Speichermenge die Batch-Größe überschreitet
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # Sample a random batch from memory / Entnimmt eine zufällige Stichprobe aus dem Speicher
        else:
            mini_sample = self.memory  # If not enough memory, use all memory / Wenn nicht genug Speicher vorhanden ist, wird der gesamte Speicher verwendet

        states, actions, rewards, next_states, dones = zip(*mini_sample)  # Unzip the mini sample into components / Entpackt die Mini-Stichprobe in Komponenten
        self.trainer.train_step(states, actions, rewards, next_states, dones)  # Train the model on the mini batch / Trainiert das Modell mit dem Mini-Batch

    def train_short_memory(self, state, action, reward, next_state, done):  # Train with immediate feedback / Trainiert mit unmittelbarem Feedback
        self.trainer.train_step(state, action, reward, next_state, done)  # Train the model with the single experience / Trainiert das Modell mit der einzelnen Erfahrung

    def get_action(self, state):  # Decide the next action based on the state / Bestimmt die nächste Aktion basierend auf dem Zustand
        self.epsilon = 80 - self.n_games  # Decrease epsilon as the number of games increases (exploration/exploitation trade-off) / Verringert epsilon mit zunehmender Anzahl der Spiele (Erkundung/Exploitation-Abwägung)
        final_move = [0,0,0]  # Initialize the move to all zeros / Initialisiert die Bewegung auf null
        if random.randint(0, 200) < self.epsilon:  # Choose random move based on epsilon / Wählt eine zufällige Bewegung basierend auf epsilon
            move = random.randint(0, 2)  # Randomly choose one of the 3 actions / Wählt zufällig eine der 3 Aktionen
            final_move[move] = 1  # Mark the selected action / Markiert die gewählte Aktion
        else:
            state0 = torch.tensor(state, dtype=torch.float)  # Convert state to a tensor / Wandelt den Zustand in ein Tensor um
            prediction = self.model(state0)  # Get prediction from the model / Holt eine Vorhersage vom Modell
            move = torch.argmax(prediction).item()  # Get the action with the highest prediction / Holt die Aktion mit der höchsten Vorhersage
            final_move[move] = 1  # Mark the selected action / Markiert die gewählte Aktion

        return final_move  # Return the action / Gibt die Aktion zurück


def train():  # Define the training process / Definiert den Trainingsprozess
    plot_scores = []  # List to store scores for plotting / Liste zur Speicherung von Ergebnissen für die Darstellung
    plot_mean_scores = []  # List to store mean scores for plotting / Liste zur Speicherung von Durchschnittsergebnissen für die Darstellung
    total_score = 0  # Variable to track total score / Variable zur Verfolgung der Gesamtergebnisse
    record = 0  # Variable to track the highest score / Variable zur Verfolgung des höchsten Ergebnisses
    agent = Agent()  # Initialize the agent / Initialisiert den Agenten
    game = SnakeGameAI()  # Initialize the game / Initialisiert das Spiel
    while True:  # Start the game loop / Startet die Spielschleife
        state_old = agent.get_state(game)  # Get the old state of the game / Holt den alten Zustand des Spiels

        final_move = agent.get_action(state_old)  # Get the action to take / Holt die Aktion, die ausgeführt werden soll

        reward, done, score = game.play_step(final_move)  # Perform the move and get the result / Führt die Bewegung aus und erhält das Ergebnis
        state_new = agent.get_state(game)  # Get the new state after the move / Holt den neuen Zustand nach der Bewegung

        agent.train_short_memory(state_old, final_move, reward, state_new, done)  # Train with the new data / Trainiert mit den neuen Daten

        agent.remember(state_old, final_move, reward, state_new, done)  # Store the experience in memory / Speichert die Erfahrung im Speicher

        if done:  # Check if the game is over / Überprüft, ob das Spiel zu Ende ist
            game.reset()  # Reset the game / Setzt das Spiel zurück
            agent.n_games += 1  # Increment the number of games played / Erhöht die Anzahl der gespielten Spiele
            agent.train_long_memory()  # Train with the long-term memory / Trainiert mit dem langfristigen Gedächtnis

            if score > record:  # Update the record score if necessary / Aktualisiert das Rekord-Ergebnis, falls erforderlich
                record = score
                agent.model.save()  # Save the model if a new record is set / Speichert das Modell, wenn ein neuer Rekord erreicht wird

            print('Game', agent.n_games, 'Score', score, 'Record:', record)  # Print the game details / Gibt die Spieldetails aus

            plot_scores.append(score)  # Add the score to the plot list / Fügt das Ergebnis zur Plot-Liste hinzu
            total_score += score  # Add to the total score / Addiert zum Gesamtergebnis
            mean_score = total_score / agent.n_games  # Calculate the mean score / Berechnet den Durchschnitt der Ergebnisse
            plot_mean_scores.append(mean_score)  # Add to the plot list for the mean score / Fügt der Plot-Liste das Durchschnittsergebnis hinzu
            plot(plot_scores, plot_mean_scores)  # Plot the results / Stellt die Ergebnisse dar


if __name__ == '__main__':  # Check if the script is being run directly / Überprüft, ob das Skript direkt ausgeführt wird
    train()  # Start the training process / Startet den Trainingsprozess
