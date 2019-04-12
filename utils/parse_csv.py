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
            if line_already_parsed(line):
                if opts.verbose:
                    print(f"\033[33mSkipped\033[0m -> {line}")
                continue
            
            # Extract info from line:
            description, timestamp, _, extra, amount, _ = line.split(";")
            description = f"{description} ({extra})"
            t = datetime.strptime(timestamp, "%d/%m/%Y")
            t = make_aware(t)  # add timezone for Django
            amount = float(amount.replace(",", ""))
            
            # Skip descriptions we can not identify:
            concept_name = identify_concept(description)
            if not concept_name:
                print(f"\033[31mUnknown description:\033[0m {description}: {line}")
                if opts.go_on:
                    continue
                else:
                    break

            # Save update:
            update = PeriodicUpdate()
            update.when = t
            update.amount = amount
            update.concept = Concept.objects.get(name=concept_name)
            if not opts.dry_run:
                update.save()
            
            # Fake save, if asked to:
            if opts.dry_run:
                print(f"\033[32mWould save:\033[0m {update}")
                continue
                
            # Save parsed line:
            save_line(line)
            print(f"\033[32mSaved\033[0m -> {update}")


def parse_args(args=sys.argv[1:]):
    """Parse CLI arguments and return a options object."""
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("input_filename",
                        help="Input file name.")
    
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Be verbose. Default: do not be.")
    
    parser.add_argument("-y", "--dry-run",
                        action="store_true",
                        help="Dry run. Default: real run.")
    
    parser.add_argument("--go-on",
                        action="store_true",
                        help="Go on after a failed description identification. Default: stop at first failure.")
    
    return parser.parse_args(args)


def save_line(line):
    """Save line as parsed (to ignore in the future)."""
    
    pl = ParsedLine()
    pl.line = line
    pl.save()


def line_already_parsed(line):
    """Return True if line already parsed."""
    
    for _ in ParsedLine.objects.filter(line=line):
        return True
    
    return False


def identify_concept(description):
    """Return concept name corresponding to descritiption, or None if none found."""
    
    for dt in DescriptionTranslation.objects.all():
        if dt.description in description:
            return dt.concept.name
    
    try:
        return DescriptionTranslation.objects.get(description=description).concept.name
    except DescriptionTranslation.DoesNotExist:
        return None


# Main:
if __name__ == "__main__":
    main()
