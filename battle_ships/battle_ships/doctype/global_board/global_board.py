# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class GlobalBoard(Document):
	def start_battle(self):
		self.set_global_formation()
		self.normalize_board()

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

		self.max_ships = 0
		self.min_ships = 0

		self.max_attacks = 0
		self.min_attacks = 0

		for coordinate_str in ships:
			if self.max_ships < ships[coordinate_str]:
				self.max_ships = ships[coordinate_str]
			elif self.min_ships > ships[coordinate_str]:
				self.min_ships = ships[coordinate_str]	

		for coordinate_str in attacks:
			if self.max_attacks < attacks[coordinate_str]:
				self.max_attacks = attacks[coordinate_str]
			elif self.min_attacks > attacks[coordinate_str]:
				self.min_attacks = attacks[coordinate_str]

		self.ships = json.dumps(ships)
		self.attacks = json.dumps(attacks)

		self.save()

	def normalize_board(self):
		normalized_ships = {}
		normalized_attacks = {}

		ships = json.loads(self.ships)
		attacks = json.loads(self.attacks)

		if self.ships:
			for coordinate in ships:
				coordinate
				count = ships[coordinate]
				normalized_ships[coordinate] = ((count - self.min_ships) / self.max_ships)

		if self.attacks:
			for coordinate in attacks:
				count = attacks[coordinate]
				normalized_attacks[coordinate] = ((count - self.min_attacks) / self.max_attacks)
		
		self.normalized_ships = json.dumps(normalized_ships)
		self.normalized_attacks = json.dumps(normalized_attacks)

		self.save()