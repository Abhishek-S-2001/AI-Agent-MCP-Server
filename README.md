# 🧠 MCP Server — Flask + PostgreSQL Multi-Agent API

A lightweight, agent-centric backend API built using **Flask** and **PostgreSQL** to support the **Model Context Protocol (MCP)**-based multi-agent systems. This backend handles all database interactions through **REST APIs** to ensure agents never directly manipulate the database.

It supports **service discovery**, **appointment booking**, **conversation tracking**, and **provider management** to facilitate seamless coordination between users and providers in a multi-agent ecosystem.

---

## 📂 Database Schema



> **Key Highlights:**
>
> - Supports provider-offering-location mappings.
> - Handles user, booking, and conversation tracking.
> - Enforces data integrity via foreign keys.

---

## 🔑 Environment Variables Setup

Create a `.env` file in the project root:

```env
DB_USER=your_postgres_user
DB_PASS=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
```

---

## 🚀 API Endpoints

### 🌐 Service Categories

| Method | Endpoint                                     | Description                   |
| ------ | -------------------------------------------- | ----------------------------- |
| GET    | `/api/service-categories`                    | Get all service categories    |
| GET    | `/api/service-categories/<uuid:category_id>` | Get a single service category |
| POST   | `/api/service-categories`                    | Create a new service category |
| PUT    | `/api/service-categories/<uuid:category_id>` | Update an existing category   |
| DELETE | `/api/service-categories/<uuid:category_id>` | Delete a service category     |

#### Example POST Body

```json
{
  "category_name": "Healthcare"
}
```

---

### 🌐 Offerings

| Method | Endpoint                            | Description           |
| ------ | ----------------------------------- | --------------------- |
| GET    | `/api/offerings`                    | Get all offerings     |
| GET    | `/api/offerings/<uuid:offering_id>` | Get a single offering |
| POST   | `/api/offerings`                    | Create a new offering |
| PUT    | `/api/offerings/<uuid:offering_id>` | Update an offering    |
| DELETE | `/api/offerings/<uuid:offering_id>` | Delete an offering    |

#### Example POST Body

```json
{
  "offering_name": "Therapy Session",
  "price": 100,
  "availability_hours": "09:00-17:00"
}
```

---

### 🌐 Services (Search)

| Method | Endpoint                  | Description                                                |
| ------ | ------------------------- | ---------------------------------------------------------- |
| GET    | `/api/db/services`        | Search services by type and/or location (returns distance) |
| GET    | `/api/db/services/nearby` | Find services within 5 km of provided lat/lon              |
| GET    | `/api/db/services/all`    | Get all available services                                 |

#### Example GET Query

```http
GET /api/db/services?type=yoga&location=marina
```

#### Response Structure

```json
{
  "intent": "search_service",
  "services": [
    {
      "provider_name": "Health First",
      "provider_email": "abc@gmail.com",
      "provider_offering_id": "uuid",
      "service_name": "Yoga Class",
      "price": 75.0,
      "availability_hours": "09:00-17:00",
      "distance_km": 4.5,
      "location": {
        "name": "Downtown Clinic",
        "city": "Mumbai",
        "latitude": 19.0760,
        "longitude": 72.8777
      }
    }
  ]
}
```

---

### 👝 Booking API

| Method | Endpoint          | Description                                                |
| ------ | ----------------- | ---------------------------------------------------------- |
| POST   | `/api/db/ai/book` | Book a service by providing email and provider offering ID |

#### Example POST Body

```json
{
  "email": "james.s@example.com",
  "provider_offering_id": "uuid",
  "appointment_date": "2024-12-25",
  "appointment_start_time": "10:00",
  "appointment_end_time": "11:00",
  "notes": "Patient: James Scott\nPhone: 1234567891\nxyz"
}
```

---

### 💬 Provider AI Agent Endpoints

| Method | Endpoint                                          | Description                                    |
| ------ | ------------------------------------------------- | ---------------------------------------------- |
| GET    | `/api/db/ai/provider/<provider_id>/bookings`      | Provider can view booking requests             |
| POST   | `/api/db/ai/provider/respond`                     | Provider can respond to booking requests       |
| GET    | `/api/db/ai/provider/<provider_id>/conversations` | Provider can view all conversations with users |

---

## 💡 Key Features

- ✨ Multi-agent backend design
- 👥 Supports user and provider role management
- ⌛ Appointment booking and status management
- 💬 Full conversation logging between users and providers
- 🌐 Service discovery with distance calculations

---

## 🛠️ Setup & Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the Flask server:

```bash
flask run --host=0.0.0.0 --port=10000
```

---

## 📦 Future Enhancements

- 🧠 JSON-RPC interface for AI agent orchestration
- 🔐 Authentication and token-based access control
- 🛣️ Docker containerization
- 💻 Provider dashboard integration

---

## 🔗 About MCP

This server is purpose-built for **Model Context Protocol (MCP)** to enable structured, agent-driven reasoning, decision-making, and service fulfillment in multi-agent environments.

Learn more at: [Model Context Protocol](https://modelcontextprotocol.io/introduction)

