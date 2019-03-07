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

Finally, the database must be initialized. From the top-level directory run the following command:

`foreman run init-db`

### To Run

Each microservice can be started individually by using the following commands:

`foreman run users`

`foreman run articles`

`foreman run tags`

`foreman run comments`

### To Test

From the top-level directory, and with a fresh database created with `foreman run init-db`, tests can be ran with the following command: `py.test`.