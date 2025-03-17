# Development Process

## Docker and Container Management

### Starting the Application

To start the entire application:
```bash
make run
```

This will start both the frontend and backend services.

### Checking Container Status

Always verify the container status and logs after making changes:

1. Check container status:
```bash
docker compose -f docker/docker-compose.yml ps
```

2. Check logs for all services:
```bash
docker compose -f docker/docker-compose.yml logs -f
```

3. Check logs for a specific service:
```bash
docker compose -f docker/docker-compose.yml logs -f frontend
docker compose -f docker/docker-compose.yml logs -f backend
```

### Important Notes

- Always check the docker-compose logs after making configuration changes
- Verify that all services are running as expected
- Look for any error messages or warnings
- Confirm that ports are correctly mapped and accessible
- Check that volumes are properly mounted

## Development Workflow

1. Make changes to code
2. Rebuild and restart containers: `make run`
3. Check logs for any errors: `docker compose -f docker/docker-compose.yml logs -f`
4. Test the changes in the browser
5. Run tests if needed: `make test`

## Accessing Services

- Frontend: http://localhost:8080
- Backend: http://localhost:8000
- Database: localhost:5433 