# SGE guide selection

Guide selection tool.

[[_TOC_]]

## Installation
Designed to run in Linux, it's possible to install manually, with Makefile and into a docker container (with Makefile).
Dependencies:
Build-essential and Python (3.8), Python-venv (3.8)
Change python command to point to Python (3.8), ubuntu expects python3 to be a specific version for compatibility.

**manually**:
Update the githook path to the repo folder and authorise.
```sh
git config core.hooksPath .githooks
chmod +x .githooks/*
```
Install python and dependencies.
```sh
sudo apt-get update \
&& sudo apt-get -y install build-essential python3.8-dev python3.8-venv \
&& sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2  \
&& sudo update-alternatives --config python
```

***Makefile**
```sh
make
``` 
sets up the git hooks that run unittests and pycodestyle on /src and /tests on ```git push```.
```sh
make install
``` 
installs dependancies below.
```sh
make setup-venv
``` 
creates a venv at ./venv and installs requirements.txt(s)

***Docker***
Dependencies: Docker desktop or Docker engine

```sh
make install
make run-docker-interactive
```
The docker image will be built according to the Dockerfile, the venv will be created and it will launch into interactive mode in the currently open terminal.

To delete containers:
```sh
make clean-docker-containers
```
To delete containers and images:
```sh
make clean-docker
```


### Githooks
There are two githooks, pre-push and prepare-commit-msg.
The first runs tests and checks linting before push.
The second prefixes the commit message with the ticket or first word (ended by "_"), e.g. TD-434: 
To skip pre-push:
```sh
git push --no-verify
```

### Python3
Check Python3 (base) and Python (updated) version

```sh
python3 --version
python --version
```


### Python Virtual Environment
Requirements:

- Ubuntu 18.X.X 
- Python3.8+
- Python-venv

Setting up Virtual Env:

```sh
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

deactivate
```


### Usage

Command Line

```sh
python3 src/cli.py --version
```

Available commands:
- --version
- mutator
- retrieve

Shared arguments (not required):

| Argument   | Description               |
|------------|---------------------------|
| --conf     | Path to config file       |
| --out_dir  | Path to output directory  |

Shared arguments should be specified before command

## Retrieve command
Retrieve command gets data from WGE and writes a tsv file that can serve as an input for mutator command. 
Command requires the Target region ID and Loci.

Uses shared input arguments: output directory and config file.

Configs used for retrieve command: ``species_id`` (set to ``Human`` by default) and ``assembly`` (set to ``GRCh38`` by default)

Possible arguments for retrieve:

| Argument      | Description                                               |
|---------------|-----------------------------------------------------------|
| --region      | String with region data, example: chr19:50398851-50399053 |
| --region_file | Path tsv file with regions                                |

Example:
```
python3 src/cli.py --out_dir my_output retrieve --region chr19:50398851-50399053
```

or

```
python3 src/cli.py --out_dir my_output retrieve --region_file examples/target_regions.tsv
```


## Mutator command
Mutator command runs the PAM mutator workflow in one command. 
Mutator requires the Guide Loci + ID, a reference GTF file to run and output directory path. 
Custom configuration can be passed to the command for any tweaks necessary.

| Argument | Description                |
|----------|----------------------------|
| --tsv    | Path to input tsv file     |
| --gtf    | Path to reference gtf file |

Example:
```
python3 src/cli.py --conf custom.conf --out_dir ./output/ mutator --gtf ./example.gtf --tsv guides.tsv 
```


## Guide selector command
Runs retrieve-mutator steps together, accepts region (or file with regions) and gtf reference as arguments


| Argument      | Description                                               |
|---------------|-----------------------------------------------------------|
| --region      | String with region data, example: chr19:50398851-50399053 |
| --region_file | Path tsv file with regions                                |
| --gtf         | Path to reference gtf file                                |



### Run with Docker

Build image 
```sh
docker build -t sge-guide-selection .
```

Run container with command (example `--version` command)
```sh
docker run sge-guide-selection --version
```

Or with Makefile:
```sh
make run-docker-interactive
```

### Run tests
With makefile (direct or in docker container):
```sh
make test
~~OR~~
make run-docker-test
```
Or manually:
```sh
source venv/bin/activate

python -m unittest -v
```

### Run code style linting
```sh
pycodestyle src tests
```

