extends Node3D

const UDPModule = preload("res://udp.gd")

@export var car_scene: PackedScene
@onready var spawn_point = $SpawnPoint



var connection_established = false

var state = "ensuring_connection"
var udp: UDPModule.UDP_Server


func _ready():
	udp = UDPModule.UDP_Server.new()


func _physics_process(_delta):

	if state == "ensuring_connection":
		udp.send_json(UDPModule.Message.new("Connection", "Connecting_to_PY").data)
		var message_recived = udp.receive_json()
		# print("Received message from Python:", message_recived)
		if message_recived and message_recived["type"] == "Connection" and message_recived["data"] == "Connecting_to_GD":
			print("Handshake successful! We are synchronized.")
			state = "spawn"
		

	elif state == "spawn":
		spawn_cars()
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
		
	
		for car in cars:
			frame_state.append(car.get_state())
			if car.alive:
				cars_alive += 1
		

		
		
		if cars_alive == 0 and cars.size() > 0:
			print("All cars are dead! Resetting generation...")
			udp.send_json(UDPModule.Message.new("Generation_Ended", frame_state).data)

		
			get_tree().call_deferred("reload_current_scene")
	
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




func spawn_cars():
	for i in range(50):
		var car = car_scene.instantiate()
		car.name = str(i)
		add_child(car)
		car.add_to_group("player")
		car.collision_layer = 2 
		car.collision_mask = 1
		car.global_transform = spawn_point.global_transform
