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
from expenses.models import PeriodicUpdate, Concept

# Globals:
PERIODICS = {
    "INTERMON": "Intermon",
}


# Functions:
def main():
    input_fn = sys.argv[1]
    with open(input_fn) as f:
        for i in range(3):
            f.readline()  # skip 3 lines
        
        for line in f:
            line = line.strip()
            description, timestamp, _, _, amount, _ = line.split(";")
            
            t = datetime.strptime(timestamp, "%d/%m/%Y")
            t = make_aware(t)  # add timezone for Django
            print(t)
            amount = float(amount.replace(",", ""))
            
            # Skip duplicates:
            such_updates = PeriodicUpdate.objects \
                .filter(when__gt=t)\
                .filter(when__lt=t+timedelta(days=1))

            u = such_updates[0]
            print(u.amount)
            exit()
            if such_updates:
                print(f"Skipped -> {line}")
                continue
            
            
            if description in PERIODICS:
                update = PeriodicUpdate()
                update.when = t
                update.amount = amount
                update.concept = Concept.objects.get(name=PERIODICS[description])
                #update.save()
                print(update)
            else:
                print(f"Unknown description --> {description}")


# Main:
if __name__ == "__main__":
    main()
