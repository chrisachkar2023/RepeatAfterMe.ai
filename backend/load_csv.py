import sqlite3
import csv

conn = sqlite3.connect('words.db')
cur = conn.cursor()

with open('backend/word_difficulty.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        cur.execute('INSERT INTO words (word, difficulty) VALUES (?, ?)', (row[0], row[1]))

conn.commit()
conn.close()
