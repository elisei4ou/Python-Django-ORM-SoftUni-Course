import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from datetime import date
from main_app.models import Car, SpecialRental
from django.core.exceptions import ValidationError
# Create a Car instance
car = Car.objects.create(brand="Tesla", model="Model S", license_plate="ABC123", rental_price_per_day=100.00)

# Create SpecialRental instance
special_rental1 = SpecialRental(
    car=car,
    start_date=date(2023, 5, 1),
    end_date=date(2023, 5, 5)
)

# Save special_rental1
print(special_rental1.save())

# Create another SpecialRental instance
special_rental2 = SpecialRental(
    car=car,
    start_date=date(2023, 5, 10),
    end_date=date(2023, 5, 12)
)

# Save special_rental2
print(special_rental2.save())

# Calculate total cost for special_rental1
print(special_rental1.calculate_total_cost())

# Calculate rental period for special_rental1
print(special_rental1.rental_period())

# Example of extending a SpecialRental
try:
    special_rental1.extend_rental(5)
except ValidationError as e:
    print(e)
