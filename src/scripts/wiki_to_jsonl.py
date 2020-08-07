import argparse
import json
import os
import sys
import unicodedata
from pathlib import Path
import nltk

args = None
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize

VOID, TITLE, ABSTRACT = 0, 1, 2


def is_article_beginning(line):
    return line.startswith("<doc")


def is_abstract_ending(line):
    return line.startswith("</doc") or (line.startswith("Section::") and not args.full)


if __name__ == '__main__':
    print(os.getcwd())
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', nargs='?', type=str, help='/path/to/source.xml', default='../data/cswiki.xml')
    parser.add_argument('target_file', nargs='?', type=str, help='/path/to/target.jsonl',
                        default='../data/wiki-pages/cswiki-001.jsonl')
    parser.add_argument('--language', type=str, default='czech')
    parser.add_argument("-f", "--full", action="store_true", help="Include the full article body.")
    parser.add_argument("-t", "--titles", action="store_true",
                        help="Append the article title to every sentence of the article.")
    parser.add_argument("-s", "--skip-tokenization", action="store_true",
                        help="Skip word tokenization and store untokenized sentences.")

    args = parser.parse_args()
    print(args.full, args.titles, args.skip_tokenization)
    Path(args.target_file).parent.mkdir(parents=True, exist_ok=True)

    reading, abstract, title = VOID, "", None
    with open(args.source_file, "r") as source_file, open(args.target_file, "w") as target_file:
        for line in source_file:
            if reading == VOID and is_article_beginning(line):
                reading = TITLE
            elif reading == TITLE:
                title = unicodedata.normalize('NFD', line).strip()
                reading = ABSTRACT
            elif reading and is_abstract_ending(line):
                reading = VOID
                try:
                    sentences = [sentence if args.skip_tokenization else (" ".join(word_tokenize(sentence, language=args.language))
                                     .replace('„', "``").replace('“', "''").replace(" ( )", ""))
                                 for sentence in sent_tokenize(abstract, "czech")]
                    if len(sentences) < 1 or len(title) < 1:
                        continue
                    if args.titles:
                        sentences = ["[ {} ]".format(title)] + sentences

                    print(json.dumps({
                        "id": title,
                        "text": " ".join(sentences),
                        "lines": "\n".join(f"{num}\t{sent}" for sent, num in zip(sentences, range(len(sentences))))
                    }, ensure_ascii=False), file=target_file)
                except:
                    print(abstract, file=sys.stderr)
                abstract = ""
            elif reading == ABSTRACT:
                abstract += unicodedata.normalize('NFD', line)
