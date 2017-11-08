# accounting_for_friends
The software allows users to keep track of money spent between friends, e.g. during a holiday, and helps settle their accounts.

![image](https://user-images.githubusercontent.com/6525798/32541333-ad4da06a-c46f-11e7-8ac5-d63830fbf154.png)
## Getting Started

![image](https://user-images.githubusercontent.com/6525798/32540462-0fed4cf0-c46d-11e7-8a9e-d24bfbf0ad68.png)

### Prerequisites

You need virtualenv set up on your machine.
To set it up, run the following command. You will need to have pip 1.3 or higher installed:

    pip3 install virtualenv

### Installing

Clone the repository to your local system and go into the folder _/accounting_for_friends_.
Then run the following commands:

    virtualenv venv
    . venv/bin/activate
    pip3 install -r requirements.txt
    
### Running it locally

To run the application:

        python3 manage.py runserver 8000
        
The application is deployed at http://accounting-for-friends.herokuapp.com/

### Running the command line interface

![image](https://user-images.githubusercontent.com/6525798/32540801-16fa8b24-c46e-11e7-98a7-e4a394b558d8.png)


        python3 manage.py shell
        exec(open('./cli.py').read())

## Documentation

        pydoc -b

## Running the tests

We are using the Django test library (**unittest** module) for testing.
For functional tests we use **Selenium**.

To run tests, simply write a command:

        python3 manage.py test


## Deployment

The application is being deployed using **Travis**.

## Authors

wiedzmac

dtidmarsh

amritasuresh

## Links

* Heroku: https://accounting-for-friends.herokuapp.com
* Trello: https://trello.com/b/OhDgwqto/accounting-for-friends
* Travis: https://travis-ci.com/
* WWW template: https://www.dropbox.com/s/yydsz16oowdjf0n/WB0CX3745.zip?dl=0
* Course website: http://www.lsv.fr/~baelde/gl/index.html
