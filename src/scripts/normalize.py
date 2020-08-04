import argparse
import json
import os
import sqlite3
from hashlib import md5
import unicodedata as ud

from common.util.log_helper import LogHelper

LogHelper.setup()
logger = LogHelper.get_logger("FEVERcs Normalize")
BUFFER_SIZE, tmp_file = 100000, ""


def is_fever_db(file):
    try:
        with sqlite3.connect(file) as db:
            db.cursor().execute("SELECT id, text, lines FROM documents LIMIT 1")
            return True
    except sqlite3.DatabaseError:
        return False


def normalize_sqlite(args):
    logger.info('Reading into a temporary database...')
    with sqlite3.connect(args.source_file) as source, sqlite3.connect(tmp_file) as target:
        c_source, c_target = source.cursor(), target.cursor()
        c_target.execute("CREATE TABLE documents (id PRIMARY KEY, text, lines);")
        offset = 0
        while True:
            rows = c_source.execute(
                f"SELECT id, text, lines FROM documents LIMIT {BUFFER_SIZE} OFFSET {offset}").fetchall()
            offset += BUFFER_SIZE
            if len(rows) == 0:
                break
            target.executemany("INSERT INTO documents VALUES (?,?,?)",
                               [[ud.normalize(args.form, column) for column in row] for row in rows])
            logger.info(f"|Processed| = {offset}")
        target.commit()


def normalize_textfile(args):
    with open(args.source_file) as source, open(tmp_file, 'w') as target:
        for line in source:
            target.write(ud.normalize(args.form, line))


def normalize(args):
    global tmp_file
    tmp_file = md5((args.source_file + args.target_file + args.form).encode('utf-8')).hexdigest() + ".db"
    if os.path.exists(tmp_file):
        os.remove(tmp_file)

    if is_fever_db(args.source_file):
        normalize_sqlite(args)
    else:
        normalize_textfile(args)
    os.replace(tmp_file, args.target_file)


if __name__ == '__main__':
    print(os.getcwd())
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', type=str, help='/path/to/source.{db,jsonl}')
    parser.add_argument('target_file', nargs='?', type=str, help='/path/to/target.{db,jsonl}, defaults to source_file',
                        default=None)
    parser.add_argument('--form', type=str, default='NFD',
                        help="Normalization form - defaults to 'NFD'. Valid values are 'NFC', 'NFKC', 'NFD', and 'NFKD'")
    args = parser.parse_args()

    if args.target_file is None:
        args.target_file = args.source_file

    normalize(args)
