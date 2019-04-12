# Standard libs:
import os
import sys
import django
import argparse
from datetime import datetime
from django.utils.timezone import make_aware

# Python stuff:
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoStates.settings")
django.setup()

# Our libs:
from expenses.models import PeriodicUpdate, Concept, DescriptionTranslation, ParsedLine


# Functions:
def main():
    # Get CLI options:
    opts = parse_args()
    
    with open(opts.input_filename) as f:
        for i in range(3):
            f.readline()  # skip 3 lines
        
        for line in f:
            line = line.strip()
            
            # Skip if already parsed:
            if ParsedLine.objects.filter(line=line):
                if opts.verbose:
                    print(f"Skipped -> {line}")
                continue
            
            # Extract info from line:
            description, timestamp, _, extra, amount, _ = line.split(";")
            description = f"{description} ({extra})"
            t = datetime.strptime(timestamp, "%d/%m/%Y")
            t = make_aware(t)  # add timezone for Django
            amount = float(amount.replace(",", ""))
            
            # Skip descriptions we can not identify:
            try:
                concept_name = DescriptionTranslation.objects.get(description=description).concept.name
            except DescriptionTranslation.DoesNotExist:
                print(f"Unknown description --> {description}")
                continue

            # Save update:
            update = PeriodicUpdate()
            update.when = t
            update.amount = amount
            update.concept = Concept.objects.get(name=concept_name)
            update.save()
            
            # Save line as parsed:
            save_line(line)
            
            # Log:
            print(f"Saved -> {update}")


def parse_args(args=sys.argv[1:]):
    """Parse CLI arguments and return a options object."""
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("input_filename",
                        help="Input file name.")
    
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Be verbose. Default: do not be.")
    
    return parser.parse_args()


def save_line(line):
    """Save line as parsed (to ignore in the future)."""
    
    pl = ParsedLine()
    pl.line = line
    pl.save()


# Main:
if __name__ == "__main__":
    main()
