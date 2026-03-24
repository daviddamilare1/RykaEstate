# RykaEstate 🏠

**RykaEstate** is a full-stack real estate platform that allows users to browse, search, rent, and buy properties.  
Registered agents can list properties and go through a simple identity verification (KYC-like) process before publishing listings.

## 🚀 Features
- User authentication  
- Become an agent (required: full name, ID type, ID photo upload)  
- One agent profile can be shared by multiple users
- Users can book a meeting with an agent or book a house tour
- Users can also book an apartment 
- Agents own and list their properties
- Filter search, Agent rating and Apartment rating
- Customer dashboard and Agent dashboard
- Clean uploads: `media/agents/<user_id>/`  

## ✨ Technologies
- Backend: Django (Python)  
- Frontend: BootstrapMade template + custom HTML/CSS/JS  
- Database: PostgreSQL (recommended) / SQLite (development)  

## ⚡ Quick Start

- git clone https://github.com/daviddamilare1/RykaEstate.git
- cd RykaEstate
- - cd est_prj
- python -m venv venv
- venv\Scripts\activate
- pip install django pillow python-decouple
- pip freeze > requirements.txt
- create .env with SECRET_KEY, DEBUG=True, MEDIA_ROOT etc.
- python est_prj/manage.py createsuperuser
- python est_prj/manage.py migrate
- python est_prj/manage.py runserver


##📍 The Process
---
I wanted to build something real world useful while learning Django properly, especially authentication, file uploads, and ManyToMany relationships.
Started with a custom user model, harder than I expected.
Then built the agent registration form, making fields actually required both in models and forms took way more tries than it should have.
Biggest headache, figuring out how to name uploaded ID photos using the user’s ID when user is a ManyToManyField. Had to use first and save the instance twice, not elegant but it works now.

Learned a lot about request files, dynamic upload paths, form validation, migrations when changing null true to required fields, and why you should test file uploads early.

Not perfect yet, mobile form could look better, no agent approval flow, no fancy property search, but I am honestly happy I shipped something functional that solves a real need, agent verification.

Still a work in progress, but this taught me more than ten tutorial projects combined.


![image alt]()
