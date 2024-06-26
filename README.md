# MarkBins
 
# Garbage Report Website

This project is a Django-based web application aimed at reducing the spread of garbage on roads. Users can report garbage by uploading a photo, specifying the location (latitude and longitude), and selecting a predefined tweet template. The application sends this data to a Twitter bot, which tweets the report and tags the municipal corporation for cleanup.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Upload a photo of the garbage.
- Input location details (latitude and longitude).
- Select from predefined tweet templates.
- Automatically send the report to a Twitter bot.
- Store reports in a database.

## Technologies

- Python
- Django
- Django Rest Framework
- Pillow
- Requests
- PostgreSQL (or SQLite for development)
- Twitter API

## Setup

### Prerequisites

- Python 3.x
- pip
- PostgreSQL (for production)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Mrmanticore/Markbins.git
    cd garbage-report-website
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the database:**

    Update `DATABASES` in `GarbageReport/settings.py` with your database credentials. For development, you can use SQLite:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    ```

    For production, use PostgreSQL:

    ```python
  use render database
    ```

5. **Run database migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Start the development server:**

    ```bash
    python manage.py runserver
    ```

8. **Configure the Twitter bot:**

    - Create a Twitter developer account and set up a new app to get API keys.
    - Add your API keys and bot configuration to the project settings.

9. **Set up environment variables:**

    Create a `.env` file in the project root and add the following:

    ```plaintext
    DEBUG=1
    SECRET_KEY=your_secret_key
    DATABASE_URL=postgres://username:password@host:port/dbname
    firbase(Firestore database cridential information)
   "type": "service_account",
  "project_id": "example",
  "private_key_id": "example",
    ```

### Deploying to Render
Manual deployment
Create a new PostgreSQL database on Render. Copy its internal database URL for now—you’ll need it later.

Create a new web service on Render, pointing it to your project’s GitHub/GitLab/Bitbucket repository (give Render permission to access it if you haven’t already).

Select Python for the runtime and set the following properties (replace mysite with your project’s name):

Property	Value
Build Command	./build.sh
Start Command	python -m gunicorn mysite.asgi:application -k uvicorn.workers.UvicornWorker

1. **Install Render CLI:**

    ```bash
    pip install render-cli
python -m gunicorn pro_marks.asgi:application -k uvicorn.workers.UvicornWorker
    ```


2. **Configure Render database URL:**

    ```bash
    export DATABASE_URL=postgres://username:password@host:port/dbname
    ```

3. **Deploy to Render:**

    Follow the [Render deployment guide](https://render.com/docs/deploy-django).

## Usage

1. **Navigate to the homepage.**
2. **Upload a photo of the garbage.**
3. **Enter the location details (latitude and longitude).**
4. **Select a predefined tweet template.**
5. **Submit the report.**

The data will be sent to the Twitter bot, which will tweet the report and tag the municipal corporation.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
