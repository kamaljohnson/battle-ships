
import frappe

# cron task
def start_battle():
    frappe.get_doc("Game Manager").start_battle()
