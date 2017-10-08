# accounting_for_friends
The software should allow to keep track of money spent between friends, e.g. during a holiday. It should help them to settle their accounts.
## Getting Started

Clone the repository to your local system.

### Prerequisites

You need virtualenv set up on your machine.
To set it up (You can do it as follows if you have pip 1.3 or higher installed in your system):

    pip install virtualenv

### Installing

Clone the repository and go into the folder _/accounting_for_friends_
Then:

    virtualenv venv
    pip install -r requirements.txt
    
### Running it locally

To run it:

        python3 manage.py runserver 8000
        
The link where the application is deployed is http://accounting-for-friends.herokuapp.com/

## Documentation

        pydoc -b

## Running the tests

We are using the Django test library (**unittest** module) for testing.

## Deployment

This is being deployed using **Travis**.

## Authors

wiedzmac

dtidmarsh

amritasuresh
