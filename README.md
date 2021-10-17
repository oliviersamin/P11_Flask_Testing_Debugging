# README to be filled properly before the end of the project.  

##### Clone the repo and the virtual environment then install the dependencies (pip install -r requirements.txt)

##### inside the root folder P11.....  use the following comand lines to run the tests:


the names of the bug are defined as follow:  
* The error linked to the login issue is named : **login_error**  
* The error linked to the points to be updated is named : **points_updated**

##### A. In a first command line window:
1. launch the flask app so the functional tests may run

##### B. In a second command line window:
1. launch the following command to run all the tests (except for the locus tests): pytest -m <name_of_the_bug> (example: pytest -m points_updated)
