# Scripts to opbtain the Czech Fever dataset
## Building data from scratch
Basic usage:
```
git clone https://github.com/heruberuto/fever-cs-dataset
cd fever-cs-dataset
pip install -r requirements.txt
/bin/bash build.sh
```
builds a fresh version of **FEVERcs** dataset using the latest available **cswiki** dump and latest stable version of the building scripts

## Download pre-built dataset
Basic (Docker-friendly) usage:

```
git clone https://github.com/heruberuto/fever-cs-baseline
/bin/bash fever-cs-baseline/download_prebuilt.sh [TARGET DIRECTORY]
```

E. g.
```
git clone https://github.com/heruberuto/fever-cs-baseline
/bin/bash fever-cs-baseline/download_prebuilt.sh /local/fever-common/data
```
