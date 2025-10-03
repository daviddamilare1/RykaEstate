import random
from django.utils import timezone
from userauths.models import User
from agents.models import Agent

# Sample data for generating agents
first_names = ['Chukwuma', 'Amaka', 'Chidi', 'Ngozi', 'Emeka', 'Ada', 'Tunde', 'Funmi', 'Ifeanyi', 'Zainab']
last_names = ['Adebayo', 'Okeke', 'Obi', 'Eze', 'Okafor', 'Nwachukwu', 'Adewale', 'Ogunleye', 'Chukwu', 'Ibrahim']
domains = ['gmail.com', 'yahoo.com', 'hotmail.com']
countries = ['Nigeria', 'USA', 'UK']
states = ['Lagos', 'Abuja', 'Rivers']
cities = ['Lagos', 'Abuja', 'Port Harcourt']
identity_types = ['National Identification Number', "Driver's License", 'International Passport']
agent_types = ['Realtor', 'Property Manager', 'Property Owner', 'Leasing Agent']
office_names = ['Prime Realty', 'City Homes', 'Elite Properties', None]
missions = ['Providing top-notch real estate services', 'Helping clients find their dream homes', None]

# Check if we already have enough agents
if Agent.objects.count() >= 10:
    print("At least 10 agents already exist, skipping creation.")
else:
    # Get existing users to reuse
    existing_users = User.objects.filter(is_superuser=False)[:10 - Agent.objects.count()]
    users_to_create = 10 - Agent.objects.count() - len(existing_users)
    
    # Create new users if needed
    new_users = []
    for i in range(users_to_create):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        username = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}"
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}@{random.choice(domains)}"
        while User.objects.filter(email=email).exists():
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}@{random.choice(domains)}"
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123',  # Default password (change for production)
                first_name=first_name,
                last_name=last_name
            )
            new_users.append(user)
            print(f"Created user: {username}")
        except Exception as e:
            print(f"Error creating user {username}: {e}")
            continue

    # Combine existing and new users
    users = list(existing_users) + new_users

    # Create agents for each user
    for user in users:
        full_name = f"{user.first_name} {user.last_name}"
        email = user.email
        phone = f"555{random.randint(1000000, 9999999)}"
        agent_id = f"aid_{''.join(random.choices('abcdefghijklmno12345', k=5))}"

        # Ensure unique agent_id
        while Agent.objects.filter(agent_id=agent_id).exists():
            agent_id = f"aid_{''.join(random.choices('abcdefghijklmno12345', k=5))}"

        try:
            agent = Agent.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                phone=phone,
                country=random.choice(countries),
                state=random.choice(states),
                city=random.choice(cities),
                identity_type=random.choice(identity_types),
                agent_type=random.choice(agent_types),
                agent_id=agent_id,
                years_of_exp=random.randint(1, 15),
                desc=f"Experienced {random.choice(agent_types)} based in {random.choice(cities)}.",
                mission=random.choice(missions),
                office_name=random.choice(office_names),
                office_address=f"123 {random.choice(cities)} Street" if random.choice(office_names) else None,
                twitter='https://twitter.com/example' if random.random() > 0.5 else None,
                instagram='https://instagram.com/example' if random.random() > 0.5 else None,
                facebook='https://facebook.com/example' if random.random() > 0.5 else None,
                whatsapp='https://wa.me/1234567890' if random.random() > 0.5 else None,
                min_price=random.randint(100000, 500000),
                max_price=random.randint(500001, 1000000),
                verified=False,
                is_available=True,
                date=timezone.now(),
                image='agent.jpg',  # Default as per models.py
                cover_img='agent_cover.jpg',  # Default as per models.py
                identity_image='id.jpg'  # Default as per models.py
            )
            print(f"Created agent: {full_name} ({agent_id})")
        except Exception as e:
            print(f"Error creating agent {full_name}: {e}")
            continue

    print("Finished creating agents!")