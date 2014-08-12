import os
import hashlib

from django.core.management.base import BaseCommand

from web.models import Level


class Command(BaseCommand):
    help = 'Load levels from file'

    def level_import(self, level_file):
        source = open(level_file, 'r').read()

        level_hash = hashlib.sha1(source).hexdigest()
        level_name = level_file.split('/')[-1].rstrip('.txt')

        print Level.objects.update_or_create(
            hash=level_hash,
            name=level_name,
            file=level_file
        )

    def handle(self, *args, **options):
        for path in args:
            if os.path.isdir(path):
                for root, _ , files in os.walk(path):
                    for f in files:
                        self.level_import(os.path.join(root, f))

            else:
                self.level_import(path)
