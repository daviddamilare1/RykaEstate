import random
from django.utils import timezone
from userauths.models import User
from agents.models import Agent
from core.models import Categories, House
from django.utils.text import slugify
import shortuuid
first_names = ['Chukwuma', 'Amaka', 'Chidi', 'Ngozi', 'Emeka', 'Ada', 'Tunde', 'Funmi', 'Ifeanyi', 'Zainab']
last_names = ['Adebayo', 'Okeke', 'Obi', 'Eze', 'Okafor', 'Nwachukwu', 'Adewale', 'Ogunleye', 'Chukwu', 'Ibrahim']
domains = ['gmail.com', 'yahoo.com', 'hotmail.com']
house_names = ['Sunset Villa', 'Lagos Retreat', 'Abuja Haven', 'Ikeja Mansion', 'Coastal Bungalow']
descriptions = ['Modern home with scenic views', 'Spacious family house', 'Luxury residence']
addresses = ['123 Ikeja Road', '45 Lagos Street', '78 Abuja Avenue']
if not Categories.objects.exists():
    for title in ['Residential']: Categories.objects.create(title=title, slug=slugify(title)+'-'+shortuuid.uuid()[:4].lower(), image='category.jpg'); print(f"Created category: {title}")
if Agent.objects.count() < 10:
    users = list(User.objects.filter(is_superuser=False)[:10 - Agent.objects.count()])
    for i in range(10 - Agent.objects.count() - len(users)):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        username = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}"
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}@{random.choice(domains)}"
        while User.objects.filter(email=email).exists():
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}@{random.choice(domains)}"
        try:
            user = User.objects.create_user(username=username, email=email, password='password123', first_name=first_name, last_name=last_name)
            users.append(user)
            print(f"Created user: {username}")
        except Exception as e:
            print(f"Error creating user {username}: {e}")
            continue
    for user in users:
        if not Agent.objects.filter(user=user).exists():
            full_name = f"{user.first_name} {user.last_name}"
            agent_id = f"aid_{''.join(random.choices('abcdefghijklmno12345', k=5))}"
            while Agent.objects.filter(agent_id=agent_id).exists():
                agent_id = f"aid_{''.join(random.choices('abcdefghijklmno12345', k=5))}"
            try:
                Agent.objects.create(user=user, full_name=full_name, email=user.email, phone=f"555{random.randint(1000000, 9999999)}", country='Nigeria', state='Lagos', city='Ikeja', identity_type='National Identification Number', agent_type='Realtor', agent_id=agent_id, years_of_exp=5, desc='Experienced agent', mission='Real estate services', min_price=100000, max_price=1000000, verified=False, is_available=True, date=timezone.now(), image='agent.jpg', cover_img='agent_cover.jpg', identity_image='id.jpg')
                print(f"Created agent: {full_name} ({agent_id})")
            except Exception as e:
                print(f"Error creating agent {full_name}: {e}")
                continue
if House.objects.count() >= 10:
    print("At least 10 houses already exist, skipping creation.")
else:
    agents = list(Agent.objects.all()[:10])
    categories = list(Categories.objects.all())
    for i in range(10 - House.objects.count()):
        agent = random.choice(agents)
        category = random.choice(categories)
        name = random.choice(house_names)
        slug = slugify(name)+'-'+shortuuid.uuid()[:4].lower()
        while House.objects.filter(slug=slug).exists():
            slug = slugify(name)+'-'+shortuuid.uuid()[:4].lower()
        try:
            house = House.objects.create(agent=agent, name=name, desc=random.choice(descriptions), address=random.choice(addresses), image='house_gallery/house.jpg', bedrooms=3, bathrooms=2, category=category, state='Lagos', city='Ikeja', price=1000000, sq_ft=2000, acres=2, featured=False, year_build=2020, date=timezone.now(), slug=slug, status='live', hid=f"hid_{shortuuid.ShortUUID(alphabet='abcdefghijklmnopqrstuvwxyz1234567890').random(length=7)}", is_sold=False)
            print(f"Created house: {name} ({house.hid})")
        except Exception as e:
            print(f"Error creating house {name}: {e}")
            continue
    print("Finished creating houses!")