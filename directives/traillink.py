from . import Directive


class Traillink(Directive):
    regex = r'\[\[!traillink (?P<title>.+)\|(?P<path>.+)\]\]'

    def newvalue(self, matchobj):
        return "[{}]({})".format(matchobj.group('title'), matchobj.group('path'))
