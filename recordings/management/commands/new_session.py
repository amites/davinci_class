from logging import getLogger
import math
import os

from boto.s3.connection import S3Connection
from django.conf import settings
from filechunkio import FileChunkIO
from slackclient import SlackClient

from recordings.models import ClassRecording, Course, CourseSession
from recordings.management.commands.sync_recordings_s3 import SyncS3Command


logger = getLogger(__name__)
AWS_S3_CHUNK_SIZE = 52428800  # Default to 50MB chunks


class Command(SyncS3Command):
    def __init__(self, *args, **kwargs):
        self.bucket = None
        self.conn = None
        self.debug = False
        self._new_recordings = []
        self.course = Course.objects.get(pk=settings.CURRENT_COURSE)

        last_session = CourseSession.objects.order_by('-date').filter(course__id=settings.CURRENT_COURSE).last()

        self.recording_path  = settings.RECORDING_PATH
        self.recording_hold_path = settings.RECORDING_HOLD_PATH
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            '--debug',
            action='store_true',
            dest='debug',
            default=False,
            help='Take a guess?'
        )

    def load_files(self):
        # return list of files with absolute paths
        # pull files form a holding dir defined in settings
        for file_name in os.listdir(self.recording_hold_path):
            if file_name.endswith(settings.RECORDING_FILE_EXTENSION):
                self._new_recordings.append(os.path.join(self.recording_hold_path, file_name))

        # add parser for course git repo to pickup new files to add to session resources

    def ask_user(self):
        for file_path in self._new_recordings:
            short_name = os.path.basename(file_path).rstrip(settings.RECORDING_FILE_EXTENSION).strip('.')
        # take a list from load_files and gather user feedback about the files
        pass

    def build_objects(self):
        # create and save the different model entries
        pass

    def handle_files(self):
        # upload to S3 if not found
        # move and rename to storage folder
        pass

    def announce(self):
        # post notification of new session references to slack
        pass

    def handle(self, *args, **options):
        if options['debug']:
            self.debug = True

        if not os.path.isdir(settings.RECORDING_HOLD_PATH):
            raise OSError('Directory {} does not exist or not defined.'.format(settings.RECORDING_HOLD_PATH))

        self.load_files()
        self.ask_user()
        self.build_objects()
        self.handle_files()
        self.announce()
