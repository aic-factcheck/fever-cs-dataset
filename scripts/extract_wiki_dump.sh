#!/bin/bash
python ../src/scripts/WikiExtractor.py -cb 1M --sections --min_text_length 1 --output ../data/extracted ../data/${1:-cs}wiki-latest-pages-articles.xml.bz2
find ../data/extracted -name '*bz2' -exec bunzip2 --stdout {} \; > ../data/${1:-cs}wiki.xml
rm -rf ../data/extracted