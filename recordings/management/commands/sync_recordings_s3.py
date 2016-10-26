from logging import getLogger
import math
import os

from boto.s3.connection import S3Connection
from django.conf import settings
from django.core.management.base import BaseCommand
from filechunkio import FileChunkIO
from slackclient import SlackClient

from recordings.models import ClassRecording


logger = getLogger(__name__)
AWS_S3_CHUNK_SIZE = 52428800  # Default to 50MB chunks
RECORDING_FILE_EXTENSION = 'm4a'


class Command(BaseCommand):
    """
    Class to scan a local directory for recording files and compare it
    to a remote S3 bucket. It will then upload any new recordings to S3
    and store them within a database for display. Optionally post a
    message to slack indicating that the uploads have been made available.
    """

    help = 'Synchronizes class recordings folder with S3, adds to DB ' \
           'for display and optionally announces new recordings to slack.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--slack',
            action='store_true',
            dest='slack',
            default=False,
            help='Announce new recordings to slack.',
        )

        parser.add_argument(
            '--debug',
            action='store_true',
            dest='debug',
            default=False,
            help='Take a guess?'
        )

    def __init__(self, *args, **kwargs):
        self.bucket = None
        self.conn = None
        self.debug = False
        self.new_recordings = []
        self.s3_file_objs = []
        self.s3_files = []
        self.file_extension = kwargs.get('file_extension',
                                         RECORDING_FILE_EXTENSION)
        super(Command, self).__init__(*args, **kwargs)

    def check_file(self, file_name, recordings=None):
        if recordings is None:
            recordings = []
        if file_name in recordings or \
                not file_name.endswith(self.file_extension):
            return False
        return True

    def get_bucket(self):
        if not self.conn:
            self.conn = S3Connection(settings.AWS_ACCESS_KEY,
                                     settings.AWS_SECRET_KEY)
        if not self.bucket:
            self.bucket = self.conn.get_bucket(settings.AWS_BUCKET)
        return self.bucket

    def get_s3_files(self, get_objs=False, force_refresh=False):
        if not force_refresh:
            if get_objs:
                if self.s3_file_objs:
                    return self.s3_file_objs
            elif self.s3_files:
                return self.s3_files

        self.s3_files = []
        self.s3_file_objs = []
        bucket = self.get_bucket()
        for bucket_file in bucket.list():
            if bucket_file.name.endswith(self.file_extension):
                self.s3_file_objs.append(bucket_file)
                self.s3_files.append(os.path.basename(
                    bucket_file.generate_url(expires_in=0, query_auth=False)))
        if get_objs:
            return self.s3_file_objs
        return self.s3_files

    def sync_s3(self):
        for bucket_file in self.get_s3_files(get_objs=True):
            if not self.check_file(bucket_file.name):
                continue
            url = bucket_file.generate_url(expires_in=0, query_auth=False)
            try:
                ClassRecording.objects.get(url=url)
                continue
            except ClassRecording.DoesNotExist:
                cr = ClassRecording(url=url)
                cr.save()

                self.stdout.write(
                    self.style.SUCCESS('Saved {}'.format(cr.__unicode__())))
                self.new_recordings.append(cr)

    def upload_directory(self, recording_path):
        """
        Uploads recording files to S3 from recording_path.

        :param recording_path: str: Directory path of where to find files.
        """
        if not os.path.isdir(recording_path):
            self.stdout.write(self.style.ERROR('Invalid directory: {}'.format(
                recording_path)))
            return None
        recordings = self.get_s3_files()
        bucket = self.get_bucket()
        for file_name in os.listdir(recording_path):
            if not self.check_file(file_name, recordings):
                continue
            try:
                obj = ClassRecording.objects.get(url__contains=file_name)
                if self.debug:
                    self.stdout.write(
                        'Found {} already exists'.format(obj.name))
                continue
            except ClassRecording.DoesNotExist:
                pass
            self.stdout.write(self.style.NOTICE(
                'Preparing to upload {}'.format(file_name)))
            file_path = os.path.join(recording_path, file_name)
            file_size = os.stat(file_path).st_size
            mp = bucket.initiate_multipart_upload(file_name)
            chunk_size = AWS_S3_CHUNK_SIZE
            chunk_count = int(math.ceil(file_size / float(chunk_size)))

            for i in range(chunk_count):
                offset = chunk_size * i
                with FileChunkIO(
                        file_path, 'r', offset=offset,
                        bytes=min(chunk_size, file_size - offset)) as fp:
                    mp.upload_part_from_file(fp, part_num=i + 1)
            mp.complete_upload()
            bucket.make_public()

    def post_to_slack(self):
        if not settings.SLACK_API_TOKEN:
            logger.error('No Slack Token Defined -- Aborting Post to Slack')
            return
        if not self.new_recordings:
            logger.info('No new recordings to post to Slack.')
            return
        urls = [cr.url for cr in self.new_recordings]
        sc = SlackClient(settings.SLACK_API_TOKEN)
        urls_txt = '<{}>'.format('>\n<'.join(urls))
        sc.api_call('chat.postMessage', channel='#python',
                    text='New class recordings:\n{}'.format(urls_txt),
                    username='class_recordings',
                    icon_emoji=':robot_face:')
        self.stdout.write(
            self.style.SUCCESS('Posted \n'.format(urls_txt)))

    def handle(self, *args, **options):
        if options['debug']:
            self.debug = True
        if os.path.isdir(str(settings.RECORDING_PATH)):
            self.upload_directory(settings.RECORDING_PATH)
        self.sync_s3()
        if options['slack']:
            self.post_to_slack()
