#  Backend Dev Demo Project Notes

## Subjective
* Overall it was a pretty fun demo project to work on. 
* Flask, SQLAlchemy, and marshmallow seem to work together well.
* Definitely like the idea of docker containers and I would like to keep learning more about them. With this project I didn't have to do much with them other than use the commands supplied in the README
* Flake8 linting was nice. 

## Problems Encountered
* README specifies that I should see 6 running containers but there were only ever 4. This didn't seem to have any effect on running or developing the project though.
* Had to modify the connection factory to allow for creation of connections without endpoints committed to the DB yet. Problem may have been related to my implementation of the connection model though.
* Stopping creation of dupe connections. Although it was not a requirement I couldn't get a composite UniqueConstraint for the to_person_id/from_person_id combination in the connection model. Managing a lookup table in python would work but it seems like using the UniqueConstraint in the model should be the way to achieve this.

## Bonuses / Extras Completed
* Caching implemented using Flask-Caching extension (https://flask-caching.readthedocs.io/en/latest/)
* Implemented get mutual friends endpoint
