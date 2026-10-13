# Forma Ecommerce — Monolithic vs Microservices

A small, responsive ecommerce demo built to compare two architectural styles. Includes product browsing, cart interactions, demo checkout/order persistence, Dockerfiles, and a microservices Compose setup.

## Screenshots
See `screenshots/monolithic.png` and `screenshots/microservices.png`.

## 1. Monolithic application
- One Flask application serves the UI and REST API.
- Product catalogue and order handling live in one deployable unit.
- SQLite persists orders in `monolithic/shop.db` (created at runtime).

Run locally:
```bash
cd monolithic
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000. API: `GET /api/products`, `GET /api/orders`, `POST /api/orders`.

Docker:
```bash
docker build -t forma-monolith .
docker run --rm -p 5000:5000 forma-monolith
```

## 2. Microservices application
- Nginx gateway/frontend on port 8080.
- Product Service: FastAPI; `GET /api/products`.
- Order Service: FastAPI + its own SQLite volume; `GET/POST /api/orders`.
- User Service: FastAPI + its own SQLite volume; `GET/POST /api/users`.
- Docker Compose creates a private network and service-name DNS; each service can be built/deployed independently.

Run (Docker Desktop or Docker Engine required):
```bash
cd microservices
docker compose up --build
```
Open http://localhost:8080. Health checks via `http://localhost:8080/health/products`, `/health/orders`, `/health/users`.

## Example API calls
```bash
curl http://localhost:8080/api/products
curl -X POST http://localhost:8080/api/users -H "Content-Type: application/json" -d '{"name":"Demo Customer","email":"demo@example.com"}'
curl -X POST http://localhost:8080/api/orders -H "Content-Type: application/json" -d '{"customer":"Demo Customer","items":[{"id":1,"qty":1},{"id":3,"qty":2}]}'
```

## Architecture comparison
| Concern | Monolith | Microservices |
|---|---|---|
| Deployment | One application | Gateway + three independently deployable services |
| Data | One SQLite database for orders; products in app | Separate persistent SQLite volumes for users and orders; product catalogue owned by Product Service |
| Scaling | Scale the whole application | Scale the busy service independently |
| Complexity | Simple to develop/debug | More network/configuration/observability overhead |
| Failure boundaries | A process issue can affect all features | Service failures can be isolated, depending on gateway and client behavior |

## Notes
- This is an educational demo, not production commerce: no authentication, payment provider, inventory locking, or shipping integration.
- The frontend uses a small sample catalogue and emoji product art so it runs without image/API keys.
- Keep secrets out of source control. Add tests and proper migrations before production use.
