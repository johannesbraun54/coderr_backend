# coderr_backend
a django backend for a freelancer developer platform 

# Coderr Backend

A Django backend for a JavaScript-based freelancer platform. This repository provides the server-side application, handling authentication, project management, and other API endpoints to support a dynamic freelancer marketplace.

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## About

**Coderr Backend** is built using Django and is designed to serve as the backbone of a freelancer developer platform. It manages user authentication, project-related operations, and provides API endpoints that allow seamless integration with a JavaScript-based frontend. This project is structured to be modular, secure, and extendable.

---

## Features

- **User Authentication:** Secure registration, login, and profile management.
- **Project Management:** API endpoints for job postings, proposals, and communications.
- **Modular Architecture:** Organized into separate Django apps (e.g., `auth_app` and `coderr_app`).
- **Media Management:** Handles file uploads (e.g., profile images, project documents) stored in `/media/uploads`.
- **RESTful API Design:** Easy integration with modern JavaScript front-end frameworks.

---

## Technologies

- **Python 3** – The programming language used.
- **Django** – The high-level Python web framework powering the backend.
- **Django REST Framework (optional):** For building RESTful APIs if implemented.
- **SQLite/PostgreSQL:** The default development database, configurable for production.

Additional dependencies can be found in the [requirements.txt](requirements.txt) file.

---

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/johannesbraun54/coderr_backend.git
   cd coderr_backend

2. **Create a Virtual Environment**

    ```bash
    python3 -m venv env
    macOs: source env/bin/activate 
    windows : `env\Scripts\activate`

3. **Install Dependencies**
    Make sure you have pip installed, then run:
    ```bash
    pip install -r requirements.txt

4. **Apply Migrations**
    ```bash
    Kopieren
    Bearbeiten
    python manage.py migrate

5. **Create a Superuser (Optional)**
    ```bash
    Kopieren
    Bearbeiten
    python manage.py createsuperuser

6. **Run the Development Server**
    
    ```bash
    Kopieren
    Bearbeiten
    python manage.py runserver
    The backend should now be running at:
    http://127.0.0.1:8000/