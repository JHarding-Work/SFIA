# Group SFIA

This is a project done to demonstrate progress and learning with the QA devops course.

The application is a flask web application with support for deployment using docker-compose
with nginx and a mysql database. Upon setup, the server performing the build will start a local
docker container with the application running and an outwards facing http port that can be 
connected to by any machine with sufficient privileges.

## Database Setup
In its current state no setup should be needed, the database will pre-populate on startup.

## Local Running
To run the app locally an environmental variable "SQLALCHEMY_DATABASE_URI" will need to be set on
your local machine. This can be set to any SQLAlchemy database string. To create a local
sqlite database set this to "sqlite:///db.sqlite".

To start the program up, from the app directory type "python app.py" in your terminal.

## Creating a build on Jenkins
This assumes you currently have a Jenkins build set up with a pipeline targeted at the repository.
A globally accessible secret file named "SECRETS_FILE" will need to be set up in the Jenkins credentials
in order for the build to be able to function. The file will need to be of the format:

SECRET_KEY=[Secret Key]   
MYSQL_ROOT_PASSWORD=[Password]

Where the variables can be any variables the user wishes.

## Running Tests
If trying to run tests of your locally, simply input the following command into the terminal:
- python3 -m pytest --cov --cov-report html
This will generate a html coverage report in the folder in the following relative path:
- htmlcov\index.html

By settting up a Jenkins pipeline using the pre-existing Jenkinsfile, a coverage report will also be produced as well as the application running.
A webhook can also be setup to allow for coverage reports to be created everytime a change is commited to the project.


## Images
Images were used for educational purposes to demonstrate proper loading of resources.

Toy story poster: https://en.wikipedia.org/wiki/Toy_Story_%28franchise%29#/media/File:Toy_Story_logo.svg
Oppenheimer and blue beetle images: https://www.showcasecinemas.co.uk/showtimes/showcase-cinema-de-lux-bluewater
Lord of the Rings image: https://imgix.ranker.com/list_img_v2/18851/2018851/original/101-things-you-didn-t-know-about-the-lord-of-the-rings-films-u1


Contributors:
- James Harding
- Athena Martin
