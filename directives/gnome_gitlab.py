from . import Directive


class Gnome_gitlab(Directive):
    regex = r'\[\[!gnome_gitlab\s*(?P<path>\S+)\s*(desc="(?P<description>.+?)"\s*)?\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'path': self.cleanvalue(matchobj.group('path')),
            'description': self.cleanvalue(matchobj.group('description'))
        }
        return '{{{{< gnome_gitlab {} >}}}}'.format(self.concatargumentdict(namedarguments))
