# Wallet

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/sarath1python/wallet.git
$ cd wallet
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ conda create -n env python=x.x
$ conda activate env
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `conda`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd walletService
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```

## Workflow
All the postman request for the corresponding step have been shared

1. Create the account using customer_xid and enpoint 'api/v1/init'
2. Initalize the account using the api endpoint 'api/v1/wallet'
3. Add deposits to wallet using 'api/v1/wallet/deposits'
4. Withdraw deposit using 'api/v1/wallet/withdrawals'
5. View wallet using get method on 'api/v1/wallet'
6. Deactivate wallet using patch method on 'api/v1/wallet'

## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(env)$ python manage.py test wallet
```
