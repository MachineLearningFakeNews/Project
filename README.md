# Project
Repo for all Project Files

## Docker Environment

### Build Docker Image

```sh
docker build -t fakenews_ml .
```

> "." refers to the Dockerfile directory. The assumption is you're in the Project directory

### Interactive Bash

```sh
docker run -it -v <ABSOLUTE_PATH_TO_PROJECT>:/root/workspace fakenews_ml /bin/bash
cd ~/workspace

# For installing libraries, run the following commands: 
pip install <PACKAGE_NAME>
pip freeze > requirements.txt
# then exit bash and commit/push requirements.txt

# Run python scripts
python my_script.py
```

> Rebuild docker image after installing new libraries.

### Running Jupyter

```sh
docker run -it -p 8888:8888 -v <ABSOLUTE_PATH_TO_PROJECT>/jupyter_notebooks:/opt/notebooks fakenews_ml
```