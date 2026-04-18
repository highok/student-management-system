# About
A simple and intuitive system to manage your student records.

This project is built using the `tkinter` and `psycopg2` libraries. `tkinter` for the UI and `psycopg2` for handling the PostgreSQL database and
it's queries.

**NOTE!** This project is still in development.

## Setup

Removing some parts like `config` which contains `.env` having sensitive information. To define it create a `condfig/.env` file and then
define some variables like `DB_NAME`, `DB_USER`, `DB_PORT`, `PASSWORD`, `DB_HOST`.

Among these `DB_HOST` and `DB_PORT` is optional as it defaults to `localhost` and `5432` respectively. If you provided different values during installation, these variables may not be optional for you. So, better to keep them anyway.

## Running

```console
$ python ./main.py
```
