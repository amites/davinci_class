import math
import os

from boto.s3.connection import S3Connection
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from filechunkio import FileChunkIO

from recordings.models import ClassRecording


AWS_S3_CHUNK_SIZE = 52428800  # Default to 50MB chunks


class Command(BaseCommand):
    help = 'Scans S3 for classes to add to the db.'

    def add_arguments(self, parser):
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     dest='delete',
        #     default=False,
        #     help='Delete poll instead of closing it',
        # )
        pass

    def __init__(self, *args, **kwargs):
        self.conn = None
        self.bucket = None
        super(Command, self).__init__(*args, **kwargs)

    def get_bucket(self):
        if not self.conn:
            self.conn = S3Connection(settings.AWS_ACCESS_KEY,
                                     settings.AWS_SECRET_KEY)
        if not self.bucket:
            self.bucket = self.conn.get_bucket(settings.AWS_BUCKET)
        return self.bucket

    def sync_s3(self):
        bucket = self.get_bucket()
        for bucket_file in bucket.list():
            if bucket_file.name.endswith('m4a'):
                url = bucket_file.generate_url(expires_in=0, query_auth=False)
                try:
                    ClassRecording.objects.get(url=url)
                    continue
                except ClassRecording.DoesNotExist:
                    cr = ClassRecording(url=url)
                    cr.save()

                    self.stdout.write(
                        self.style.SUCCESS('Saved {}'.format(cr.__unicode__())))

    def upload_directory(self, recording_path):
        if not os.path.isdir(recording_path):
            self.stdout.write(self.style.ERROR('Invalid directory: {}'.format(
                recording_path)))
            return None
        for fname in os.listdir(recording_path):
            if fname.endswith('mp4'):
                try:
                    ClassRecording.objects.get(url__contains=fname)
                    continue
                except ClassRecording.DoesNotExist:
                    pass
                bucket = self.get_bucket()
                file_path = os.path.join(recording_path, fname)
                file_size = os.stat(file_path).st_size
                mp = bucket.initiate_multipart_upload(fname)
                chunk_size = AWS_S3_CHUNK_SIZE
                chunk_count = int(math.ceil(file_size / float(chunk_size)))

                for i in range(chunk_count):
                    offset = chunk_size * i
                    with FileChunkIO(
                            file_path, 'r', offset=offset,
                            bytes=min(chunk_size, file_size - offset)) as fp:
                        mp.upload_part_from_file(fp, part_num=i + 1)
                mp.complete_upload()

    def handle(self, *args, **options):
        if os.path.isdir(str(settings.RECORDING_PATH)):
            self.upload_directory(settings.RECORDING_PATH)
        self.sync_s3()
