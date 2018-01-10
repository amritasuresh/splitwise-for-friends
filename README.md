# accounting_for_friends
The software allows users to keep track of money spent between friends, e.g. during a holiday, and helps settle their accounts.

![image](https://user-images.githubusercontent.com/6525798/32541333-ad4da06a-c46f-11e7-8ac5-d63830fbf154.png)

In order to invoice their friends, Accounting for Friends users are organized into groups. Each group contains one or more users.

The members of a group can create a transaction between the members of the group. The user enters the total amount that one person paid, and the software automatically creates transactions between the other members of the group. For example, if one user paid €30 for 3 people to have lunch, the software will create transactions that require the other two users to pay €10 to the first user.

For ease of use, the transactions within a group are also labeled by a single event (e.g. "weekend road trip" or "EDM festival").

Transactions are created in euros, but users can also change the interface to display the transaction amounts in US dollars, Polish złoty, and Indian rupees.

The software also provides a resolution feature, in order to efficiently resolve outstanding transactions between users.

![image](https://user-images.githubusercontent.com/6525798/32540462-0fed4cf0-c46d-11e7-8a9e-d24bfbf0ad68.png)

## Installation

For detailed installation instructions, see the INSTALL.md file.

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
