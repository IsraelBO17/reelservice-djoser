from django.core import management
from django.core.management.base import BaseCommand
from django.core.management.commands import loaddata


class Command(BaseCommand):
    """
    Custom management command to load fixtures into the database.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--fixtures",
            dest="fixtures",
            nargs="+",
            required=True,
            help="Fixture filenames to load (comma-separated).",
        )

    def handle(self, *args, **options):
        fixtures = options["fixtures"]
        for fixture in fixtures:
            self.stdout.write(f"Loading fixture: {fixture}")
            # loaddata(fixture)
            management.call_command("loaddata", fixture)
        self.stdout.write(self.style.SUCCESS("Successfully loaded fixtures."))
