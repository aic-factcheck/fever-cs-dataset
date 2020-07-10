cd scripts || exit
/bin/bash download_wiki_dump.sh
/bin/bash extract_wiki_dump.sh
/bin/bash extracted_wiki_to_jsonl.sh
/bin/bash build_db.sh
/bin/bash build_tfidf.sh