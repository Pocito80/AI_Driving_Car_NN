class Message:
	var data: Variant

	func _init(type: String = "", content: Variant = null) -> void:
		self.data = {"type": type, "data": content}

class UDP_Server:
	var udp: PacketPeerUDP

	func _init(host: String = "127.0.0.1", listen_port: int = 4243, send_port: int = 4242):
		self.udp = PacketPeerUDP.new()
		self.udp.bind(listen_port)
		self.udp.connect_to_host(host, send_port)

	func send_json(data: Variant) -> void:
		var json_data = JSON.stringify(data)
		self.udp.put_packet(json_data.to_utf8_buffer())

	func receive_json():
		if self.udp.get_available_packet_count() > 0:
			var raw_data = self.udp.get_packet().get_string_from_utf8()
			var parsed = JSON.parse_string(raw_data)
			return parsed

	func send_message(message: String) -> void:
		self.send_json(message)

	func receive_message():
		if self.udp.get_available_packet_count() > 0:
			var raw_data = self.udp.get_packet().get_string_from_utf8()
			return raw_data
