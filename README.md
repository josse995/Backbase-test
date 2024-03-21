# mycurrency

Test for Backbase that consist of building a web platform that allows users to calculate currency exchanges rates

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)

License: MIT

## Requirements

- Linux/Mac (This project was built using Ubuntu, therefore, other operating systems are not covered)
- Docker >= 25.0.4 ([official installation guide](https://docs.docker.com/get-docker/))
- docker-compose >= 1.29.2 ([official installation guide](https://docs.docker.com/compose/install/))

## How to set up

1. Open a terminal on the root folder of the project
2. Execute `docker-compose -f local.yml up` to start the app (for a complete view on the start, go to [local.yml](local.yml))
   1. To clean the container, execute `docker-compose -f local.yml down`

## Basic Commands

Because this project was built to be used only with docker, every command has to be done towards the container.
>Always execute the commands from the root of the project!!!

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page.

- To create a **superuser account**, use this command:

      $ docker-compose -f local.yml run --rm django python manage.py createsuperuser

**To verify the user, check your console for a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.**

### Running tests with django test

    $ docker-compose -f local.yml run --rm django python manage.py test

## Architecture

This project has two main Docker containers: a Python container to contain the django app
and a postgres docker container.

### Django app

This django app has the following parts (each of them has their own README.md):

- [currency](mycurrency/currency/README.md): core of the django app, where there are the main models and django admin views
- [currency_rates](mycurrency/currency_rates/README.md): service that allows to retrieve the rate value of a given currency to the rest of them between two given dates
- [currency_converter](mycurrency/currency_converter/README.md): service that allows to obtain the latest exchange value from given currency to another given currency.
- [rate_of_return](mycurrency/rate_of_return/README.md): service that allows to get the time-weighted rate of return by day from given source and exchanged currency of a given amount since a given start date. 
- [providers](mycurrency/providers/README.md): in order to get the exchange rates, it is needed to get it from external providers.
- users: all the managing of users was made thanks to the cookie-cutter, so we won't go further on it.

## API

To access the api:

1. Once the app is running and having a superuser created, go to [0.0.0.0:8000/api/docs](http://0.0.0.0:8000/api/docs)
2. Execute the endpoint `/auth-token` (selecting `application/json` as type of payload) with the email and password. Copy the token given
3. Click on any padlock symbol to authorize every request. **On the text box put the prefix `token` followed by the token that you previously copied**
4. Execute any endpoint following the instructions (is given) on each endpoint.

## Deployment

This test was made taking into consideration only local environment (not production) due to time limitations.
The production docker-compose file was generated through cookie-cutter, but was not modified/adapted to this project.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
