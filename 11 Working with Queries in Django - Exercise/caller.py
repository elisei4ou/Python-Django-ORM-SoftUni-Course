import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout
from main_app.choices import LaptopOperationSystemChoices
from django.db.models import Case, When, Value


# Import your models
# Create and check models
# Run and print your queries

def show_highest_rated_art():
    highest_rated_ard = ArtworkGallery.objects.order_by('-rating', 'id').first()

    return f"{highest_rated_ard.art_name} is the highest-rated art with a {highest_rated_ard.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery):
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts():
    negative_rated_arts = ArtworkGallery.objects.filter(rating__lt=0)
    negative_rated_arts.delete()


def show_the_most_expensive_laptop():
    most_expensive_laptop = Laptop.objects.order_by('-price', '-id').first()

    return f"{most_expensive_laptop.brand} is the most expensive laptop available for {most_expensive_laptop.price}$!"


def bulk_create_laptops(args):
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=['Lenovo', 'Asus']).update(
        storage=512
    )


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=['Apple', 'Dell', 'Acer']).update(
        memory=16
    )


def update_operation_systems():
    Laptop.objects.filter(brand='Asus').update(
        operation_system=LaptopOperationSystemChoices.WINDOWS
    )

    Laptop.objects.filter(brand='Apple').update(
        operation_system=LaptopOperationSystemChoices.MAC_OS
    )

    Laptop.objects.filter(brand__in=['Dell', 'Acer']).update(
        operation_system=LaptopOperationSystemChoices.LINUX
    )

    Laptop.objects.filter(brand='Lenovo').update(
        operation_system=LaptopOperationSystemChoices.CHROME_OS
    )



def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()



def bulk_create_chess_players(args):
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players():
    ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won():
    ChessPlayer.objects.filter(title='GM').update(
        games_won=30
    )


def change_chess_games_lost():
    ChessPlayer.objects.filter(title='no title').update(
        games_won=25
    )


def change_chess_games_drawn():
    ChessPlayer.objects.update(
        games_drawn=10
    )


def grand_chess_title_GM():
    ChessPlayer.objects.filter(rating__gte=2400).update(
        title='GM'
    )


def grand_chess_title_IM():
    ChessPlayer.objects.filter(rating__in=range(2300, 2400)).update(
        title='IM'
    )


def grand_chess_title_FM():
    ChessPlayer.objects.filter(rating__in=range(2200, 2299)).update(
        title='FM'
    )


def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(rating__in=range(0, 2200)).update(
        title='regular player'
    )


def set_new_chefs():
    Meal.objects.filter(meal_type='Breakfast').update(
        chef='Gordon Ramsay'
    )

    Meal.objects.filter(meal_type='Lunch').update(
        chef="Julia Child"
    )

    Meal.objects.filter(meal_type='Dinner').update(
        chef="Jamie Oliver"
    )

    Meal.objects.filter(meal_type='Snack').update(
        chef="Thomas Keller"
    )


def set_new_preparation_times():
    Meal.objects.filter(meal_type='Breakfast').update(
        preparation_time='10 minutes'
    )

    Meal.objects.filter(meal_type='Lunch').update(
        preparation_time='12 minutes'
    )

    Meal.objects.filter(meal_type='Dinner').update(
        preparation_time='15 minutes'
    )

    Meal.objects.filter(meal_type='Snack').update(
        preparation_time='5 minutes'
    )


def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in=['Breakfast', 'Dinner']).update(
        calories=400
    )


def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).update(
        calories=700
    )


def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).delete()


def show_hard_dungeons():
    dungeons = Dungeon.objects.filter(difficulty='Hard').order_by('-location')

    return '\n'.join(f"{d.name} is guarded by {d.boss_name} who has {d.boss_health} health points!" for d in dungeons)


def bulk_create_dungeons(args):
    Dungeon.objects.bulk_create(args)


def update_dungeon_names():
    Dungeon.objects.update(
        name=Case(
            When(difficulty='Easy', then=Value("The Erased Thombs")),
            When(difficulty='Medium', then=Value("The Coral Labyrinth")),
            When(difficulty='Hard', then=Value("The Lost Haunt"))
        )
    )


def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty='Easy').update(
        boss_health=500
    )


def update_dungeon_recommended_levels():
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty='Easy', then=Value(25)),
            When(difficulty='Medium', then=Value(50)),
            When(difficulty='Hard', then=Value(75))
        )
    )


