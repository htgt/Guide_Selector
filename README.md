# SGE guide selection

## Installation
Dependencies:
Build-essential and Python (3.8), Python-venv (3.8)
Change python command to point to Python (3.8), ubuntu expects python3 to be a specific version for compatibility.

```sh
sudo apt-get update \
&& sudo apt-get -y install build-essential python3.8-dev python3.8-venv \
&& sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2  \
&& sudo update-alternatives --config python
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
- window 

Window command returns window for mutation in the guide. 
Example:
```
python3 src/cli.py window --seq GCCATTGTCCGGGAGTCAGAAACT --strand + --window_length 15
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
```
source venv/bin/activate

python -m unittest
```

