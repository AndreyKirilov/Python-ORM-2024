import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character
# Import your models here


def create_pet(name, species):
    pet = Pet.objects.create(name=name, species=species)
    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name, origin, age, description, is_magical):
    artifact = Artifact.objects.create(name=name, origin=origin, age=age,
                                       description=description, is_magical=is_magical)
    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    all_locations = Location.objects.all().order_by('-id')
    result = []

    for location in all_locations:
        result.append(f"{location.name} has a population of {location.population}!")

    return "\n".join(result)


def new_capital():
    capital_location = Location.objects.first()
    capital_location.is_capital = True
    capital_location.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        discount = sum(int(x) for x in str(car.year)) / 100
        final_discount = float(car.price) * discount
        car.price_with_discount = float(car.price) - final_discount
        car.save()


def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)
    result = []

    for ut in unfinished_tasks:
        result.append(f"Task - {ut.title} needs to be done until {ut.due_date}!")

    return "\n".join(result)


def complete_odd_tasks():
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 == 1:
            task.is_finished = True

    Task.objects.bulk_update(tasks, ['is_finished'])


def encode_and_replace(text, task_title):
    tasks_with_title = Task.objects.filter(title=task_title)
    decoded_text = ''.join(chr(ord(s) - 3) for s in text)

    for task in tasks_with_title:
        task.description = decoded_text

    Task.objects.bulk_update(tasks_with_title, ['description'])


def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    result = []

    for dr in deluxe_rooms:
        if dr.id % 2 == 0:
            result.append(f"Deluxe room with number {dr.room_number} costs {dr.price_per_night}$ per night!")

    return "\n".join(result)


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')
    previous_room_capacity = 0

    for r in rooms:
        if r.is_reserved is False:
            previous_room_capacity = r.capacity
            continue

        else:
            if r.id == 1:
                r.capacity += r.id
                previous_room_capacity = r.capacity

            else:
                r.capacity += previous_room_capacity
                previous_room_capacity = r.capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()
    if last_room.is_reserved is False:
        last_room.delete()


def update_characters():
    Character.objects.filter(class_name='Mage').update(level=F('level') + 3,
                                                       intelligence=F('intelligence') - 7)

    Character.objects.filter(class_name='Warrior').update(hit_points=F('hit_points') / 2,
                                                          dexterity=F('dexterity') + 4)

    Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(inventory='The inventory is empty')


def fuse_characters(first_character: Character, second_character: Character):
    fusion_name = f"{first_character.name} {second_character.name}"
    fusion_class_name = 'Fusion'
    fusion_level = (first_character.level + second_character.level) // 2
    fusion_strength = (first_character.strength + second_character.strength) * 1.2
    fusion_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    fusion_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    fusion_hit_points = (first_character.hit_points + second_character.hit_points)

    if first_character.class_name in ['Mage', 'Scout']:
        fusion_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"

    else:
        fusion_inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(name=fusion_name, class_name=fusion_class_name, level=fusion_level,
                             strength=fusion_strength, dexterity=fusion_dexterity,
                             intelligence=fusion_intelligence, hit_points=fusion_hit_points,
                             inventory=fusion_inventory)

    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    characters = Character.objects.filter(inventory='The inventory is empty').delete()
# Create queries within functions
