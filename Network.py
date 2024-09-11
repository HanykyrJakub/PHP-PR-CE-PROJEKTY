import numpy as np
import matplotlib.pyplot as plt

# Activation functions and their derivatives
def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))  

def sigmoid_derivative(x):
    return x * (1 - x)

# Mean Squared Error loss function
def mse_loss(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

# Neural Network Class
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Initialize weights and biases
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_hidden = np.random.randn(hidden_size)
        self.bias_output = np.random.randn(output_size)

    def forward(self, X):
        # Forward pass
        self.hidden_layer_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        self.hidden_layer_output = sigmoid(self.hidden_layer_input)

        self.output_layer_input = np.dot(self.hidden_layer_output, self.weights_hidden_output) + self.bias_output
        self.output_layer_output = sigmoid(self.output_layer_input)

        return self.output_layer_output

    def backward(self, X, y, output, learning_rate):
        # Compute the error
        error_output_layer = y - output
        output_delta = error_output_layer * sigmoid_derivative(output)

        error_hidden_layer = np.dot(output_delta, self.weights_hidden_output.T)
        hidden_delta = error_hidden_layer * sigmoid_derivative(self.hidden_layer_output)

        # Update weights and biases
        self.weights_hidden_output += np.dot(self.hidden_layer_output.T, output_delta) * learning_rate
        self.weights_input_hidden += np.dot(X.T, hidden_delta) * learning_rate
        self.bias_hidden += np.sum(hidden_delta, axis=0) * learning_rate
        self.bias_output += np.sum(output_delta, axis=0) * learning_rate

    def train(self, X, y, epochs, learning_rate):
        # Training process
        loss_history = []
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output, learning_rate)

            # Calculate loss and store it
            loss = mse_loss(y, output)
            loss_history.append(loss)

            if (epoch + 1) % 100 == 0:
                print(f'Epoch {epoch + 1}, Loss: {loss:.4f}')

        return loss_history

# Function to convert temperature (0 to 1 range) to Celsius (-30°C to 50°C)
def normalize_to_celsius(normalized_temp):
    return normalized_temp * (50 - (-30)) + (-30)

# Generate synthetic weather data for training the neural network
def generate_weather_data(n_samples=1000, seed=42):
    np.random.seed(seed)
    temperature = np.random.rand(n_samples)  # Temperature values (0=cold, 1=hot)
    humidity = np.random.rand(n_samples)  # Humidity values (0=dry, 1=humid)
    wind_speed = np.random.rand(n_samples)  # Wind speed values (0=calm, 1=windy)

    # Convert temperature from normalized to Celsius
    temperature_celsius = normalize_to_celsius(temperature)

    # Define rain conditions (arbitrary rule: humidity > 0.6 and wind > 0.3 or temp < 0.3 in normalized range)
    rain_condition = (humidity > 0.6) & (wind_speed > 0.3) | (temperature < 0.3)
    rain = rain_condition.astype(int).reshape(-1, 1)

    weather_data = np.column_stack((temperature_celsius, humidity, wind_speed))
    return weather_data, rain, 'weather'  # Return a flag indicating weather data

# Generate synthetic weight loss data for training the neural network
def generate_weight_loss_data(n_samples=1000, seed=42):
    np.random.seed(seed)
    calories_consumed = np.random.randint(1500, 3000, n_samples)
    calories_burned = np.random.randint(500, 1500, n_samples)
    sleep_duration = np.random.uniform(6, 10, n_samples)
    stress_levels = np.random.uniform(0, 10, n_samples)
    diet_type = np.random.randint(0, 3, n_samples)  # 0: Low-carb, 1: Keto, 2: Mediterranean

    # ... (add more features as needed)

    # Calculate hypothetical weight change based on a simplified model
    weight_change = (calories_consumed - calories_burned) * 0.001 - sleep_duration * 0.05 + stress_levels * 0.02

    weight_data = np.column_stack((calories_consumed, calories_burned, sleep_duration, stress_levels, diet_type))
    return weight_data, weight_change, 'weight'  # Return a flag indicating weight loss data

# Split dataset into train and test
def train_test_split(data, labels, split_ratio=0.8):
    split_index = int(len(data) * split_ratio)
    return data[:split_index], labels[:split_index], data[split_index:], labels[split_index:]

# Main function to integrate everything
def main():
    user_choice = input("Choose prediction type (weather or weight): ")

    if user_choice == 'weather':
        weather_data, rain, _ = generate_weather_data()
        nn_weather = NeuralNetwork(input_size=3, hidden_size=4, output_size=1)

        # Split data into training and testing sets
        train_X, train_y, test_X, test_y = train_test_split(weather_data, rain, split_ratio=0.8)

        # Train the neural network on the weather data
        weather_loss_history = nn_weather.train(train_X, train_y, epochs=3000, learning_rate=0.1)

        # ... (rest of the weather prediction code)
    elif user_choice == 'weight':
        weight_data, weight_change, _ = generate_weight_loss_data()
        nn_weight_loss = NeuralNetwork(input_size=5, hidden_size=8, output_size=1)

        # Split data into training and testing sets
        train_X, train_y, test_X, test_y = train_test_split(weight_data, weight_change, split_ratio=0.8)

        # Train the neural network on the weight loss data
        weight_loss_history = nn_weight_loss.train(train_X, train_y, epochs=3000, learning_rate=0.1)

        # ... (rest of the weight loss prediction code)
    else:
        print("Invalid choice. Please enter 'weather' or 'weight'.")

if __name__ == "__main__":
    main()