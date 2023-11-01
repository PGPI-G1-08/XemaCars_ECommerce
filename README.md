# Car Rental E-Commerce Website

This is a Django-based e-commerce website for a car rental company. It allows customers to browse and rent cars online, manage their bookings, and explore available car options.

## Getting Started

These instructions will help you set up the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10
- Django
- Virtual environment (optional but recommended)

### Installation

1. Clone this repository to your local machine.

```
git clone https://github.com/PGPI-G1-08/XemaCars_ECommerce.git
```

2. Create a virtual environment and activate it (optional but recommended).

```
python3 -m venv venv
source venv/bin/activate
```

3. Install the project dependencies.

```
pip install -r requirements.txt
```

4. Create a .env file in `XemaCars_ECommerce` and add the following environment variables.

```
DB_NAME=<database name>
DB_USER=<database user>
DB_PASSWORD=<database password>
DB_HOST=<database host>
```

5. Migrate models and run the server.

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

6. Open a web browser and visit `http://localhost:8000/` to access the website, and `http://localhost:8000/admin/` to access the admin panel.

### Project Structure

The project follows the standard Django project structure. Key directories include:

- `XemaCars_ECommerce/`: Root project directory.
- `apps/`: Contains individual Django apps for different aspects of the website (e.g., car listings, user management, orders).
- `static/`: Stores static files like CSS, JavaScript, and images.
- `media/`: Stores user-uploaded media files, such as car images.
- `templates/`: Contains HTML templates for the website's pages.

## Built With

- [Django](https://www.djangoproject.com/) - The web framework used

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Django community for their excellent documentation and resources.
