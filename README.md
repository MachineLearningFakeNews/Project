# Fake News Detection Pipeline

Classifies articles into two categories: reliable (non bias political, credible) or unreliable. We scrapped articles from ([OpenSources](http://www.opensources.co/)).

## Links

- [Final Report](https://drive.google.com/open?id=1PEd8e-9McCLDi3pBlo6kLcMEnKwWqjKxLV-kzc58gAA)

- [Slides](https://drive.google.com/open?id=1_WGbkFeD_sVvtIYzw80kmq4aIhjU8JvdFEOQwzJaJe0)

- [Data](https://www.dropbox.com/s/rx2rv8po8raj58k/dataset_models.zip?dl=0)

## Docker Environment

### Build Docker Image

```sh
docker build -t fakenews_ml .
```

> "." refers to the Dockerfile directory. The assumption is you're in the Project directory

### Interactive Bash

```sh
docker run -it -v <ABSOLUTE_PATH_TO_PROJECT>:/root/workspace fakenews_ml /bin/bash

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
docker run -it -p 8888:8888 -v <ABSOLUTE_PATH_TO_PROJECT>:/root/workspace -v <ABSOLUTE_PATH_TO_PROJECT>/jupyter_notebooks:/root/workspace/jupyter_notebooks fakenews_ml
```

## Contributing

[Trello board](https://trello.com/b/AXAFuqlV/fake-news-and-machine-learning)
