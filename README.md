# Project 11: Improve a Python Web App by testing and debugging  

### Aim of the project
1. Several issues have been identified and need to be corrected in the project.  
Tests need to be performed and passed to be sure the bugs have been corrected.

2. A new feature needs to be added to the project.  
Tests are needed to check its validity.
   
3. The program will need an update regarding one feature after the previous corrections.  
Tests will be updated also to reflect this evolution.

4. Check that at least 60% of the code has been covered by the tests  

### Configuration used to run the tests
My personal configuration for this project:
* OS: Linux Mint 20.2 Cinnamon
* Python version: 3.8.10
* Webdriver for Selenium: Chromium  
Version 94.0.4606.81 (Build officiel) for Linux Mint (64 bits)

However here are the general observations to run the tests
* The unitary and integration tests can be run from any configuration
* <span style="color:red">The functional tests must be run with Chromium on your computer
* The performance tests can be run from any configuration  
* The unitary and integration tests can be performed at once and appart from the functional tests
* The functional tests can be run on their own  
To be able to run the tests follow the
  steps described in the following sections of this file.

### Conventions used
* It has been decided to use PEP8 for this program  
* All the corrections, features and tests will be written folowing the PEP8
* As this program is a MVP and some code has already been written, the existing code will remain as it is until the QA has been validated
* When the program is validated, all the code will be updated to PEP8 standard

### Steps to perform to run the program
1. Clone the repo & install the virtual environment 
2. Install the dependencies: `pip install -r requirements.txt`
3. All tests appart from functional tests can be performed, the command to run them will be displayed in the next section of this file

### Selenium WebDriver for functional tests (the tests in this repo are configured with Chromium)
1. To run functional tests  do as follows:  
    a. go to [this webpage](https://openclassrooms.com/fr/courses/7155841-testez-votre-projet-python/7414241-testez-le-comportement-fonctionnel-d-un-programme#r-7431078)   
    b. download the WebDriver corresponding to Chromium for your computer  
    c. install it on your computer  
    d. go to the following folder:
        `P11_Flask_Testing_Debugging/tests/fonctionnels/`   
    e. replace the actual chromedriver file.<span style="color:red"> **!!WARNING!! use the exact same file name when replacing the chromdriver file**</span>        
    f. tests are ready to be performed using the commands presented in the next section
        
### Command lines to run the tests
#### A. All the unitary and integration tests at once
To run all the tests at once (except the functional tests) do as follows:
1. in a new terminal window go to the root directory
2. activate your virtual environment  
3. go to the root folder `P11_Flask_Testing_Debugging`
4. then type `pytest -m all_tests` to run the tests

#### B. All the functional tests at once
To run the functional tests you will need to do as follows:  
1. open a first terminal window go to the root directory  
    a. activate your virtual environment  
    c. go to the directory `P11_Flask_Testing_Debugging`  
    d. type `export FLASK_APP=server.py`  
    e. then `flask run`
2. open a second terminal window   
    a. activate your virtual environment  
    b. go to the directory `P11_Flask_Testing_Debugging`  
    c. type `pytest -m functional_tests` to run the tests

#### C. Unitary, integration and functional tests for only one bug or feature at the time 
To run only one bug or feature tests you will need to do as follows:  
1. open a first terminal window go to the root directory  
    a. activate your virtual environment  
    c. go to the directory `P11_Flask_Testing_Debugging`  
    d. type `export FLASK_APP=server.py`  
    e. then `flask run`
2. open a second terminal window   
    a. activate your virtual environment  
    b. go to the directory `P11_Flask_Testing_Debugging`  
    c. type `pytest -m <pytest_marker>` to run the tests

Here are the details regarding the bugs ad features of this program  

| BUGS - FEATURES | PYTEST MARKER | COMMAND LINE |  
| ---------------- | ----------- |  ----------- | 
| bug/login-error | login_error | pytest -m login_error |   
| bug/points-update | points_updated | pytest -m points_updated |
| bug/past-competition | past_competition | pytest -m past_competition |
| bug/no_more_than_club_points | no_more_than_club_points | pytest -m no_more_than_club_points |
| bug/max_12_places | max_12_places | pytest -m max_12_places |
| feature/points_by_place | points_by_place | pytest -m points_by_place |
| feature/list_of_clubs_and_points | new_feature | pytest -m new_feature |

####E. Performance tests
To run one performance test for each bug or feature at the time do as follows:   
1. open a first terminal window go to the root directory  
    a. activate your virtual environment  
    c. go to the directory `P11_Flask_Testing_Debugging`  
    d. type `export FLASK_APP=server.py`  
    e. then `flask run`
2. open a second terminal window   
    a. activate your virtual environment  
    b. go to the directory `P11_Flask_Testing_Debugging`  
    c. type `locust -f tests/performance/all_performance_tests.py`

Then follow the instructions using these parameters:  
* Number of users = 6  
* Spawn rate = 6  
* Host = http://127.0.0.1:5000

