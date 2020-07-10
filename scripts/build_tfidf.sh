PYTHONPATH=../src python ../src/scripts/build_tfidf.py \
--ngram 2 \
--hash-size 16777216 \
--tokenizer simple \
${1:-../data/fever.db} ${2:-../data}