# Database Setup

This project uses **SQLite** as the database and **SQLAlchemy** as the ORM.

---

## 1. Creating the Database

To create the database, run the Flask application once. SQLAlchemy will automatically create the necessary tables based on the models defined.


Make sure the `instance/` folder exists to store the SQLite file.

---

## 2. Database File

The database file is saved in:


✅ Ensure that this file is included in your GitHub repository if you want others to use your sample data.

---

## 3. Optional: Using Flask-Migrate

If you're using `Flask-Migrate` for migrations, follow these steps:

pip install Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

---

## 4. Updating the Database Schema

To update the schema (if you change models):

---

## Notes

- If you're not using `Flask-Migrate`, SQLAlchemy will create tables automatically, but it won’t update them if you change the model structure later.
