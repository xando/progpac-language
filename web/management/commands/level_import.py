import os
import hashlib

from django.core.management.base import BaseCommand, CommandError
from web.models import Level


class Command(BaseCommand):
    help = 'Load levels from file'

    def level_import(self, location):
        source = open(location, 'r').read()
        source_lines = source.split()

        name = location.rstrip(".txt")
        hash = hashlib.sha1(source).hexdigest()
        contet = "\n".join(source_lines[:25])
        maxsize = source_lines[-1]
        points = source_lines[-3]

        print hash
        print Level.objects.get_or_create(
            hash=hash,
            name=name,
            content=contet,
            maxsize=maxsize,
            points=points,
        )


    def handle(self, *args, **options):
        for path in args:
            if os.path.isdir(path):
                for root, _ , files in os.walk(path):
                    for f in files:
                        self.level_import(os.path.join(root, f))

            else:
                self.level_import(path)
