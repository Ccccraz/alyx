import inspect
import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from alyx.base import alyx_mail
from actions.models import Surgery, WaterRestriction
from subjects.models import Subject, StockManager

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate daily reports"

    def add_arguments(self, parser):
        parser.add_argument('-U', '--users', nargs='*',
                            help='Usernames')
        parser.add_argument('names', nargs='*',
                            help='List of reports to make')
        parser.add_argument('--list', action='store_true', default=False,
                            help="List of available reports")
        parser.add_argument('--no-email', action='store_true', default=False,
                            help="Show report without sending an email")

    def handle(self, *args, **options):
        if options.get('list'):
            methods = inspect.getmembers(self, predicate=inspect.ismethod)
            names = sorted([m[0][5:] for m in methods if m[0].startswith('make_')])
            self.stdout.write(', '.join(names))
            return
        self.do_send = not options.get('no_email')
        users = options.get('users')
        users = (User.objects.filter(username__in=users).order_by('username')
                 if users else User.objects.all())
        for name in options.get('names'):
            method = getattr(self, 'make_%s' % name, None)
            if method:
                self.stdout.write("Making report %s." % name)
                # Global reports for admins.
                if name in ('actions',):
                    method()
                else:
                    for user in users:
                        method(user)

    def _send(self, to, subject, text=''):
        self.stdout.write('"[alyx] %s" sent to %s.\n\n' % (subject, to))
        self.stdout.write(text)
        self.stdout.write("\n\n")
        if self.do_send:
            alyx_mail(to, subject, text)

    def make_water_restriction(self, user):
        wr = WaterRestriction.objects.filter(start_time__isnull=False,
                                             end_time__isnull=True,
                                             subject__responsible_user=user,
                                             ).order_by('subject__nickname')
        if not wr:
            return
        if not user.email:
            logger.warn("Skipping user %s because there is no email.", user.username)
            return
        subject = '%d mice on water restriction' % len(wr)
        text = "Mice on water restriction:\n"
        text += '\n'.join('* %s since %s' % (w.subject.nickname, w.start_time.date())
                          for w in wr)
        self._send(user.email, subject, text)

    def make_surgery(self, user):
        surgery_done = set([surgery.subject.nickname for surgery in
                            Surgery.objects.filter(subject__responsible_user=user)])
        subjects_user = set([subject.nickname for subject in
                             Subject.objects.filter(responsible_user=user)])
        surgery_pending = sorted(subjects_user - surgery_done)
        if not surgery_pending:
            return
        if not user.email:
            logger.warn("Skipping user %s because there is no email.", user.username)
            return
        subject = '%d mice awaiting surgery' % len(surgery_pending)
        text = "Mice awaiting surgery:\n"
        text += '\n'.join('* %s' % nickname for nickname in surgery_pending)
        self._send(user.email, subject, text)

    def make_actions(self):
        tbg = Subject.objects.filter(to_be_genotyped=True).order_by('nickname')
        tbc = Subject.objects.filter(to_be_culled=True).order_by('nickname')
        tbr = Subject.objects.filter(death_date__isnull=False,
                                     reduced=False).order_by('nickname')
        subject = '%d mice awaiting action' % (len(tbg) + len(tbc) + len(tbr))

        text = "%d mice to be genotyped:\n" % len(tbg)
        text += '\n'.join('* %s' % s.nickname for s in tbg)

        text += "\n\n%d mice to be culled:\n" % len(tbc)
        text += '\n'.join('* %s' % s.nickname for s in tbc)

        text += "\n\n%d mice to be reduced:\n" % len(tbr)
        text += '\n'.join('* %s' % s.nickname for s in tbr)

        to = [sm.user.email for sm in StockManager.objects.all() if sm.user.email]
        self._send(to, subject, text)
