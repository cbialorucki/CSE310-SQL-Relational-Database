# CSE310 SQL Relational Database

# Overview

This is a local account management system written in Python. It creates a local SQL database in memory and users interact with it through a built-in command line interface (CLI) application. Users can see statistical information about the database, create an account, change attributes about their account, or delete their account.

This project was designed to help teach myself about how to use a SQL database. As a future software engineer, I will need to work with SQL databases to store information and build systems for other people. I will be in a better position to build solutions if I better understand how to use SQL.

[Software Demo Video](http://youtube.link.goes.here)

# Relational Database

This software uses the SQLite library built into Python, sqlite3. This database only uses one table to log uses into and out of the database. This table contains an ID which is the primary key, a name, a unique phone number, a unique email address, and a password. The password field is stored in plaintext, which is a massive security issue. Please do not use this database for a professional project. This is for testing and evaluation purposes only.

# Documentation

[Program Code Documentation](/Sphinx-docs/markdown/index.md)

# Development Environment

Tools Used
* Microsoft Visual Studio Code

Programming Languages and Libraries Used
* Python
* sqlite3

# Useful Websites

* [Python Central](https://www.pythoncentral.io/)
* [SQLite Tutorial](https://www.sqlitetutorial.net/)
* [Sphinx](https://www.sphinx-doc.org/en/master/index.html)

# Future Work

* Security requires improvement. This software should not be used in any commercial or professional environment.

* For a permanent installation, the SQL database needs to be stored to disk, not in memory only. Currently the program stores the database in memory, which is deleted when the program is closed.

* An internet-connected front end would make this system much more useful. With an internet-connected front end pointing to a permanent installation, users would be able to log in, log out, and log in on another computer instead of being limited to testing it locally.