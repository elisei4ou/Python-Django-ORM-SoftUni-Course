import os
import django


from main_app.choices import ClassNameChoices

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


# Create queries within functions

def create_pet(name: str, species: str):
    new_pet = Pet.objects.create(name=name, species=species)
    new_pet.save()

    return f"{name} is a very cute {species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    new_artifact = Artifact.objects.create(name=name, origin=origin, age=age, description=description, is_magical=is_magical)
    new_artifact.save()

    return f"The artifact {name} is {age} years old!"

def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()

def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    str_return = ''
    LocationModel = Location.objects.all().order_by('-id')

    for location in LocationModel:
        str_return += f"{location.name} has a population of {location.population}!\n"

    return str_return

def new_capital():
    LocationModel = Location.objects.first()
    LocationModel.is_capital = True
    LocationModel.save()


def get_capitals():
    all_capitals = Location.objects.filter(is_capital=True).values('name')
    return all_capitals


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    CarModel = Car.objects.all()

    for car in CarModel:
        percent_off = sum([int(n) for n in str(car.year)]) / 100
        discount = percent_off * float(car.price)
        car.price_with_discount = float(car.price) - discount
        car.save()

    # Car.objects.bulk_update(CarModel, 'price_with_discount')


def get_recent_cars():
    recent_cars = Car.objects.filter(year__gt=2020).values('model', 'price')
    return recent_cars


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    TaskModel = Task.objects.filter(is_finished=False)
    return_str = ''

    for task in TaskModel:
        return_str += f"Task - {task.title} needs to be done until {task.due_date}!\n"

    return return_str


def complete_odd_tasks():
    TaskModel = Task.objects.all()

    for task in TaskModel:
        if task.id % 2 == 1:
            task.is_finished = True

    Task.objects.bulk_update(TaskModel, ['is_finished'])


def encode_and_replace(text: str, task_title: str):
    TaskModelByTitle = Task.objects.filter(title=task_title)
    new_text = ''

    for symbol in text:
        new_symbol = chr(ord(symbol) - 3)
        new_text += new_symbol

    for task in TaskModelByTitle:
        task.description = new_text


    Task.objects.bulk_update(TaskModelByTitle, ['description'])


def get_deluxe_rooms():
    RoomModel = HotelRoom.objects.filter(room_type='Deluxe')
    deluxe_rooms = []

    for room in RoomModel:
        if room.id % 2 == 0:
            deluxe_rooms.append(f'Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!')

    return '\n'.join(deluxe_rooms)


def increase_room_capacity():
    RoomModel = HotelRoom.objects.order_by('id')
    previous_room = None

    for room in RoomModel:

        if not room.is_reserved:
            continue

        if previous_room:
            room.capacity += previous_room.capacity
        else:
            room.capacity += room.id

        previous_room = room
        room.save()


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()

def delete_last_room():
    last_room = HotelRoom.objects.last()

    if not last_room.is_reserved:
        last_room.delete()


def update_characters():
    CharacteModel = Character.objects.all()

    for character in CharacteModel:
        if character.class_name == ClassNameChoices.MAGE:
            character.level += 3
            character.intelligence -= 7
        elif character.class_name == ClassNameChoices.WARRIOR:
            character.hit_points = character.hit_points / 2
            character.dexterity += 4
        else:
            character.inventory = "The inventory is empty"

        character.save()


def fuse_characters(first_character: Character, second_character: Character):
    sets_of_items = {
        'Mage': "Bow of the Elven Lords, Amulet of Eternal Wisdom",
        'Scout': "Bow of the Elven Lords, Amulet of Eternal Wisdom",
        'Warrior': "Dragon Scale Armor, Excalibur",
        'Assassin': "Dragon Scale Armor, Excalibur"
    }

    new_character = Character(
        name=f"{first_character.name} {second_character.name}",
        class_name="Fusion",
        level=abs((first_character.level + second_character.level) // 2),
        strength=abs((first_character.strength + second_character.strength) * 1.2),
        dexterity=abs((first_character.dexterity + second_character.dexterity) * 1.4),
        intelligence=abs((first_character.intelligence + second_character.intelligence) * 1.5),
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=sets_of_items[first_character.class_name]
    )

    first_character.delete()
    second_character.delete()
    new_character.save()


def grand_dexterity():
    CharacterModel = Character.objects.all()

    for c in CharacterModel:
        c.dexterity = 30

    Character.objects.bulk_update(CharacterModel, ['dexterity'])


def grand_intelligence():
    CharacterModel = Character.objects.all()

    for c in CharacterModel:
        c.intelligence = 40

    Character.objects.bulk_update(CharacterModel, ['intelligence'])


def grand_strength():
    CharacterModel = Character.objects.all()

    for c in CharacterModel:
        c.strength = 50

    Character.objects.bulk_update(CharacterModel, ['strength'])


def delete_characters():
    CharacterModel = Character.objects.all()

    for c in CharacterModel:
        if c.inventory == "The inventory is empty":
            c.delete()
