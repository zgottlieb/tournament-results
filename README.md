Tournament Results
==================

Description
-----------

A simple database for storing the results of a (fake) tournament.
Created for practice using PostgreSQL with Python.

Usage
-----

This app uses VirtualBox and Vagrant to create an environment to
create a temporary version of the database and test the app's functions
and queries. You will need both to run this app. Here are links for
downloads:

VirtualBox: http://www.virtualbox.org/wiki/Downloads
Vagrant:  http://www.vagrantup.com/downloads.html

To run the app:

1) Clone this repo to your machine.
2) Nagivate into the vagrant folder in the new repo folder.
3) Run the command *vagrant up*
4) Run the command *vagrant ssh*
5) Navigate to /vagrant/tournament.
6) Run *python tournament_test.py* to run the database tests.
