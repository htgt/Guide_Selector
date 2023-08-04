# SGE guide selection

Guide selection tool.

[[_TOC_]]

## Installation
Dependencies:
Build-essential and Python (3.8), Python-venv (3.8)
Change python command to point to Python (3.8), ubuntu expects python3 to be a specific version for compatibility.

```sh
make
make install
make setup-venv
```
```make``` sets up the git hooks that run unittests and pycodestyle on /src and /tests on ```git push```.
```make install``` installs dependancies below.
```make setup-venv``` creates a venv at ./venv and installs requirements.txt(s)

Or **manually**:
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

Mutator command runs the PAM mutator workflow in one command. 
Mutator requires the Guide Loci + ID, a reference GTF file to run and output directory path. 
Custom configuration can be passed to the command for any tweaks necessary.
Example:
```
python3 src/cli.py mutator --gtf ./example.gtf --tsv guides.tsv --conf custom.conf --out_dir ./output/
```

### Run with Docker

Build image 
```
docker build -t sge-guide-selection .
```

Run container with command (example `--version` command)
```
docker run sge-guide-selection --version
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

