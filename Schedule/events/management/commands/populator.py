from django.core.management.base import BaseCommand
from optparse import make_option
import urllib.request
import csv
import copy
import itertools
import re
from events.models import Activity


class Database(object):

    def __init__(self):
        self.plan = {}

    def add(self, name, value, key):

        if name == '':
            name = 'unallocated'

        if name not in self.plan:
            self.plan[name] = {key: [value]}

        elif key not in self.plan[name]:
            s = copy.deepcopy(value)
            self.plan[name][key] = [s]
        else:
            self.plan[name][key].append(value)

    def add_single(self, name, value, key):
        self.plan[name][key] = value

    def remove_useless(self):
        self.plan.pop('Students Sets', None)

    def cleanDuplicates(self, group):
        temp = group[0]
        sav = [i[2] for i in group]
        hours = [i.replace(':', '.') for i in sav]
        c = [i.split('-') for i in hours]
        hours = list(itertools.chain(*c))
        hour = min(hours) + '-' + max(hours)
        temp[2] = hour
        return temp

    def fix_Rooms(self, name, key):
        pattern = re.compile(u'\w{1}-\d{1,3}[a-z]?', re.U)
        i = self.plan[name][key][7]
        m = pattern.findall(i)
        if m == []:
            m = ['Ł-1']
        # print(m[0])
        self.plan[name][key][7] = m[0]

    def fix_Tags(self, name, key):
        i = self.plan[name][key][6]
        pattern = re.compile(u'^[^(\+)]+', re.U)
        m = pattern.findall(i)
        if i == '':
            m = ['None']
        elif (i[0] == '(' and i[-1] == ')') or ('Zapisy' in i):
            m = ['Wychowanie fizyczne']
        self.plan[name][key][6] = m[0]

    def fix_Teachers(self, name, key):
        i = self.plan[name][key][5]
        print(i)
        i = i.split('+')
        for k in i:
            k = k.translate(dict.fromkeys(map(ord, u"?()~-0123456789"))).split(" ")
            if i == []:
                self.plan[name][key][5] = []
            else:
                self.plan[name][key][5] = i


def load_data():
    url = 'http://nwpei.prz.rzeszow.pl/~szczep/Lato2015_timetable.csv'
    resource = urllib.request.urlopen(url)
    reader = csv.reader(resource.read().decode('utf-8').splitlines())
    Sup = Database()

    for i in reader:
        group = i[3]
        key = i[0]
        Sup.add(group, i, key)

    Sup.remove_useless()

    for group in Sup.plan.keys():
        for i in Sup.plan[group].keys():
            s = Sup.cleanDuplicates(Sup.plan[group][i])
            del Sup.plan[group][i]
            Sup.add_single(group, s, s[0])

    K = Sup.plan
    for i in K:
        for j in K[i]:
            s = K[i][j]
            A = Activity(code=int(s[0]), Hour=s[2], Day=s[1],
                         Subject=s[4], Teachers=s[5], Students=s[3], Tag=s[6], Room=s[7], Comment=s[8])
            A.save()


class Command(BaseCommand):
    args = ''
    help = ''

    option_list = BaseCommand.option_list + (
        make_option('--add', action='store_true', dest='add', default=False, help='Clear teachers from local db'),
        make_option('--delete', action='store_true', dest='delete', default=False, help='Clear teachers from local db'),)

    def handle(self, *args, **options):
        if options['add']:
            load_data()
        if options['delete']:
            for i in Activity.objects.all():
                i.delete()
