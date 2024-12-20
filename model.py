import torch  # Import the PyTorch library for tensor operations (English) / Importiere die PyTorch-Bibliothek für Tensoroperationen (Deutsch)
import torch.nn as nn  # Import the neural network module from PyTorch (English) / Importiere das Modul für neuronale Netzwerke von PyTorch (Deutsch)
import torch.optim as optim  # Import the optimization module from PyTorch (English) / Importiere das Optimierungsmodul von PyTorch (Deutsch)
import torch.nn.functional as F  # Import the functional module for neural network operations (English) / Importiere das funktionale Modul für neuronale Netzwerkoperationen (Deutsch)
import os  # Import the OS library for interacting with the operating system (English) / Importiere die OS-Bibliothek für die Interaktion mit dem Betriebssystem (Deutsch)

class Linear_QNet(nn.Module):  # Define a class for the neural network model (English) / Definiere eine Klasse für das neuronale Netzwerkmodell (Deutsch)
    def __init__(self, input_size, hidden_size, output_size):  # Initialize the model with input, hidden, and output layer sizes (English) / Initialisiere das Modell mit Eingabe-, versteckten und Ausgabeschichtgrößen (Deutsch)
        super().__init__()  # Call the parent class constructor (English) / Rufe den Konstruktor der Elternklasse auf (Deutsch)
        self.linear1 = nn.Linear(input_size, hidden_size)  # Define the first linear layer (English) / Definiere die erste lineare Schicht (Deutsch)
        self.linear2 = nn.Linear(hidden_size, output_size)  # Define the second linear layer (English) / Definiere die zweite lineare Schicht (Deutsch)

    def forward(self, x):  # Define the forward pass method for the network (English) / Definiere die Vorwärtsmethode für das Netzwerk (Deutsch)
        x = F.relu(self.linear1(x))  # Apply ReLU activation to the first linear layer (English) / Wende die ReLU-Aktivierung auf die erste lineare Schicht an (Deutsch)
        x = self.linear2(x)  # Pass through the second linear layer (English) / Gehe durch die zweite lineare Schicht (Deutsch)
        return x  # Return the output of the network (English) / Gebe die Ausgabe des Netzwerks zurück (Deutsch)

    def save(self, file_name='model.pth'):  # Define a method to save the model (English) / Definiere eine Methode zum Speichern des Modells (Deutsch)
        model_folder_path = './model'  # Set the folder path to store the model (English) / Setze den Ordnerpfad zum Speichern des Modells (Deutsch)
        if not os.path.exists(model_folder_path):  # Check if the model folder exists (English) / Überprüfe, ob der Modellordner existiert (Deutsch)
            os.makedirs(model_folder_path)  # Create the model folder if it doesn't exist (English) / Erstelle den Modellordner, wenn er nicht existiert (Deutsch)

        file_name = os.path.join(model_folder_path, file_name)  # Join the folder path and filename (English) / Verbinde den Ordnerpfad und den Dateinamen (Deutsch)
        torch.save(self.state_dict(), file_name)  # Save the model's state dictionary (English) / Speichere das Zustandsdiktat des Modells (Deutsch)


class QTrainer:  # Define a class for training the Q-learning model (English) / Definiere eine Klasse für das Trainieren des Q-Learning-Modells (Deutsch)
    def __init__(self, model, lr, gamma):  # Initialize the trainer with model, learning rate, and gamma (English) / Initialisiere den Trainer mit Modell, Lernrate und Gamma (Deutsch)
        self.lr = lr  # Set the learning rate (English) / Setze die Lernrate (Deutsch)
        self.gamma = gamma  # Set the discount factor (English) / Setze den Rabattfaktor (Deutsch)
        self.model = model  # Assign the model to the trainer (English) / Weise das Modell dem Trainer zu (Deutsch)
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)  # Set the optimizer (Adam) for training (English) / Setze den Optimierer (Adam) für das Training (Deutsch)
        self.criterion = nn.MSELoss()  # Define the loss function (Mean Squared Error) (English) / Definiere die Verlustfunktion (Mittlere quadratische Abweichung) (Deutsch)

    def train_step(self, state, action, reward, next_state, done):  # Define the training step method (English) / Definiere die Trainingsschritt-Methode (Deutsch)
        state = torch.tensor(state, dtype=torch.float)  # Convert the state to a PyTorch tensor (English) / Konvertiere den Zustand in einen PyTorch-Tensor (Deutsch)
        next_state = torch.tensor(next_state, dtype=torch.float)  # Convert the next state to a tensor (English) / Konvertiere den nächsten Zustand in einen Tensor (Deutsch)
        action = torch.tensor(action, dtype=torch.long)  # Convert the action to a tensor (English) / Konvertiere die Aktion in einen Tensor (Deutsch)
        reward = torch.tensor(reward, dtype=torch.float)  # Convert the reward to a tensor (English) / Konvertiere die Belohnung in einen Tensor (Deutsch)

        if len(state.shape) == 1:  # Check if the state is a 1D array (English) / Überprüfe, ob der Zustand ein 1D-Array ist (Deutsch)
            state = torch.unsqueeze(state, 0)  # Add an extra dimension for batch processing (English) / Füge eine zusätzliche Dimension für die Stapelverarbeitung hinzu (Deutsch)
            next_state = torch.unsqueeze(next_state, 0)  # Add extra dimension to next state (English) / Füge eine zusätzliche Dimension für den nächsten Zustand hinzu (Deutsch)
            action = torch.unsqueeze(action, 0)  # Add extra dimension to action (English) / Füge eine zusätzliche Dimension für die Aktion hinzu (Deutsch)
            reward = torch.unsqueeze(reward, 0)  # Add extra dimension to reward (English) / Füge eine zusätzliche Dimension für die Belohnung hinzu (Deutsch)
            done = (done, )  # Ensure done is a tuple (English) / Stelle sicher, dass done ein Tupel ist (Deutsch)

        pred = self.model(state)  # Predict Q values using the current model and state (English) / Sage die Q-Werte mit dem aktuellen Modell und Zustand voraus (Deutsch)

        target = pred.clone()  # Clone the predicted Q values (English) / Klone die vorhergesagten Q-Werte (Deutsch)
        for idx in range(len(done)):  # Loop through all the actions (English) / Schleife durch alle Aktionen (Deutsch)
            Q_new = reward[idx]  # Initialize Q_new with the current reward (English) / Initialisiere Q_new mit der aktuellen Belohnung (Deutsch)
            if not done[idx]:  # If the episode is not done (English) / Wenn die Episode noch nicht beendet ist (Deutsch)
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))  # Calculate Q_new using the discount factor (English) / Berechne Q_new unter Verwendung des Rabattfaktors (Deutsch)

            target[idx][torch.argmax(action[idx]).item()] = Q_new  # Update the target Q value for the selected action (English) / Aktualisiere den Ziel-Q-Wert für die ausgewählte Aktion (Deutsch)

        self.optimizer.zero_grad()  # Reset the gradients for the optimizer (English) / Setze die Gradienten für den Optimierer zurück (Deutsch)
        loss = self.criterion(target, pred)  # Calculate the loss between the target and the predicted Q values (English) / Berechne den Verlust zwischen dem Ziel und den vorhergesagten Q-Werten (Deutsch)
        loss.backward()  # Backpropagate the loss (English) / Rückpropagiere den Verlust (Deutsch)

        self.optimizer.step()  # Update the model weights based on the gradients (English) / Aktualisiere die Modellgewichte basierend auf den Gradienten (Deutsch)




