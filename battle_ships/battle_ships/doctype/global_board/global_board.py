# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class GlobalBoard(Document):
	def set_battle_results(self):
		self.set_global_formation()
		self.normalize_board()
		self.set_attacked_coordinates()
		self.set_best_ship_coordinates()

		game_manager = frappe.get_doc("Game Manager")
		game_manager.start_season()

	def set_global_formation(self):
		all_player_boards = frappe.get_all("Player Board", fields=['ship_coordinates', 'attack_coordinates'])

		ships = {}
		attacks = {}

		board_size = frappe.get_doc("Game Manager").get_board_size()

		for i in range(board_size[0]):
			for j in range(board_size[1]):
				ships[f'{i}{j}'] = 0
				attacks[f'{i}{j}'] = 0

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

	def set_attacked_coordinates(self):
		normalized_attacks = json.loads(self.normalized_attacks)
		
		attacked_coordinates = []

		for coordinate in normalized_attacks:
			if normalized_attacks[coordinate] >= 0.5:
				attacked_coordinates.append(coordinate)
		
		self.attacked_coordinates = json.dumps(attacked_coordinates)
		self.save()

	def set_best_ship_coordinates(self):
		normalized_attacks = json.loads(self.normalized_attacks)
		
		best_ship_coordinates = []

		for coordinate in normalized_attacks:
			if normalized_attacks[coordinate] == 0:
				best_ship_coordinates.append(coordinate)
		
		self.best_ship_coordinates = json.dumps(best_ship_coordinates)
		self.save()