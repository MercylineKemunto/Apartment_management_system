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
