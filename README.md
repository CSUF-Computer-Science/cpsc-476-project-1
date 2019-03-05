# New Kids On The Blog

## CPSC-476 Blog Microservice

### Team Members

* Dayna Anderson
* Joshua Ferrara
* Hector Medina

### The Setup

Python 3 is packaged with a virtual environment. Should be good so that we all have the same dependencies.

On *nix environment:

`python3 -m venv venv`

On Windows:

`py -3 -m venv venv`

Then install dependencies with:

`pip3 install -r requirements.txt`

To update dendency file:

`pip3 freeze > requirements.txt`

To start the virtual environment:

`. venv/bin/activate`

### To Run
To run a server locally.

On *nix environment:

```
export FLASK_APP=services
flask run
```