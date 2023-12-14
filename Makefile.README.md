### Makefile
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