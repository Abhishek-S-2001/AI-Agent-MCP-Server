
# 🧠 MCP Server — Flask + PostgreSQL

A lightweight backend API built with Flask to support a Model Context Protocol (MCP)-based multi-agent system. This backend manages all interactions with the PostgreSQL database through REST APIs, ensuring agents do not directly touch the database.

---

## 🗃️ Database Schema

![alt text](/assets/image.png)

## 🔐 Environment Variables

Create a `.env` file in the root directory with:

```env
DB_USER=your_user
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
```

---

## 🚀 API Endpoints

### 🌐 Service Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/service-categories` | Get all service categories |
| GET    | `/api/service-categories/<uuid:category_id>` | Get a single service category |
| POST   | `/api/service-categories` | Create a new service category |
| PUT    | `/api/service-categories/<uuid:category_id>` | Update an existing category |
| DELETE | `/api/service-categories/<uuid:category_id>` | Delete a service category |

#### Example POST Body

```json
{
  "category_name": "Healthcare"
}
```

---

### 🌐 Offerings

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/offerings` | Get all offerings |
| GET    | `/api/offerings/<uuid:offering_id>` | Get a single offering |
| POST   | `/api/offerings` | Create a new offering |
| PUT    | `/api/offerings/<uuid:offering_id>` | Update an offering |
| DELETE | `/api/offerings/<uuid:offering_id>` | Delete an offering |

#### Example POST Body

```json
{
  "offering_name": "Therapy Session"
}
```

---

## 🛠️ Setup & Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   flask run
   ```

---

## 📦 Future Additions

- 🧩 MCP JSON-RPC interface
- 🧾 Booking endpoints
- 🔐 Token-based auth
- 🐳 Docker support

---

## 💡 About MCP

This server is designed to interface with [Model Context Protocol](https://modelcontextprotocol.io/introduction), serving as a backend API to support agent reasoning, queries, and updates without direct database interaction.
