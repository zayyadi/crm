# CRM System

A comprehensive Customer Relationship Management (CRM) system built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- User authentication and authorization with JWT tokens
- Customer management (CRUD operations)
- Contact management
- Lead tracking and management
- Sales opportunity tracking
- Email functionality for password reset
- Role-based access control
- **Invoicing and billing automation** - Create and manage invoices, process payments, and handle subscriptions
- **AI Chatbot integration** - Intelligent customer support chatbot with context-aware responses powered by Google's Gemini AI

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with OAuth2
- **Email**: SMTP integration with template support
- **Testing**: Pytest
- **Deployment**: Docker support

## Prerequisites

- Python 3.11+
- PostgreSQL database
- Redis (for session management)
- SMTP server credentials (for email functionality)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd crm/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Copy the `.env.example` file to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```
   
   Update the following variables in `.env`:
   - `DATABASE_URL`: Your PostgreSQL database connection string
   - `SECRET_KEY`: A secure secret key for JWT token generation
   - `SMTP_*`: Your email server credentials

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`.

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

```bash
pytest
```

## Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t crm-backend .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 crm-backend
   ```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # Application entry point
│   ├── core/                # Core configuration and database setup
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas for validation
│   ├── auth/                # Authentication logic
│   └── routers/             # API route handlers
├── tests/                   # Test files
├── alembic/                 # Database migrations
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── Dockerfile               # Docker configuration
```

## API Endpoints

### Authentication
- `POST /api/v1/register` - User registration
- `POST /api/v1/login` - User login
- `POST /api/v1/token` - Token refresh
- `GET /api/v1/logout/` - User logout

### Users
- `PATCH /api/v1/{id}` - Update user password
- `DELETE /api/v1/{id}` - Delete user
- `POST /api/v1/send_token` - Send password reset token
- `POST /api/v1/password_reset` - Reset password

### Customers
- `POST /api/v1/customers/` - Create customer
- `GET /api/v1/customers/` - List customers
- `GET /api/v1/customers/{customer_id}` - Get customer
- `PUT /api/v1/customers/{customer_id}` - Update customer
- `DELETE /api/v1/customers/{customer_id}` - Delete customer

### Contacts
- `POST /api/v1/contacts/` - Create contact
- `GET /api/v1/contacts/` - List contacts
- `GET /api/v1/contacts/{contact_id}` - Get contact
- `PUT /api/v1/contacts/{contact_id}` - Update contact
- `DELETE /api/v1/contacts/{contact_id}` - Delete contact

### Leads
- `POST /api/v1/leads/` - Create lead
- `GET /api/v1/leads/` - List leads
- `GET /api/v1/leads/{lead_id}` - Get lead
- `PUT /api/v1/leads/{lead_id}` - Update lead
- `DELETE /api/v1/leads/{lead_id}` - Delete lead

### Opportunities
- `POST /api/v1/opportunities/` - Create opportunity
- `GET /api/v1/opportunities/` - List opportunities
- `GET /api/v1/opportunities/{opportunity_id}` - Get opportunity
- `PUT /api/v1/opportunities/{opportunity_id}` - Update opportunity
- `DELETE /api/v1/opportunities/{opportunity_id}` - Delete opportunity

### Billing and Invoicing
- `POST /api/v1/billing/invoices/` - Create invoice
- `GET /api/v1/billing/invoices/` - List invoices
- `GET /api/v1/billing/invoices/{invoice_id}` - Get invoice
- `PUT /api/v1/billing/invoices/{invoice_id}` - Update invoice
- `DELETE /api/v1/billing/invoices/{invoice_id}` - Delete invoice
- `POST /api/v1/billing/payments/` - Create payment
- `GET /api/v1/billing/payments/` - List payments
- `POST /api/v1/billing/subscriptions/` - Create subscription
- `GET /api/v1/billing/subscriptions/` - List subscriptions
- `PUT /api/v1/billing/subscriptions/{subscription_id}/cancel` - Cancel subscription

### AI Chatbot
- `POST /api/v1/chatbot/sessions/` - Create chat session
- `GET /api/v1/chatbot/sessions/` - List chat sessions
- `GET /api/v1/chatbot/sessions/{session_id}` - Get chat session
- `POST /api/v1/chatbot/sessions/{session_id}/messages` - Send message to chatbot
- `DELETE /api/v1/chatbot/sessions/{session_id}` - Delete chat session

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
