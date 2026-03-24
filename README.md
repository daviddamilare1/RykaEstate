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


![image alt](https://github.com/daviddamilare1/RykaEstate/blob/d461de9d41971667b34cb099500b9e72aa8302fa/a6a4-102-89-75-177.ngrok-free.app_(Nest%20Hub%20Max).png)


![image alt](https://github.com/daviddamilare1/RykaEstate/blob/2bbe1796d53a60f9580e900cbf1470e1c03a6c98/127.0.0.1_8000_apartments(Nest%20Hub%20Max).png)


![image alt](https://github.com/daviddamilare1/RykaEstate/blob/ca49b2b98c7b6c84ee20bd2a86617251cdc43739/127.0.0.1_8000_apt_details_apt_5l2v3j5_aid_31odl_(Nest%20Hub%20Max)%20(2).png)


![image alt](https://github.com/daviddamilare1/RykaEstate/blob/9ca007a01918a2bb6c45c78d6fda48f1a04f54b0/screencapture-127-0-0-1-8000-agents-agents-2026-03-21-08_32_30.png)
