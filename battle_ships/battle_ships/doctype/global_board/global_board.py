# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GlobalBoard(Document):
	def start_battle(self):
		self.set_global_formation()

	def set_global_formation(self):
		all_player_boards = frappe.get_all("Player Board", fields=['ship_coordinates', 'attack_coordinates'])

		ships = {}
		attacks = {}

		for board in all_player_boards:
			if board.ship_coordinates:
				for coordinate_str in board.ship_coordinates.split(' '):
					if coordinate_str in ships: 
						ships[coordinate_str] += 1
					else:
						ships[coordinate_str] = 1
			if board.attack_coordinates:
				for coordinate_str in board.attack_coordinates.split(' '):
					if coordinate_str in attacks: 
						attacks[coordinate_str] += 1
					else:
						attacks[coordinate_str] = 1

		self.ships = ''
		self.attacks = ''

		for coordinate_str in ships:
			self.ships += f'{coordinate_str}:{ships[coordinate_str]},'

		for coordinate_str in attacks:
			self.attacks += f'{coordinate_str}:{attacks[coordinate_str]},'

		self.ships = self.ships[:-1]
		self.attacks = self.attacks[:-1]

		self.save()