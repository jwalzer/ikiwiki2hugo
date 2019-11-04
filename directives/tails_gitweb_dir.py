from . import Directive


class Tails_gitweb_dir(Directive):
    regex = r'\[\[!tails_gitweb_dir\s+((?P<directory>[\w@._/-]+)\s*|desc="(?P<description>.(?s)+?)"\s*)*\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'directory': self.cleanvalue(matchobj.group('directory')),
            'description': self.cleanvalue(matchobj.group('description')),
        }
        return '{{{{< tails_gitweb_dir {} >}}}}'.format(self.concatargumentdict(namedarguments))
