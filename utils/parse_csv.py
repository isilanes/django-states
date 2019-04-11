# Standard libs:
import os
import sys
import django
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

# Python stuff:
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoStates.settings")
django.setup()

# Our libs:
from expenses.models import PeriodicUpdate, Concept, DescriptionTranslation


# Functions:
def main():
    input_fn = sys.argv[1]
    with open(input_fn) as f:
        for i in range(3):
            f.readline()  # skip 3 lines
        
        for line in f:
            line = line.strip()
            description, timestamp, _, _, amount, _ = line.split(";")

            # Skip descriptions we can not identify:
            try:
                concept_name = DescriptionTranslation.objects.get(description=description).concept_name
            except DescriptionTranslation.DoesNotExist:
                print(f"Unknown description --> {description}")
                continue
                
            t = datetime.strptime(timestamp, "%d/%m/%Y")
            t = make_aware(t)  # add timezone for Django
            amount = float(amount.replace(",", ""))
            
            # Skip duplicates:
            such_updates = PeriodicUpdate.objects \
                .filter(when__gte=t)\
                .filter(when__lte=t+timedelta(days=1))\
                .filter(amount__gte=amount-0.01)\
                .filter(amount__lte=amount+0.01)  # just in case with those sneaky floats

            if such_updates:
                print(f"Skipped -> {line}")
                continue
            
            update = PeriodicUpdate()
            update.when = t
            update.amount = amount
            update.concept = Concept.objects.get(name=concept_name)
            update.save()
            print(f"Saved -> {update}")


# Main:
if __name__ == "__main__":
    main()
