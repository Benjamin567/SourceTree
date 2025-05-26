from AiMemory import AI
import tensorflow as tf
import numpy as np
print("[AiBrain] Neural network running prediction...")
monster = AI("Forest Stalker")
monster.load_brain()
memory = monster.memory

memory = [
    {"ran": False, "hid": True,  "used_forest": False, "distance_to_player": 2.4, "attack_used": "ambush",       "successful": True},
    {"ran": True,  "hid": False, "used_forest": True,  "distance_to_player": 6.8, "attack_used": "charge",       "successful": True},
    {"ran": False, "hid": False, "used_forest": False, "distance_to_player": 1.1, "attack_used": "light_attack", "successful": True},
    {"ran": True,  "hid": True,  "used_forest": True,  "distance_to_player": 9.3, "attack_used": "charge",       "successful": True},
    {"ran": False, "hid": True,  "used_forest": True,  "distance_to_player": 3.1, "attack_used": "ambush",       "successful": True},
    {"ran": True,  "hid": False, "used_forest": False, "distance_to_player": 5.5, "attack_used": "charge",       "successful": False},
    {"ran": False, "hid": False, "used_forest": True,  "distance_to_player": 2.2, "attack_used": "light_attack", "successful": True},
    {"ran": True,  "hid": True,  "used_forest": False, "distance_to_player": 8.0, "attack_used": "ambush",       "successful": False},
    {"ran": False, "hid": False, "used_forest": False, "distance_to_player": 1.6, "attack_used": "light_attack", "successful": True},
    {"ran": True,  "hid": False, "used_forest": True,  "distance_to_player": 7.1, "attack_used": "charge",       "successful": True},
    {"ran": True,  "hid": True,  "used_forest": True,  "distance_to_player": 9.8, "attack_used": "charge",       "successful": False},
    {"ran": False, "hid": True,  "used_forest": False, "distance_to_player": 3.5, "attack_used": "ambush",       "successful": True},
    {"ran": False, "hid": False, "used_forest": True,  "distance_to_player": 1.9, "attack_used": "light_attack", "successful": True},
    {"ran": True,  "hid": False, "used_forest": False, "distance_to_player": 5.9, "attack_used": "charge",       "successful": False},
    {"ran": True,  "hid": True,  "used_forest": False, "distance_to_player": 8.7, "attack_used": "ambush",       "successful": True},
    {"ran": False, "hid": False, "used_forest": False, "distance_to_player": 1.3, "attack_used": "light_attack", "successful": False},
    {"ran": True,  "hid": False, "used_forest": True,  "distance_to_player": 6.5, "attack_used": "charge",       "successful": True},
    {"ran": False, "hid": True,  "used_forest": True,  "distance_to_player": 2.8, "attack_used": "ambush",       "successful": False},
    {"ran": False, "hid": False, "used_forest": False, "distance_to_player": 1.0, "attack_used": "light_attack", "successful": True},
    {"ran": True,  "hid": True,  "used_forest": True,  "distance_to_player": 9.6, "attack_used": "charge",       "successful": True},
]


filtered_memory = [data for data in memory if data["successful"]]


attack_to_index = {
    "ambush": 0,
    "charge": 1,
    "light_attack": 2
}





#.items tells python that attack_to_index is a pair. This line of code is swaping input with output, by making v:k (like a dictionary), from k:v.
index_to_attack = {v: k for k, v in attack_to_index.items()}

inputs = []
outputs = []

for data in filtered_memory: 
	input_vector = [
		1 if data["ran"] else 0,
		1 if data["hid"] else 0,
		1 if data["used_forest"] else 0,
		data["distance_to_player"]
	]
	inputs.append(input_vector)
	attack_index = attack_to_index[data["attack_used"]]
	outputs.append(attack_index)


X = np.array(inputs)  #Inputs: player behaviour data
Y = np.array(outputs) # Outputs: which attack was used
		
model = tf.keras.models.Sequential([  # The model is the AI/nerual network

    tf.keras.layers.Input(shape=(4,)),  # Input layer: expects 4 input values (ran, hid, used_forest, distance)

    tf.keras.layers.Dense(8, activation='relu'),  # Hidden layer: 8 neurons using ReLU (zeroes out negatives)

    tf.keras.layers.Dense(3, activation='softmax')  # Output layer: 3 attack options, softmax turns them into probabilities
])

model.compile(
    optimizer='adam',                          # Optimizer that adjusts weights to reduce errors (smart gradient descent), adam is the smartest auto adjuster to the weights
    loss='sparse_categorical_crossentropy',    # loss function tells the AI how far its last prediction was. Spare gives a single number output representing data conditions, categorical_crossentropy punishes wrong guesses, and rewards confident correct ones  
    metrics=['accuracy']                       # Tracks how often the model predicts correctly
)


model.fit(X, Y, epochs=50) #epochs trains the data sets, in this case 50 times, and tracks its accuracy. .fit uses the inputs to train the AI into giving a good output.



new_situation = np.array([[1, 0, 1, 6.3]])  # ran, not hid, used forest, distance

prediction = model.predict(new_situation)

predicted_index = np.argmax(prediction[0])  # Get the index of the highest probability
predicted_attack = index_to_attack[predicted_index]

print(f"The AI predicts the best attack is: {predicted_attack}")

return predicted_attack


