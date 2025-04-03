# Apartment Management System

A comprehensive Django-based apartment management system that handles property management, tenant tracking, payments, and maintenance requests.

## Features

### Property Management
- **Apartments**: Track multiple apartment buildings
- **Units**: Manage individual units with occupancy status
- **Leases**: Handle lease agreements with start/end dates
- **Tenants**: Manage tenant information and assignments

### Financial Management
- **Payments**: Track and record rent payments
- **Debts**: Monitor outstanding balances
- **Expenses**: Record property-related expenses

### Maintenance System
- **Requests**: Submit and track maintenance requests
- **Status Updates**: Monitor request progress
- **Unit-Specific**: Link requests to specific units

### User Management
- **Roles**:
  - Admin: Full system access
  - Manager: Property management
  - Tenant: Access to personal dashboard

### Notifications
- System-wide notifications
- User-specific alerts
- Maintenance updates

## Project Structure

```
rental_management/
├── api/
│   ├── models.py      # Database models
│   ├── views.py       # View logic
│   ├── urls.py        # URL routing
│   ├── templates/     # HTML templates
│   └── static/        # Static files
├── rental_management/
│   ├── settings.py    # Project settings
│   ├── urls.py        # Main URL configuration
│   └── wsgi.py        # WSGI configuration
└── manage.py          # Django management script
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd apartment_management_system
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

## Usage

### Admin/Manager Access
1. Log in with admin credentials
2. Access the dashboard for:
   - Property management
   - Tenant tracking
   - Financial overview
   - Maintenance requests

### Tenant Access
1. Log in with tenant credentials
2. Access tenant dashboard for:
   - Lease information
   - Payment history
   - Maintenance requests
   - Notifications

## Created Tenants

The system includes the following tenant accounts:

| Username | Email | Password |
|----------|-------|----------|
| tenant1  | tenant1@example.com | tenant123 |

## Development

### Running the Server
```bash
python manage.py runserver
```

### Creating New Tenants
```bash
python manage.py create_tenant <username> <email> <password>
```

### Database Management
```bash
python manage.py makemigrations
python manage.py migrate
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django Framework
- Bootstrap for UI components
- Font Awesome for icons

## Project Overview
A comprehensive Django-based Property Management System that allows management of properties, units, leases, tenants, payments, maintenance requests, and more.

## Features
* Property & Building Management
* Unit Tracking and Inventory
* Tenant Information Management
* Lease Creation, Document Generation, and Management
* Payment Processing and Financial Tracking
* Maintenance Request Workflow
* Occupancy Tracking and Statistics
* Dashboard with Key Performance Indicators
* Email Communication System
* Reporting and Data Visualization

## Setup Instructions

### Prerequisites
* Python 3.9+
* pip (Python package manager)
* Django 4.2+

### Installation Steps
1. Clone the repository
2. Create a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Set up the database:

```
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:

```
python manage.py createsuperuser
```

6. Run the development server:

```
python manage.py runserver
```

## Models

### Core Models
* **Property**: Represents a real estate property with name, address, and owner
* **Unit**: Individual rental units with details like size, bedrooms, bathrooms, and rent
* **Tenant**: Stores tenant information and emergency contacts
* **Lease**: Manages rental agreements between tenants and property units
* **Payment**: Tracks all financial transactions
* **MaintenanceRequest**: Handles repair and maintenance workflow

## API Endpoints

### Properties
* `GET /api/properties/`: List properties
* `POST /api/properties/`: Create property
* `GET /api/properties/{id}/`: Retrieve specific property
* `PUT /api/properties/{id}/`: Update property
* `DELETE /api/properties/{id}/`: Delete property

### Units
* `GET /api/units/`: List units
* `POST /api/units/`: Create unit
* `GET /api/units/{id}/`: Retrieve specific unit
* `PUT /api/units/{id}/`: Update unit
* `DELETE /api/units/{id}/`: Delete unit

### Tenants
* `GET /api/tenants/`: List tenants
* `POST /api/tenants/`: Create tenant
* `GET /api/tenants/{id}/`: Retrieve specific tenant
* `PUT /api/tenants/{id}/`: Update tenant
* `DELETE /api/tenants/{id}/`: Delete tenant

### Leases
* `GET /api/leases/`: List leases
* `POST /api/leases/`: Create lease
* `GET /api/leases/{id}/`: Retrieve specific lease
* `PUT /api/leases/{id}/`: Update lease
* `DELETE /api/leases/{id}/`: Delete lease
* `GET /api/leases/{id}/document/`: Generate lease document

### Other Endpoints
* `GET/POST /api/payments/`: Manage payments
* `GET/POST /api/maintenance-requests/`: Handle maintenance requests
* `GET /api/dashboard/`: Get dashboard statistics

## Filtering and Search
Most endpoints support:
* Filtering by specific fields (e.g., `?status=active`)
* Searching within text fields (e.g., `?search=smith`)
* Ordering results (e.g., `?ordering=-created_at`)

## Authentication
* Token-based authentication
* User-specific permissions
* Admin interface for full management

## Development Notes
* Uses Django and Django Rest Framework
* Comprehensive model relationships
* PDF generation for lease documents
* Email notifications for tenant communication
* Dashboard with occupancy and financial metrics

## Testing
```
python manage.py test
```


