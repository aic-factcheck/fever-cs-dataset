# Scripts to obtain the Czech Wiki & Fever dataset
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
### Embed the latest dataset within a Docker image
Using `wget` from `Dockerfile`, unpacking the contents into `/local/fever-common/data`:
```dockerfile
RUN wget "https://raw.githubusercontent.com/heruberuto/fever-cs-dataset/master/download_prebuilt.sh" -O download_prebuilt.sh && /bin/bash download_prebuilt.sh /local/fever-common/data
```

### Using locally
Basic usage:

```
git clone https://github.com/heruberuto/fever-cs-baseline
/bin/bash fever-cs-baseline/download_prebuilt.sh [TARGET DIRECTORY]
```

E. g.
```
git clone https://github.com/heruberuto/fever-cs-baseline
/bin/bash fever-cs-baseline/download_prebuilt.sh /local/fever-common/data
```
