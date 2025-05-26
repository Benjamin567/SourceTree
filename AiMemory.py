import json
print("[AiMemory] Received player behavior data")

class AI:



    # Creating attributes

    def __init__(self, name, aggression=0.5, stealth=0.5, memory_limit=100, difficulty=1):
        self.name = name
        self.aggression = aggression
        self.stealth = stealth
        self.memory = []
        self.memory_limit = memory_limit
        self.difficulty = difficulty




    # Getting info on player which also manages memory

	def observe_player(self, player_behavior, attack_used, successful):
		if len(self.memory) >= self.memory_limit:
			self.memory.pop(0)
		player_behavior["attack_used"] = attack_used
		player_behavior["successful"] = successful
			 self.memory.append(player_behavior)



    # AI is deciding a strategy after remembering how many times the player ran vs. hid

    def decide_strategy(self):
        player_hid = sum(1 for x in self.memory if x.get("hid"))
        running = sum(1 for x in self.memory if x.get("ran"))

        if player_hid > running:
            print(f"{self.name}'s stealth attribute is increasing")
            self.stealth += 0.1
        else:
            print(f"{self.name}'s aggression attribute is increasing")
            self.aggression += 0.1

        self.stealth = min(self.stealth, 1.0)
        self.aggression = min(self.aggression, 1.0)



    # Saving the brain by creating a file, then rewriting the file (with all the AI knew and has now learned) after every run

    def save_brain(self, filename="monster_brain.json"):
        with open(filename, "w") as f:
            json.dump({
                "aggression": self.aggression,
                "stealth": self.stealth,
                "memory": self.memory,
                "difficulty": self.difficulty
            }, f)



    # AI gets its memories of player encounters.
    def load_brain(self, filename="monster_brain.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.aggression = data.get("aggression", self.aggression)
                self.stealth = data.get("stealth", self.stealth)
                self.memory = data.get("memory", self.memory)
                self.difficulty = data.get("difficulty", self.difficulty)
                print(f"{self.name}'s brain loaded from file.")
        except FileNotFoundError:
            print("No brain file found — starting fresh.")
            self.save_brain()



    # Difficulty per day
    def level_up(self):
        self.difficulty += 1
        self.aggression += 0.1 * self.difficulty
        self.stealth += 0.1 * self.difficulty
        self.aggression = min(self.aggression, 1.0)
        self.stealth = min(self.stealth, 1.0)
        print(f"{self.name} has leveled up! Difficulty is now {self.difficulty}")



# Create the monster
monster = AI("Forest Stalker")



# Load the brain, and create new if doesn't exist
monster.load_brain()



# Simulate behavior


#!!!! Change for unity later
monster.observe_player(
    {"ran": True, "hid": False, "used_forest": True, "distance_to_player": 7.2},
    attack_used="light_attack",
    successful=True
)


# Adapts
monster.decide_strategy()
monster.level_up()


# Save updated brain to file
monster.save_brain()
