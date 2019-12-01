import os
import sys
import django
import argparse
from datetime import datetime

from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand

from expenses.models import PeriodicUpdate, Concept, DescriptionTranslation, ParsedLine


class Command(BaseCommand):
    help = "Parses a CSV from bank."

    def add_arguments(self, parser):
        """Parse CLI arguments and return a options object."""

        parser.add_argument("input_filename",
                            help="Input file name.")

        parser.add_argument("--verbose",
                            action="store_true",
                            help="Be verbose. Default: do not be.")

        parser.add_argument("-y", "--dry-run",
                            action="store_true",
                            help="Dry run. Default: real run.")

        parser.add_argument("--go-on",
                            action="store_true",
                            help="Go on after a failed description identification. Default: stop at first failure.")

    def handle(self, *args, **kwargs):

        input_file_name = kwargs["input_filename"]
        verbose = kwargs["verbose"]
        go_on = kwargs["go_on"]
        dry_run = kwargs["dry_run"]

        with open(input_file_name) as f:
            for i in range(3):
                f.readline()  # skip 3 lines

            for line in f:
                line = line.strip()

                # Skip if already parsed:
                if line_already_parsed(line):
                    if verbose:
                        print(f"\033[33mSkipped\033[0m -> {line}")
                    continue

                # Extract info from line:
                digested = DigestedLine(line)

                # Skip descriptions we can not identify:
                if not digested.concept:
                    print(f"\033[31mCan't identify line:\033[0m {line.replace(';', ' | ')}")
                    if go_on:
                        continue
                    else:
                        print(f"Line was: {line}")
                        break

                # Save update:
                update = PeriodicUpdate()
                update.when = digested.timestamp
                update.amount = digested.amount
                update.concept = digested.concept

                if not dry_run:
                    update.save()

                # Fake save, if asked to:
                if dry_run:
                    print(f"\033[32mWould save:\033[0m {update}")
                    continue

                # Save parsed line:
                save_line(line)
                print(f"\033[32mSaved\033[0m -> {update}")


class DigestedLine:

    def __init__(self, line):
        self.line = line

        # Helpers:
        self._concept = None
        self._concept_col = None
        self._extra_data_col = None
        self._date_col = None
        self._amount_col = None

    def identify_concept(self):
        """Return Concept to description, or None if none found."""

        # Try DescriptionTranslation with exact same description field as our concept column:
        dt = DescriptionTranslation.objects.filter(description=self.concept_col).first()
        if dt is not None:
            return dt.concept

        # Else, try DescriptionTranslation with description containing combined {concept_col}+{extra_data_col}:
        dt = DescriptionTranslation.objects.filter(description__contains=self.combined_concept).first()
        if dt is not None:
            return dt.concept

        return None

    def _digest_line(self):
        self._concept_col, self._date_col, _, self._extra_data_col, self._amount_col, _ = self.line.split(";")

    @property
    def concept(self):
        """
        Concept object corresponding to this line.

        :return: Concept
        """
        if self._concept is None:
            self._concept = self.identify_concept()

        return self._concept

    @property
    def concept_col(self):
        """
        Value in "concept" column of line.

        :return: str
        """
        if self._concept_col is None:
            self._digest_line()

        return self._concept_col

    @property
    def combined_concept(self):
        """
        Combination of concept column + extra data column, to get something more unique.

        :return: str
        """
        if self._concept_col is None or self._extra_data_col is None:
            self._digest_line()

        return f"{self._concept_col} ({self._extra_data_col})"

    @property
    def timestamp(self):
        """
        Time stamp of line.

        :return: timezone-aware datetime
        """
        if self._date_col is None:
            self._digest_line()

        t = datetime.strptime(self._date_col, "%d/%m/%Y")

        return make_aware(t)  # add timezone for Django

    @property
    def amount(self):
        """
        Amount of euros appearing in line.

        :return: float
        """
        if self._amount_col is None:
            self._digest_line()

        return float(self._amount_col.replace(",", ""))


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

