# New Kids On The Blog

## CPSC-476 Blog Microservice

### Team Members

* Dayna Anderson
* Joshua Ferrara
* Hector Medina

### The Setup

#### 1) Virtual Environment Setup

Python 3 is packaged with a virtual environment. Should be good so that we all have the same dependencies.

From the project directory, run the following commands:

##### a) On *nix environment:

Using [Tuffix](https://github.com/kevinwortman/tuffix)? You'll also need this: `apt-get install python3-venv`

`python3 -m venv venv`

##### b) On Windows:

`py -3 -m venv venv`

#### 2) Start the virtual environment:

`. venv/bin/activate`

#### 3) Then install dependencies with:

`pip3 install -r requirements.txt`

##### As a developer, to update dendency file:

`pip3 freeze > requirements.txt`

#### 4) Additionally, you'll have to install foreman:

`sudo apt install ruby-foreman`

#### 5) Finally, the database must be initialized. From the top-level directory run the following command:

`foreman run init-db`

### To Run

Each microservice can be started individually by using the following commands:

`foreman run users`

`foreman run articles`

`foreman run tags`

`foreman run comments`

### To Test

#### 1) Initialize the database with test data

`foreman run init-db`

#### 2) Run the tests

`py.test`

This will execute all tests in the `tests` directory in alphabetical order and has been tested to work with the default testing database.
