## Getting Started

Accounting For Friends is built using Python 3 and Django 1.11. It also uses the Centaurus template from Bootstrap for HTML and CSS on the front end: https://wrapbootstrap.com/theme/centaurus-WB0CX3745

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