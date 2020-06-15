import json
import sqlite3

INSERT = 'INSERT INTO documents(id,text,lines) VALUES (?,?,?)'
with open("fever_cs.jsonl") as jsonl:
    conn = sqlite3.connect('fever_cs.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS documents (id PRIMARY KEY, text, lines)')
    values = []
    for line in jsonl:
        article = json.loads(line)
        sentences = "\n".join(f"{k}\t{v}" for k, v in zip(range(len(article["sentences"])), article["sentences"]))
        cur.execute(INSERT, (article["id"], article["text"], sentences))
    conn.commit()
    conn.close()
