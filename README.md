# RykaEstate 🏠

**RykaEstate** is a full-stack real estate platform built with Django that allows users to browse, rent, and book properties while enabling agents to verify their identity and manage listings.

## 🔥 Highlights
- KYC-like agent verification system (ID upload + validation flow)
- Multi-user agent profiles (ManyToMany relationship)
- Property booking system (meetings, tours, apartment reservations)
- Role-based dashboards (Agent & Customer)
- Dynamic file upload system with structured media storage

---

## 🚀 Features
- User authentication  
- Become an agent (ID verification required)  
- Property listing and ownership system  
- Booking system (house tours, meetings, apartments)  
- Filtered search  
- Agent & apartment rating system  
- Separate dashboards for agents and users
- In-app notification 

---

## 🔌 API Endpoints

- GET /api/featured_houses/
- GET /api/houses/
- GET /api/featured_apartments/
- GET /api/apartments/
- GET /api/categories/
- GET /api/category_detail/<id>/


---


## 🛠 Tech Stack
- **Backend:** Django (Python)  
- **Frontend:** Bootstrap + custom HTML/CSS/JS  
- **Database:** PostgreSQL / SQLite  

---

## ⚡ Setup Instructions

```bash
git clone https://github.com/daviddamilare1/RykaEstate.git
cd RykaEstate

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


## 📍 Development Journey

This project was built to deeply understand Django beyond tutorials.

Key challenges:

Implementing a custom user model
Handling ManyToMany relationships for agent profiles
Managing dynamic file uploads (ID verification system)
Debugging form validation and required fields
Handling migrations when changing model constraints

One major challenge was naming uploaded files based on user IDs when using ManyToMany relationships.
This required saving the instance twice to properly attach file paths.


![image alt](https://github.com/daviddamilare1/RykaEstate/blob/2806d4d09204c7b74de27a90719291991cd08a83/127.0.0.1_8000_(Nest%20Hub%20Max)%20(2).png)


![image alt](https://github.com/daviddamilare1/RykaEstate/blob/2bbe1796d53a60f9580e900cbf1470e1c03a6c98/127.0.0.1_8000_apartments(Nest%20Hub%20Max).png)


![image alt](https://github.com/daviddamilare1/RykaEstate/blob/ca49b2b98c7b6c84ee20bd2a86617251cdc43739/127.0.0.1_8000_apt_details_apt_5l2v3j5_aid_31odl_(Nest%20Hub%20Max)%20(2).png)


![image alt](https://github.com/daviddamilare1/RykaEstate/blob/9ca007a01918a2bb6c45c78d6fda48f1a04f54b0/screencapture-127-0-0-1-8000-agents-agents-2026-03-21-08_32_30.png)
