import datetime
import os
import shutil
from logging import getLogger

from django.conf import settings
from django.template.defaultfilters import slugify
from six.moves import input  # Py2 + Py3 compatible
from slackclient import SlackClient

from recordings.models import ClassRecording, Course, CourseSession, SessionReference
from recordings.management.commands.sync_recordings_s3 import SyncS3Command


logger = getLogger(__name__)
AWS_S3_CHUNK_SIZE = 52428800  # Default to 50MB chunks


class Command(SyncS3Command):
    def __init__(self, *args, **kwargs):
        self.bucket = None
        self.conn = None
        self.debug = False
        self.new_recordings = []
        self.new_urls = []
        self.course = Course.objects.get(pk=settings.CURRENT_COURSE)
        self._session = None
        self._session_date = None
        self._session_num = None
        self._session_name = None

        self.recording_path = settings.RECORDING_PATH
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
                self.new_recordings.append(os.path.join(self.recording_hold_path, file_name))

        # TODO: add parser for course git repo to pickup new files to add to session resources

    @property
    def session_date(self):
        if self._session_date:
            return self._session_date
        date_str = '%Y-%m-%d'
        today = datetime.date.today()
        session_date = None
        while not session_date:
            user_date_str = input('Enter class date ({}): '.format(today.strftime(date_str)))
            if user_date_str:
                try:
                    session_date = datetime.datetime.strptime(user_date_str, date_str)
                except ValueError:
                    continue
            session_date = today
        self._session_date = session_date
        return self._session_date

    @property
    def session_num(self):
        if self._session_num:
            return self._session_num

        last_session = CourseSession.objects.filter(course__id=settings.CURRENT_COURSE).order_by('-date').last()

        session_default = last_session.num + 1

        # keep asking until valid answer
        while not self._session_num:
            input_num = input('Session number? (Leave empty for default {}): '.format(session_default))
            if not input_num:
                self._session_num = session_default
            elif str(input_num).isdigit():
                self._session_num = int(input_num)
                try:
                    CourseSession.objects.get(course=self.course, num=self._session_num)
                    check_session = input('Session with number {} found, is that correct? [y/n]: ')
                    if check_session.lower() in ['n', 'no']:
                        self._session_num = None
                except CourseSession.DoesNotExist:
                    pass
            else:
                print('{} is not a valid number, try again'.format(input_num))
        return self._session_num

    @property
    def session(self):
        # create new CourseSession
        if not self._session_name:
            self._session_name = input('Enter a name for the session (blank): ')

        try:
            self._session = CourseSession.objects.get(date=self.session_date, course=self.course)
        except CourseSession.DoesNotExist:
            self._session = CourseSession(date=self.session_date, course=self.course, num=self.session_num)

        if self._session_name:
            self._session.name = self._session_name
        self._session.save()
        return self._session

    def add_recordings(self):
        # create ClassRecording entries
        # TODO: add check of old session numbers to see if duplicates

        # TODO: add input to check if single recordings have code wars
        # TODO: add input to check if single recordings have additional resources

        upload_files = []
        for file_path in self.new_recordings:
            short_name = os.path.basename(file_path).rstrip('.{}'.format(settings.RECORDING_FILE_EXTENSION))
            recording_name = input('Short name for session part [{}]: '.format(' - '.join(short_name.split('--'))))

            old_file_name = os.path.basename(file_path)
            slugged_name = slugify(old_file_name).rstrip('.{}'.format(settings.RECORDING_FILE_EXTENSION))
            if recording_name:
                slugged_name += '--{}'.format(slugify(recording_name))
            file_name = '{date}--class-{session_num}--{name}.{ext}'.format(
                date=self.session_date, session_num=self.session_num, name=slugged_name,
                ext=settings.RECORDING_FILE_EXTENSION)
            upload_files.append({
                'file_path': file_path,
                'file_name': file_name,
                'short_name': short_name,
                'session': self.session,
            })

        self.upload_create_recording_files(upload_files)

    def upload_create_recording_files(self, upload_files):
        session_part = 1
        for file_args in upload_files:
            key = self.handle_session_recording_file(file_args['file_path'], file_args['file_name'])
            short_name = file_args['short_name']

            if len(short_name.split('--')) > 1:
                session_part_str = file_args['short_name'].split('--')[0]
                if session_part_str.isdigit():
                    session_part = int(session_part_str)

            if len(short_name.split('--')) > 1:
                short_name = short_name.split('--')[1]
            display_name = ' '.join(short_name.split('-')).title()
            obj = ClassRecording(session=file_args['session'], url=key.generate_url(expires_in=0, query_auth=False),
                                 name=display_name, class_part=session_part)
            obj.save()

            session_part += 1

    def add_session_codewars(self, recording):
        # ask if session is codewars
        # if so get from user
            # url problem
                # use requests to pull web-page and scrape data
            # url solution (github)
                # use requests to save the raw code to a db TextField
            # code snippet?
        pass

    def add_session_resource(self):
        # ask if additional resource
        # if so get from user
            # url
            # gist url
            # parse file for snippet?
        added = False
        while True:
            has_resource = input('Is there {} resource for this session? [y/n]: '.format('a' if added else 'another'))
            if has_resource.lower() not in ['y', 'yes']:
                break
            resource_url = input('Enter resource url if there is one: ')
            resource_gist = input('Enter gist_url if there is one: ')

            # TODO: validate that url is valid in form
            # TODO: validate that url exists, include setting to disable check

            # TODO: load contents of snippet file
            # resource_snippet_file = input('Enter snippet file path if there is one: ')

            # TODO: add logic to connect to specific recording

            if not resource_url and not resource_gist:
                continue

            name = input('Enter resource name (optional): ')
            kwargs = {
                'name': name if name else None,
                'session': self.session,
                'url': resource_url if resource_url else None,
                'gist_url': resource_gist if resource_gist else None,
            }

            SessionReference.objects.create(**kwargs)

    def handle_session_recording_file(self, file_path, file_name):
        # upload file to bucket
        s3_file_name = os.path.join(self.course.slug, file_name)
        self.upload_file(file_path, s3_file_name)
        bucket = self.get_bucket()
        key = bucket.new_key(s3_file_name)
        key.make_public()

        self.new_urls.append(key.generate_url(expires_in=0, query_auth=False))

        # move old file to new path (hold to store)
        shutil.move(file_path, os.path.join(self.recording_path, file_name))
        return key

    def announce(self):
        # post notification of new session references to slack
        if not settings.SLACK_API_TOKEN:
            print('No Slack Token Defined -- Aborting Post to Slack')
            return
        if not self.new_recordings:
            print('No new recordings to post to Slack.')
            return

        sc = SlackClient(settings.SLACK_API_TOKEN)
        urls_txt = '<{}>'.format('>\n<'.join(self.new_urls))
        sc.api_call('chat.postMessage', channel=settings.SLACK_CHANNEL,
                    text='New class recordings:\n{}'.format(urls_txt),
                    username='davinci_class',
                    icon_emoji=':robot_face:')
        self.stdout.write(self.style.SUCCESS('Posted \n'.format(urls_txt)))

    def handle(self, *args, **options):
        if options['debug']:
            self.debug = True

        if not os.path.isdir(settings.RECORDING_HOLD_PATH):
            raise OSError('Directory {} does not exist or not defined.'.format(settings.RECORDING_HOLD_PATH))

        self.load_files()

        # pre-load class session data
        self.session
        self.session_date

        self.add_recordings()
        self.add_session_resource()
        self.announce()
