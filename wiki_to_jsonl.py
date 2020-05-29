import json
import os
import re
import sys
from xml.etree import ElementTree

import nltk
from nltk.tokenize import word_tokenize
import xmltodict as xmltodict
from wikiextractor.WikiExtractor import Extractor
from sentence_splitter import SentenceSplitter

article, reading, extractor, splitter = "", False, Extractor(None, None, None, []), SentenceSplitter(language='cs')
COMMON_ABBREVIATIONS = {"např.": "například", "atd.": "atd", }


def is_article_beginning(line):
    return line == "  <page>\n"


def is_article_ending(line):
    return line.startswith("==") or line.startswith("&lt;!-") or "</text>" in line


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return ' '.join(cleantext.split())


def cleantext(text):
    result = text + "\n"
    while text != result:
        text = result
        result.replace("\n\n", "\n")
        result.replace("\t", " ")
        result.replace("  ", " ")
    return result


os.environ["CORENLP_HOME"] = "/home/bertik/stanford-corenlp-full-2016-10-31"

with open("/local/fever-common/data/cswiki-20200520-pages-articles.xml") as file, \
        open("output2.jsonl", "w") as out:
    st = nltk.CoreNLPParser()
    for line in file:
        if not reading and is_article_beginning(line):
            article, reading = line, True
        elif reading and is_article_ending(line):
            try:
                et = xmltodict.parse(article + "</text></revision></page>")
                sentences = splitter.split(cleanhtml(extractor.wiki2text(et["page"]["revision"]["text"]["#text"])))
                #sentences = [" ".join(st.tokenize(sentence)) for sentence in sentences]
                sentences = [" ".join(word_tokenize(sentence, language="czech")) for sentence in sentences]

                print(sentences)
                print(json.dumps({"id": et["page"]["title"], "text": " ".join(sentences), "sentences": sentences}, ensure_ascii=False),
                      file=out)
            except:
                print(article, file=sys.stderr)
            reading = False
        else:
            article += line
