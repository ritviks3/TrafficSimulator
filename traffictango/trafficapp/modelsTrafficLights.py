class TrafficLight:
    def __init__(self, name, initial_state="red", green_duration=60, yellow_duration=5, red_duration=30):
        self.name = name
        self.states = ["green", "yellow", "red"]
        self.state = initial_state  # Current state of the traffic light
        self.green_duration = green_duration  # Duration of green light in seconds
        self.yellow_duration = yellow_duration  # Duration of yellow light in seconds
        self.red_duration = red_duration  # Duration of red light in seconds
        self.timer = 0  # Timer to track the time in the current state

    def change_state(self, new_state):
        #Change the state of the traffic light
        self.state = new_state

    def update(self):
        #Update the traffic light's state based on a predefined cycle
        if self.state == "green":
            if self.timer >= self.green_duration:
                self.change_state("yellow")
                self.timer = 0
            else:
                self.timer += 1
        elif self.state == "yellow":
            if self.timer >= self.yellow_duration:
                self.change_state("red")
                self.timer = 0
            else:
                self.timer += 1
        elif self.state == "red":
            if self.timer >= self.red_duration:
                self.change_state("green")
                self.timer = 0
            else:
                self.timer += 1

    def __str__(self):
        return f"Traffic Light {self.name}: {self.state}"