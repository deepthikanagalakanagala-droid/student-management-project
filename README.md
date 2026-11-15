<<<<<<< HEAD
# CampusFlow — Student Management System (Project #1)

Full-stack student management app based on Project #1 of the supplied **DevOps Project - Docker and Jenkins** PDF: React frontend, FastAPI backend, PostgreSQL database, three Docker Compose services, and AWS EC2 deployment.

## Features
- Add, view, search, edit, and delete students
- Validate name, email, course, and study year
- Prevent duplicate email addresses
- Dashboard with student/course totals
- Persistent PostgreSQL database using a Docker volume
- Single public web port; backend and database stay internal
- REST API with interactive documentation (`/docs` when accessed internally)

## Architecture
```
Browser → EC2 public IP:80 → React/Nginx container
                                  │ /api/*
                                  ▼
                            FastAPI container
                                  │
                                  ▼
                            PostgreSQL container
                            (persistent volume)
```

## Prerequisites
- Docker Engine + Docker Compose plugin (or Docker Desktop)
- For cloud deployment: AWS account, Ubuntu EC2 instance, SSH key, security group

## Run locally
1. Open a terminal in the project root.
2. Copy `.env.example` to `.env`.
3. Change `POSTGRES_PASSWORD` to a long random password containing letters/numbers (avoid URL-reserved characters unless URL-encoded).
4. Run:
   ```bash
   docker compose up --build -d
   docker compose ps
   ```
5. Open `http://localhost` (or `http://localhost:8080` if `WEB_PORT=8080`).
6. Stop with `docker compose down`. Database data remains in the named volume. **Do not run `docker compose down -v` unless you intend to delete the database.**

## Deploy on AWS EC2 (Ubuntu)
1. Launch an Ubuntu 24.04 EC2 instance (size according to available memory; 2 GiB or more is recommended for builds). Create/download an SSH key pair.
2. Configure EC2 security group inbound rules: TCP 22 **only from your IP**, TCP 80 from users who need the demo. Never expose TCP 5432 or 8000.
3. Connect:
   ```bash
   chmod 400 my-key.pem
   ssh -i my-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
   ```
4. Install Docker using Docker's official Ubuntu installation guide: https://docs.docker.com/engine/install/ubuntu/ . Install Docker Compose plugin as documented. Confirm `docker compose version` works.
5. Transfer the project folder to the EC2 instance using `scp`, or clone your GitHub repository (without committing `.env`).
6. In the project folder, create `.env` from `.env.example` and replace the placeholder password.
7. Run `sudo docker compose up --build -d` (or use Docker's configured non-root permissions).
8. Verify `sudo docker compose ps` and `sudo docker compose logs --tail=50 backend`.
9. Visit `http://YOUR_EC2_PUBLIC_IP` and create a student.
10. For a public-facing production deployment, add HTTPS with a domain and TLS reverse proxy; this project is an HTTP-only classroom/demo baseline and **has no user authentication**. Do not store real student personal information or expose the demo publicly without access controls.

## Test the API
```bash
# From EC2 or a local machine running the app:
curl http://localhost/api/health
curl -X POST http://localhost/api/students \
  -H 'Content-Type: application/json' \
  -d '{"name":"Alex Morgan","email":"alex@example.com","course":"Computer Science","year":2}'
curl http://localhost/api/students
curl http://localhost/api/stats
```
For updating and deleting, use `PUT /api/students/{id}` and `DELETE /api/students/{id}`.

## Persistence demo
1. Add a student through the UI.
2. Run `docker compose down` (without `-v`).
3. Run `docker compose up -d`.
4. Refresh the browser; the student should still be present.

## Troubleshooting
- `docker compose ps`: inspect service status.
- `docker compose logs backend`: backend errors.
- `docker compose logs db`: database errors.
- `docker compose logs frontend`: Nginx errors.
- If port 80 is in use, set `WEB_PORT=8080` in `.env` and restart Compose; allow that port in your firewall for remote access.
- If database credentials change after the volume is initialized, existing PostgreSQL users/passwords are not automatically updated. Use the original credentials or intentionally reset the development volume.

## Presentation checklist
1. Show dashboard and three services running (`docker compose ps`).
2. Add, search, edit, and delete a student.
3. Show PostgreSQL persistence after container recreation.
4. Explain service-name networking (`db`, `backend`) and public/private ports.
5. Open app using EC2 public IP.
6. Show GitHub source and Dockerfiles.

## Limitations
- No authentication or authorization (demo only).
- No TLS in the base project.
- Database tables are created at app startup; production systems should use migrations.
- Docker build/runtime has not been executed in the artifact-generation environment; run the commands above to validate on your machine.
=======
# student-management-project
A web-based Student Management System to add, view, update, search, and delete student details.
>>>>>>> 4147edf3a4611b13d6de9a34c3c6eea8aec20720
