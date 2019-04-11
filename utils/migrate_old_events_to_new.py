# Standard libs:
import os
import sys
import json
import django

# Python stuff:
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoStates.settings")
django.setup()


# Functions:
def old_to_periodic():
    print("OldUpdate -> PeriodicUpdate")

    from expenses.models import OldUpdate, PeriodicUpdate

    for old_update in OldUpdate.objects.all():
        new_update = PeriodicUpdate()
        new_update.concept = old_update.concept
        new_update.when = old_update.when
        new_update.amount = old_update.amount
        new_update.comment = old_update.comment
        new_update.save()


def oldoneoff_to_oneoff():
    print("OldOneOffUpdate -> OneOffUpdate")
    
    from expenses.models import OldOneOffUpdate, OneOffUpdate
    
    for old_update in OldOneOffUpdate.objects.all():
        print(old_update)
        new_update = OneOffUpdate()
        new_update.when = old_update.when
        new_update.amount = old_update.amount
        new_update.comment = old_update.comment
        new_update.save()



# Main:
if __name__ == "__main__":
    #old_to_periodic()
    #oldoneoff_to_oneoff()
    pass
