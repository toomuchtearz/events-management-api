# Event Management API

A professional, production-ready REST API for managing events and attendee registrations. Built with **Django**, **Django REST Framework**, and **PostgreSQL**, fully containerized with **Docker**.

## Features

* Structured under `/api/v1/` to support future scalability and backward compatibility.
* Replaced the default username with **Email-based authentication** and implemented a case-insensitive `UserManager` for better UX and security.
* Features a custom `wait_for_db` management command to ensure the application waits for PostgreSQL to be fully ready before running migrations, preventing container race conditions.
* Uses `select_related` and `annotate` to handle complex queries (like attendee counts) in a single database hit, preventing N+1 query issues.
* Support for keyword search, ordering, and location/date filtering via `django-filters`.
* Integrated email confirmation system using Django's core mail signals (currently configured for console output for easy testing).
* Fully interactive **Swagger/OpenAPI 3.0** documentation with custom schema refinements for a clean UI.

---

## Tech Stack

* **Framework:** Django 6.x / Django REST Framework
* **Database:** PostgreSQL 16
* **Documentation:** drf-spectacular (OpenAPI 3.0)
* **Containerization:** Docker & Docker Compose
* **Authentication:** SimpleJWT (Email-based)

---

## Quick Start

The project is fully containerized for a "one-click" setup experience.

1.  **Clone the repository:**
    ```bash
    git clone <https://github.com/toomuchtearz/events-management-api.git>
    cd events-management-api
    ```

2.  **Configure Environment:**
    Copy the sample environment file. The defaults are pre-configured to work with the Docker services out of the box:
    ```bash
    cp .env.sample .env
    ```

3.  **Run the project:**
    ```bash
    docker-compose up --build
    ```

The API will be available at `http://localhost:8001/`

---

## Documentation

Once the server is running, you can explore and test the API endpoints directly through the interactive UI:

* **Swagger UI:** http://localhost:8001/api/v1/schema/swagger-ui/
* **Redoc:** http://localhost:8001/api/v1/schema/redoc/
* **Schema (JSON):** http://localhost:8001/api/v1/schema/

---

## Tests

The project includes a comprehensive test suite covering user authentication, custom model managers, event registration logic, and permissions.

To run the tests inside the Docker container:
```bash
docker-compose exec app python manage.py test
```

### Coverage Includes:

* **Users App:** Custom manager logic (email normalization), registration API, and profile management.
* **Events App:** CRUD permissions, organizer-specific restrictions, and registration/unregistration logic.

---

## 🚦 How to Start Using the API

Follow these steps to authenticate and make your first request:

### 1. Create an Admin Account

```bash
docker-compose exec app python manage.py createsuperuser
```

### 2. Obtain JWT Tokens

Endpoint: `POST /api/v1/token/`

Payload:
```json
{
  "email": "your-email@example.com",
  "password": "your-password"
}
```

### 3. Authenticate in Swagger

Open: http://localhost:8001/api/v1/schema/swagger-ui/

1. Click the "Authorize" button
2. Enter: `<your_access_token>`
3. Click Authorize

### 4. Access Protected Endpoints

* Create an Event: `POST /api/v1/events/`
* My Events: `GET /api/v1/events/my/`
* User Profile: `GET /api/v1/users/me/`

---

## Scalability

* Implement **Celery & Redis** to move email notifications to background workers.
* Add **Redis** caching to the event list endpoint for high-traffic scalability.
