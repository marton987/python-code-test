# Ostmodern Python Code Test

The goal of this exercise is to test that you know your way around Django and
REST APIs. Approach it the way you would an actual long-term project.

The idea is to build a platform on which your users can buy and sell Starships.
To make this process more transparent, it has been decided to source some
technical information about the Starships on sale from the [Starship
API](https://swapi.co/documentation#starships).

A Django project some initial data models have been created already. You may need
to do some additional data modelling to satify the requirements.

## Getting started

* This test works with either
  [Docker](https://docs.docker.com/compose/install/#install-compose) or
  [Vagrant](https://www.vagrantup.com/downloads.html)
* Get the code from `https://github.com/ostmodern/python-code-test`
* Do all your work in your own `develop` branch
* Once you have downloaded the code the following commands will get the site up
  and running

```shell
# For Docker
docker-compose up
# You can run `manage.py` commands using the `./manapy` wrapper

# For Vagrant
vagrant up
vagrant ssh
# Inside the box
./manage.py runserver 0.0.0.0:8008
```
* The default Django "It worked!" page should now be available at
  http://localhost:8008/

## Tasks

Your task is to build a JSON-based REST API for your frontend developers to
consume. You have built a list of user stories with your colleagues, but you get
to decide how to design the API. Remember that the frontend developers will need
some documentation of your API to understand how to use it.

We do not need you to implement users or authentication, to reduce the amount of
time this exercise will take to complete. You may use any external libraries you
require.

* We need to be able to import all existing
  [Starships](https://swapi.co/documentation#starships) to the provided Starship
  Model
* A potential buyer can browse all Starships
* A potential buyer can browse all the listings for a given `starship_class`
* A potential buyer can sort listings by price or time of listing
* To list a Starship as for sale, the user should supply the Starship name and
  list price
* A seller can deactivate and reactivate their listing

After you are done, create a release branch in your repo and send us the link.


## Results

To import all existing Starships, you need to run the specific command:

```
./manage.py import_starships --endpoint https://swapi.co/api/starships/
```

Where the `endpoint` is the URL of the Starships.

An extended documentation using Swagger is located at `http://localhost:8008/api-docs/`.

To run tests, you should run the next command (For Docker):

    ./manapy test
