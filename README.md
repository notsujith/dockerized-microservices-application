# Dockerized Document Management System

This project involves developing multiple Flask applications each functioning as a microservice in a comprehensive document management system. The system allows user management, document creation and editing, activity logging, and document search functionalities. Each microservice is containerized using Docker to ensure scalability and isolation.

## Project Structure

- **User Management Microservice**: Handles user creation and login, generating JWTs for authentication.
- **Document Management Microservice**: Manages document creation and editing.
- **Logging Microservice**: Logs all activities across the system.
- **Search Microservice**: Enables searching documents based on various criteria.

Each microservice communicates over a Docker network and has its own SQLite database to ensure modularity and independence of operations.

## Technologies Used

- **Flask**: For creating the microservice endpoints.
- **SQLite**: Used for the microservice databases.
- **Docker**: For containerization and isolation of services.
- **JWTs**: For secure authentication across microservices.

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/notsujith/dockerized-microservices-application.git
   ```
2. **Build the Docker images**:
   Each microservice has its own Dockerfile named accordingly (`Dockerfile.users`, `Dockerfile.docs`, etc.). Use the following commands to build the Docker images for each service:
   ```bash
   docker build -t user-management -f Dockerfile.users .
   docker build -t document-management -f Dockerfile.docs .
   docker build -t logging -f Dockerfile.logs .
   docker build -t search -f Dockerfile.search .
   ```
3. **Run the containers**:
   Assuming a Docker network named `your-netid`, run each service with:
   ```bash
   docker run --network your-network -p 9000:9000 user-management
   docker run --network your-network -p 9001:9001 document-management
   docker run --network your-network -p 9002:9002 search
   docker run --network your-network -p 9003:9003 logging
   ```

## API Endpoints

Each microservice exposes specific endpoints for interacting with the system. For example, the User Management Service provides:

- POST `/create_user`: Creates a new user.
- POST `/login`: Authenticates a user and returns a JWT.

Document, search, and logging services provide similar endpoints tailored to their functionalities. 

## Contributing

Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
