from pathlib import Path
import argparse
import json
import os
import sys
import unicodedata

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

VOID, TITLE, ABSTRACT = 0, 1, 2


def is_article_beginning(line):
    return line.startswith("<doc")


def is_abstract_ending(line):
    return line.startswith("Section::") or line.startswith("</doc")


if __name__ == '__main__':
    print(os.getcwd())
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', nargs='?', type=str, help='/path/to/source.xml', default='../data/cswiki.xml')
    parser.add_argument('target_file', nargs='?', type=str, help='/path/to/target.jsonl', default='../data/wiki-pages/cswiki-001.jsonl')
    parser.add_argument('--language', type=str, default='czech')
    args = parser.parse_args()
    Path(args.target_file).parent.mkdir(parents=True, exist_ok=True)

    reading, abstract, title = VOID, "", None
    with open(args.source_file, "r") as source_file, open(args.target_file,"w") as target_file:
        for line in source_file:
            if reading == VOID and is_article_beginning(line):
                reading = TITLE
            elif reading == TITLE:
                title = unicodedata.normalize('NFKC', line).strip()
                reading = ABSTRACT
            elif reading and is_abstract_ending(line):
                reading = VOID
                try:
                    sentences = [" ".join(word_tokenize(sentence, language=args.language)) for sentence in sent_tokenize(abstract,"czech")]
                    print(sentences)
                    print(json.dumps({"id": title, "text": " ".join(sentences), "sentences": sentences},
                                     ensure_ascii=False),file=target_file)
                except:
                    print(abstract, file=sys.stderr)
                abstract = ""
            elif reading == ABSTRACT:
                abstract += unicodedata.normalize('NFKC', line)