def update_dungeon_rewards():
    Dungeon.objects.filter(boss_health=500).update(
        reward="1000 Gold"
    )

    Dungeon.objects.filter(location__startswith='E').update(
        reward="New dungeon unlocked"
    )

    Dungeon.objects.filter(location__endswith='s').update(
        reward="Dragonheart Amulet"
    )


def set_new_locations():
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss'))
        )
    )


def show_workouts():
    workouts = Workout.objects.filter(workout_type__in=['Calisthenics', 'CrossFit'])

    return '\n'.join(f"{w.name} from {w.workout_type} type has {w.difficulty} difficulty!" for w in workouts)


def get_high_difficulty_cardio_workouts():
    return Workout.objects.filter(workout_type='Cardio', difficulty='High').order_by('instructor')


def set_new_instructors():
    Workout.objects.update(
        instructor=Case(
            When(workout_type='Cardio', then=Value("John Smith")),
            When(workout_type='Strength', then=Value("Michael Williams")),
            When(workout_type='Yoga', then=Value("Emily Johnson")),
            When(workout_type='CrossFit', then=Value("Sarah Davis")),
            When(workout_type='Calisthenics', then=Value("Chris Heria"))
        )
    )


def set_new_duration_times():
    Workout.objects.update(
        duration=Case(
            When(instructor='John Smith', then=Value('15 minutes')),
            When(instructor='Sarah Davis', then=Value('30 minutes')),
            When(instructor='Chris Heria', then=Value('45 minutes')),
            When(instructor='Michael Williams', then=Value('1 hour')),
            When(instructor='Emily Johnson', then=Value('1 hour and 30 minutes'))
        )
    )


def delete_workouts():
    Workout.objects.exclude(workout_type__in=['Strength', 'Calisthenics']).delete()


# def show_the_most_expensive_laptop() -> str:
#     most_expensive_laptop = Laptop.objects.order_by('-price', '-id').first()
#
#     return f"{most_expensive_laptop.brand} is the most expensive laptop available for {most_expensive_laptop.price}$!"
#
#
# def bulk_create_laptops(args) -> None:
#     Laptop.objects.bulk_create(args)
#
#
# def update_to_512_GB_storage() -> None:
#
#     """
#     UPDATE laptop
#     SET storage = 512
#     WHERE brand IN ('Asus, 'Lenovo');
#     """
#     Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)
#
#     # """
#     # UPDATE laptop
#     # SET storage = 512
#     # WHERE brand = 'Asus' OR brand = 'Lenovo';
#     # """
#     # Laptop.objects.filter(Q(brand='Asus') or Q(brand='Lenovo')).update(storage=512)
#
#
# def update_to_16_GB_memory() -> None:
#     Laptop.objects.filter(brand__in=["Dell", "Apple", "Acer"]).update(memory=16)
#
#
# def update_operation_systems() -> None:
#     """
#     UPDATE "main_app_laptop"
#     SET "operation_system" = CASE
#         WHEN ("main_app_laptop"."brand" = 'Asus') THEN 'Windows'
#         WHEN ("main_app_laptop"."brand" = 'Apple') THEN 'MacOS'
#         WHEN ("main_app_laptop"."brand" = 'Lenovo') THEN 'Chrome OS'
#         WHEN ("main_app_laptop"."brand" IN ('Dell', 'Acer')) THEN 'Linux'
#         ELSE NULL
#     END;
#     """
#
#     Laptop.objects.update(
#         operation_system=Case(
#             When(brand="Asus", then=Value(OperationSystemChoices.WINDOWS)),
#             When(brand="Apple", then=Value(OperationSystemChoices.MACOS)),
#             When(brand="Lenovo", then=Value(OperationSystemChoices.CHROME_OS)),
#             When(brand__in=["Dell", "Acer"], then=Value(OperationSystemChoices.LINUX)),
#         )
#     )
#
#     # Laptop.objects.filter(brand="Asus").update(operation_system=OperationSystemChoices.WINDOWS)
#     # Laptop.objects.filter(brand="Apple").update(operation_system=OperationSystemChoices.MACOS)
#     # Laptop.objects.filter(brand="Lenovo").update(operation_system=OperationSystemChoices.CHROME_OS)
#     # Laptop.objects.filter(brand__in=["Dell", "Acer"]).update(operation_system=OperationSystemChoices.LINUX)
#
#
# def delete_inexpensive_laptops() -> None:
#     Laptop.objects.filter(price__lt=1200).delete()







