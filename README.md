# Microservice-Based Backend Module

**Aim:** To design, build, and deploy two independent backend microservices using Python (Flask) that communicate a realistic customer-order domain, and test them via Postman.

---

## Services Built

**1. Customer Service (Port 5001)**
Manages customer data and exposes an API to fetch orders belonging to a specific customer.

**2. Order Service (Port 5002)**
Manages order data and exposes an API to update the status of an existing order.

All data is stored in-memory using Python dictionaries (no database).

---

## Steps Performed

1. Created two separate Flask applications — one for each microservice.
2. Defined in-memory data stores (customers and orders as dictionaries).
3. Implemented REST API endpoints in each service.
4. Ran both services locally using Gunicorn on separate ports.
5. Tested all endpoints using Postman (GET and PUT requests).
6. Deployed both services independently on Render (free tier).

---

## Endpoints Tested

| Service | Method | Endpoint | Action |
|---|---|---|---|
| Customer | GET | /customers | List all customers |
| Customer | GET | /customers/{id}/orders | Fetch orders for a customer |
| Order | GET | /orders/{id} | Get a single order |
| Order | PUT | /orders/{id}/status | Update order status |

---

## Learning Outcomes

- Understood the microservice architecture pattern and how services are kept independent.
- Learned to build REST APIs using Flask and structure them around a single responsibility.
- Practised using in-memory data structures as a lightweight alternative to a database.
- Gained hands-on experience testing APIs with Postman (setting methods, headers, and JSON body).
- Deployed multiple services on a cloud platform (Render) and understood free-tier constraints like instance spin-down and shared compute hours.