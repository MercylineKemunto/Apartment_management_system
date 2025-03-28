# Apartment Management System

## Overview

This project is an **Apartment Management System** built using Django and Django REST Framework. The goal of this system is to facilitate the management of apartment rentals, including features for leases, payments, maintenance requests, and notifications.

## Project Structure

The main components of the project include:

- **Models**: Defined in `models.py`, these represent the core database schema for the application, including:
  - `Apartment`: Represents an apartment building.
  - `Unit`: Represents individual rental units within an apartment.
  - `Lease`: Connects tenants to units with specific rental terms.
  - `Payment`: Tracks rent payments associated with leases.
  - `Debt`: Manages overdue payments.
  - `MaintenanceRequest`: Logs maintenance issues submitted by tenants.
  - `Expense`: Tracks shared expenses incurred by the apartment.
  - `Notification`: Manages alerts and notifications for users.
# Property Management System

## Project Overview
A comprehensive Django-based Property Management System that allows management of apartments, units, leases, payments, maintenance requests, and more.

## Features
- Apartment Management
- Unit Tracking
- Lease Management
- Payment Processing
- Maintenance Request Handling
- Expense Tracking
- Notification System

## Setup Instructions

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### Installation Steps
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Apartments
- `GET /api/apartments/`: List apartments
- `POST /api/apartments/`: Create apartment
- `GET /api/apartments/{id}/`: Retrieve specific apartment

### Units
- `GET /api/units/`: List units
- `POST /api/units/`: Create unit
- `GET /api/units/{id}/`: Retrieve specific unit

### Leases
- `GET /api/leases/`: List leases
- `POST /api/leases/`: Create lease
- `GET /api/leases/{id}/`: Retrieve specific lease

### Other Endpoints
- Payments
- Debts
- Maintenance Requests
- Expenses
- Notifications

## Filtering and Search
Most endpoints support:
- Filtering by specific fields
- Searching within text fields
- Ordering results

## Authentication
- Token-based authentication
- User-specific permissions
- Admin interface for full management

## Development Notes
- Uses Django Rest Framework
- Comprehensive model relationships
- Flexible filtering and search capabilities

## Recommended Improvements
- Add more advanced permission classes
- Implement more complex filtering
- Add custom actions to viewsets
- Create more detailed reporting features
