# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt


from frappe.utils import datetime
import frappe
from frappe.model.document import Document

class GameManager(Document):
	@frappe.whitelist()
	def start_battle(self):	
		# TODO: Lock the season, no more updates when in battle	

		global_board = frappe.get_doc("Global Board")
		self.clear_board_of_non_participants()

		if len(frappe.get_all("Player", filters={'participated': ['=', True]})) > 0:
			global_board.set_battle_results()
			self.update_player_scores()

		self.current_player_participation_count = 0
		self.battle_start_time = (datetime.datetime.now() + datetime.timedelta(days=1))
		self.save()

	def clear_board_of_non_participants(self):
		all_inactive_players = frappe.get_all("Player", filters={'participated': ['=', False]}, pluck="name")
		for player in all_inactive_players:
			player_doc = frappe.get_doc("Player", player)
			player_doc.clean_up()
			player_board = frappe.get_doc("Player Board", player_doc.player_board)
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

	def get_battle_start_time(self):
		return self.battle_start_time