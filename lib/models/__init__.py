import sqlite3

CONN = sqlite3.connect('inventory_management.db')
CURSOR = CONN.cursor()
