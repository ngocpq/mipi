# MIPI

This repository contains dataset, experimental results and implementation source code of MIPI, a method to identify incorrect patches in automated program repair based on the meaning of source code.

Table of Contents
=================
  * [Repository's organization](#organization)
  * [Requirements](#requirements)
  * [Quickstart](#quickstart)
  * [Running MIPI as a WebSocket service](#running-mipi-as-a-websocket-service)

## Organization
---
The repository is organized as follows:
* [Experiment](/benchmarks): dataset and experimental results
* [src](/src): implementation source code and scripts
    * [mipi-code2vec](/src/mipi-code2vec): implementation code of MIPI based on Code2Vec model.
    * [scripts](/src/scripts): scripts for extracting the modified code snippets of patches in the QuixBugs and Defects4J benchmark.

## Requirements  
---
* [Python3](https://www.python.org/downloads/) - version 3.6 or newer. To check the version:
> python3 --version
* [TensorFlow](https://www.tensorflow.org/install) - version 2.0.0 or newer
* [Gensim](https://radimrehurek.com/gensim/install.html)

## Quickstart
----------
### Step 0: Cloning this repository
Cloning this repository and move to the MIPI's implementation folder
```
git clone git@github.com:ngocpq/mipi.git
cd src/mipi-code2vec
```

### Step 1: Downloading a trained Code2Vec model (1.4 GB)
The pre-trained Code2Vec model can be downloaded [here](https://s3.amazonaws.com/code2vec/model/java14m_model.tar.gz).

You need to extract the downloaded model files into the folder <MIPI_CODE_DIR>/models. Where <MIPI_CODE_DIR> is the MIPI's implementation root dir (folder [src/mipi-code2vec](/src/mipi-code2vec).
After you unziped the model files, the structure of the <MIPI_CODE_DIR>/models will look like follows:
```
- <MIPI_CODE_DIR>/
  - ...
  - models/
    - java14_model/
      - model files ...
```

### Step 2: Running MIPI example test
You can run the sample program mipi_sample.py using the following command to test if the configuration is correct:

```
cd <MIPI_CODE_DIR>
python mipi_sample.py
```

The output will look like:
```
C:\workplace\mipi-code2vec\venv36\Scripts\python.exe C:/workplace/mipi-code2vec/mipi_sample.py
2021-08-26 14:48:54.644632: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2
WARNING:tensorflow:From C:\workplace\mipi-code2vec\venv36\lib\site-packages\tensorflow_core\python\ops\resource_variable_ops.py:1630: calling BaseResourceVariable.__init__ (from tensorflow.python.ops.resource_variable_ops) with constraint is deprecated and will be removed in a future version.
Instructions for updating:
If using Keras pass *_constraint arguments to layers.
Results: 
<mipi.base_codemeaning_predictor.PatchEvaluationResult object at 0x000001FACD2F9CC0>
Json resuls: 
{"PatchId": "kPAR_Lang41", "Predicted": "incorrect", "MinSimGain": -0.007740318775177002, "MaxPatDistance": 0.007740318775177002, "SnippetsResults": ["{\"SimGain\": -0.007740318775177002, \"PatDistance\": 0.007740318775177002, \"Predicted\": \"incorrect\"}"]}
Results: 
<mipi.base_codemeaning_predictor.PatchEvaluationResult object at 0x000001FACD34EE80>
Json resuls: 
{"PatchId": "kPAR_Lang41", "Predicted": "correct", "MinSimGain": 0.01696985960006714, "MaxPatDistance": 0.01862657070159912, "SnippetsResults": ["{\"SimGain\": 0.01696985960006714, \"PatDistance\": 0.01862657070159912, \"Predicted\": \"correct\"}"]}

Process finished with exit code 0
```

## Running MIPI as a WebSocket service
----------

Running the following command to start the MIPI Websocket server:

```
cd <MIPI_CODE_DIR>
python mipi_server_start.py
```

After started, the MIPI Websocket server will wailting for the requests at the address ws://localhost:8765

