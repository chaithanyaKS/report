# Report API

Welcome to the documentation for **Report API**. This guide will walk you through the steps to install and set up the app.

## Installation

This project uses python 3.10 version

Follow these steps to install and set up the Django:

1. Clone the repository:
   ```sh
   git clone https://github.com/chaithanyaKS/report
   ```
2. Change into the project directory:
    ```sh
    cd report
    ```
3. create a virtual environment and install the dependencies
    ```sh
    python -m venv .venv
    source .venv/Scripts/activate # for windows
    source .venv/bin/activate # for linux
    pip install -r requirements.txt
    ```

4. Run the migrations
    ```sh
    python manage.py migrate
    ```

5. Run Redis in docker using the command below
    ```sh
    docker run -p 6379:6379 -d redis/redis-stack-server:latest
    ```

6. Run the server 
    ```sh
    python manage.py runserver
    ```
7. Run the celery worker (Make sure redis is running before starting the server)
    ```sh
    python -m celery -A report worker --uid=celery -l INFO -S django -E --pool=eventlet --logfile=celery.log
    ```
