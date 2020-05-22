import json
import sys
from pathlib import Path
from random import shuffle

LABELS = ("SUPPORTS", "REFUTES", "NOT ENOUGH INFO")
DEV_SIZE = TEST_SIZE = {label: 3333 for label in LABELS}  # 3333 data points for each label, feel free to adjust
datasets, datapoints = sys.argv[1].split("+"), {label: [] for label in LABELS}
folder = sys.argv[2] if len(sys.argv) > 2 else "."
Path(folder).mkdir(parents=True, exist_ok=True)

for dataset in datasets:
    with open(dataset) as file:
        for line in file:
            datapoint = json.loads(line)
            datapoints[datapoint["label"]].append(datapoint)

results = {dataset: [] for dataset in ("dev", "test", "train")}

for label in LABELS:
    shuffle(datapoints[label])  # comment this out to achieve a deterministic partitioning algorithm
    results["dev"].extend(datapoints[label][0:DEV_SIZE[label]])
    results["test"].extend(datapoints[label][DEV_SIZE[label]:DEV_SIZE[label] + TEST_SIZE[label]])
    results["train"].extend(datapoints[label][DEV_SIZE[label] + TEST_SIZE[label]:])

for dataset in ("dev", "test", "train"):
    shuffle(results[dataset])
    with open(folder + "/" + dataset + ".jsonl", "w") as file:
        file.writelines(json.dumps(datapoint, ensure_ascii=False) + "\n" for datapoint in results[dataset])
    if dataset is not "train":
        with open(folder + "/" + dataset + "-blind.jsonl", "w") as file:
            file.writelines(json.dumps({k: datapoint[k] for k in ("id", "claim")}, ensure_ascii=False) + "\n" for datapoint in results[dataset])
