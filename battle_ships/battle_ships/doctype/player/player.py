# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class Player(Document):
	def before_insert(self):
		if not self.player_board:
			self.player_board = frappe.new_doc("Player Board").insert(ignore_permissions=True).name

	def update_formation(self, formation):
		formation = json.loads(formation)
		self.participated = True
		self.save(ignore_permissions=True)

		return frappe.get_doc("Player Board", self.player_board).update_formation(formation)
	
	def get_formation(self):
		return frappe.get_doc("Player Board", self.player_board).get_formation()

	def compute_score(self):
		game_manager = frappe.get_doc("Game Manager")
		score = game_manager.base_score

		global_board = frappe.get_doc("Global Board")
		player_board_doc = frappe.get_doc("Player Board", self.player_board)
		
		attacked_coordinates = json.loads(global_board.attacked_coordinates)

		player_ship_coordinates = json.loads(player_board_doc.ship_coordinates)
		player_attack_coordinates = json.loads(player_board_doc.attack_coordinates)

		ships_sank = 0
		for attacked_coordinate in attacked_coordinates:
			for player_ship_coordinate in player_ship_coordinates:
				if attacked_coordinate == player_ship_coordinate:
					ships_sank += 1
		
		score -= (ships_sank * game_manager.score_decrement_for_ships_sank)

		best_ship_coordinates = json.loads(global_board.best_ship_coordinates)

		best_ships = 0
		for best_ship_coordinate in best_ship_coordinates:
			for player_ship_coordinate in player_ship_coordinates:
				if best_ship_coordinate == player_ship_coordinate:
					best_ships += 1

		score += (ships_sank * game_manager.score_increment_for_best_ships)
		
		best_attacks = 0
		for attacked_coordinate in attacked_coordinates:
			for player_attack_coordinate in player_attack_coordinates:
				if attacked_coordinate == player_attack_coordinate:
					best_attacks += 1
		
		score += (ships_sank * game_manager.score_increment_for_best_attacks)

		self.score = score
		self.save(ignore_permissions=True)

	def check_and_get_battle_results(self):
		if self.new_result_available:
			global_board = frappe.get_doc("Global Board")

			ac = json.loads('[]' if global_board.attacked_coordinates == '' else global_board.attacked_coordinates)
			bsc = json.loads('[]' if global_board.best_ship_coordinates == '' else global_board.best_ship_coordinates)

			best_ship_coordinates = []
			attacked_coordinates = []

			for c in ac:
				attacked_coordinates.append(json.loads(c))

			for c in bsc:
				best_ship_coordinates.append(json.loads(c))

			return {
				"score": self.score,
				"attacked_coordinates": attacked_coordinates,
				"best_ship_coordinates": best_ship_coordinates
			}
		else:
			return 'No Result'

	def play_again(self):
		self.new_result_available = False
		self.score = 0
		frappe.get_doc("Player Board", self.player_board).clear_board()
		self.save(ignore_permissions=True)

	def clean_up(self):
		self.new_result_available = False
		self.save()