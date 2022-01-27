# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GameManager(Document):
	@frappe.whitelist()
	def start_battle(self):
		self.stop_season()

		self.current_player_participation_count = 0
		self.save(ignore_permissions=True)
		
		global_board = frappe.get_doc("Global Board")
		self.clear_board_of_non_participants()

		if len(frappe.get_all("Player", filters={'participated': ['=', True]})) > 0:
			global_board.set_battle_results()
			self.update_player_scores()

	def clear_board_of_non_participants(self):
		all_inactive_players = frappe.get_all("Player", filters={'participated': ['=', False]}, fields=["player_board", "name"])
		for player in all_inactive_players:
			player_board = frappe.get_doc("Player Board", player.player_board)
			player_board.clear_board()

	def update_player_scores(self):
		all_players = frappe.get_all("Player", filters={'participated': ['=', True]}, pluck="name")
		
		for player in all_players:
			player_doc = frappe.get_doc("Player", player)
			
			player_doc.compute_score()
			
			player_doc.new_result_available = True
			player_doc.participated = False
			player_doc.save()

	def get_board_size(self):
		return list(map(int, self.board_size.split(' ')))

	def stop_season(self):
		self.season_paused = True
		self.save(ignore_permissions=True)
		frappe.db.commit()

	def start_season(self):
		self.season_paused = False
		self.save(ignore_permissions=True)
		frappe.db.commit()

	def get_session_players_left(self):
		players_left = self.battle_start_trigger_player_count - self.current_player_participation_count
		return players_left

	def update_session_players_left(self):
		self.current_player_participation_count = (frappe.get_all("Player", filters={'participated': ['=', True]}))
		self.save(ignore_permissions=True)

		if self.current_player_participation_count >= self.battle_start_trigger_player_count:
			self.start_battle()