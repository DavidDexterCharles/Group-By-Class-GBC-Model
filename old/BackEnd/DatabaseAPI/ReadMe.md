# Database API

This is a REST API that the model uses to perform CRUD operations on the
database.

To run the api: `python3 api.py` or `python api.py`

Two common approaches usually used for performing CRUD on a database
includes:
1. Adhoc Approach of writting SQL Queries to perform all the CRUD operations on the database.
2. Using ORMS,Object-relational Mapper (ORM).
    * From Wikipedia: "Object-relational mapping (ORM) is a mechanism that makes it possible to address, access and manipulate objects without having to consider how those objects relate to their data sources."
    * An example ORM is SQL Alchemy. SQL Alchemy provides a means by which
   Pyhton classes can be associated with database tables. Instances of these python classes (objects) are also associated with rows in tables they corresponding to. 
   The ORM provides a system that transparently synchronizes all state changes between each object(instance of python class) and rows related to them.

Instead of using those Approaches an API to interact with the database was created and utilized instead. Providing the benifits of a REST architecture. The technology
used for the creation of this DatabaseAPI is "Flask-Restless". Flask-Restless is a Flask extension that uses models(instances of python classes)
which have been described using SQLAlchemy or FLask-SQLAlchemy(flask extension of SQLAlchemy), for the creation of ReSTful JSON APIs.