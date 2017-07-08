import re
from logging import getLogger

import requests
from django.core.management.base import BaseCommand

from recordings.models import CodeWarsProblem


logger = getLogger(__name__)

# The beginning of a command line function to streamline back-filling old
# Course entries.


class Command(BaseCommand):
    def handle(self, *args, **options):
        for codewar_problem in CodeWarsProblem.objects.all():
            # TODO: check for more details
            if not codewar_problem.url:
                continue
            # add try / except
            response = requests.get(codewar_problem.url)
            if codewar_problem.kyu is None:
                match = re.search(r'<span>(\d+) kyu</span>', response.content)
                if match:
                    codewar_problem.kyu = int(match.group(1))

            if not codewar_problem.name:
                match = re.search(r'"challengeName":"(.*?)"', response.content)
                if match:
                    codewar_problem.name = match.group(1)

            print('Updating codewars {}'.format(codewar_problem.name))
            codewar_problem.save()
