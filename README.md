# New Kids On The Blog

## CPSC-476 Blog Microservice

### Team Members

* Dayna Anderson
* Joshua Ferrara
* Hector Medina
* Jon Mouchou

### The Setup

#### 1) Virtual Environment Setup

Python 3 is packaged with a virtual environment. Should be good so that we all have the same dependencies.

From the project directory, run the following commands:

##### a) On *nix environment:

Using [Tuffix](https://github.com/kevinwortman/tuffix)? You'll also need this: `sudo apt-get install python3-venv`

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

#### 5) Nginx needs to be installed for load balancing support:

`sudo apt install nginx nginx-extras`

#### 6) create a cache folder for Nginx to store auth cache files:

`sudo mkdir -p /var/cache/nginx`

#### 7) Delete default port 80 file

`sudo rm /etc/nginx/sites-enabled/default`

#### 8) Copy blog file from project to your Nginx sites-available directory. Create a symlink to the sites-enabled and restart Nginx service:

`sudo cp blog /etc/nginx/sites-available`<br />
`sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/blog`<br />
`sudo service nginx restart`

#### 9) Finally, the database must be initialized. From the top-level directory run the following command:

`foreman run init-db`

### To Run

All microservices can be started in a formation using the following command

`foreman start -m users=3,articles=3,tags=3,comments=3,rss=3`

### Networking
| Service  | Port  |
|----------|-------|
| Articles | :500n |
| Tags     | :510n |
| Comments | :520n |
| Users    | :530n |
| RSS	   | :540n |

*n indicates the individual instance of the microservice running in a formation. For three instances of the Users service, the instances should be running on ports 5300-5302.*

### API Documentation

API documentation is avaialble on our [Postman page](https://documenter.getpostman.com/view/262836/S11PpFTY)

### To Test

#### 1) Initialize the database with test data

`foreman run init-data`

#### 2) Run the tests

`py.test`

This will execute all tests in the `tests` directory in alphabetical order and has been tested to work with the default testing database.
