======================================
`ezrest` Python REST wrapper framework
======================================

*Project Goal*

This goal of this project is to supply a framework that makes writing REST API wrappers much faster.

*Code Goal*

Ensuring extensibility is the most important part. There are a million different API's and they are ALL different.
In no way will it be possible to make a framework that can wrap all API's. This framework will target API's that
conform to the most BASIC of REST protocols while supplying addons that conform the most advanced.


The most basic features include CRUD.


The most advanced feature include different actions based on HTTP response codes.

CONTENTS
--------

example - Contains examples.

example.google - An example app for querying google, written intentionally complicated to demonstrate proper OOP techniques.


ezrest - The framework layer

ezrest.models - Base Model class and Metaclass details

ezrest.parameters - Parameter class and subclasses.

ezrest.exceptions - Exception objects used in the app. All exceptions thrown must extend EZRestError.


tests - Unit tests

