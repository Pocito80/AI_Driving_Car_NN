extends Node3D

const UDPModule = preload("res://udp.gd")

@export var car_scene: PackedScene
@onready var track_path_node: Path3D = $TrackPath
@onready var spawn_point = $SpawnPoint
# @onready var spawn_point


var connection_established = false

var state = "ensuring_connection"
var udp: UDPModule.UDP_Server
var game_values

func _ready():
	udp = UDPModule.UDP_Server.new()


func _physics_process(_delta):

	if state == "ensuring_connection":
		udp.send_json(UDPModule.Message.new("Connection", "Connecting_to_PY").data)
		var message_recived = udp.receive_json()
		# print("Received message from Python:", message_recived)
		if message_recived and message_recived["type"] == "Connection" and message_recived["data"] == "Connecting_to_GD":
			print("Handshake successful! We are synchronized.")
			state = "reciving_paramiters"
		
	elif state == "reciving_paramiters":
		var message_recived = udp.receive_json()
		if message_recived and message_recived["type"] == "Paramiters":
			print("Received model parameters from Python.")
			udp.send_json(UDPModule.Message.new("Paramiters", "Paramiters_received").data)
			game_values = message_recived["data"]
			Engine.time_scale = int(game_values["game_speed"])
			if game_values["map"] == "map_2":
				spawn_point = $SpawnPoint2
				track_path_node = $TrackPath2
			state = "spawn"
			# print(game_values["model_parameters"]["number_of_agents"])

	elif state == "spawn":
		spawn_cars(int(game_values["model_paramiters"]["number_of_agents"]))
		state = "running"	
	
	elif state == "running":

		# print(Engine.get_frames_per_second())
		
		while udp.udp.get_available_packet_count() > 0:
			var message_recived = udp.receive_json()
			
			if message_recived and message_recived["type"] == "Commands":
				var commands = message_recived["data"]
				# print("Received commands:", commands)
				distribute_commands(commands)

		var frame_state = []
		var cars_alive = 0
		var cars = get_tree().get_nodes_in_group("player")
		
		# print(cars)
		for car in cars:
			frame_state.append(car.get_state())
			if car.alive:
				cars_alive += 1
		

		
		
		if cars_alive == 0 and cars.size() > 0:
			print("All cars are dead! Resetting generation...")
			udp.send_json(UDPModule.Message.new("Generation_Ended", frame_state).data)

		
			get_tree().call_deferred("reload_current_scene")
			# state = "ensure_connection"
	
		udp.send_json(UDPModule.Message.new("FleetState", frame_state).data)
			
	
func distribute_commands(commands: Dictionary):

	var cars = get_tree().get_nodes_in_group("player")
	var commands_map: Dictionary = commands
	commands_map = commands["data"]
	
	for car in cars:
		var car_actions = commands_map[car.name]
		var throttle = car_actions[0][0]
		var steering = car_actions[0][1]
		car.apply_ai_command(throttle, steering)




func spawn_cars(number_of_agents):
	for i in range(number_of_agents):
		var car = car_scene.instantiate()
		car.track_path = track_path_node
		car.spawn_point = spawn_point
		car.setup(int(game_values["model_paramiters"]["raycast_number"]))
		car.name = str(i)
		add_child(car)
		car.add_to_group("player")
		car.collision_layer = 2 
		car.collision_mask = 1
		car.global_transform = spawn_point.global_transform
