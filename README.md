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

Where the variables can be any variables the use wishes.

## Images
Images used were official movie posters and were used for educational purposes to demonstrate proper loading of resources.

Contributors:
- James Harding
- Athena Martin
