from . import Directive


class Tails_gitweb_branch(Directive):
    regex = r'\[\[!tails_gitweb_branch\s+((?P<branch>[\w@._/-]+)\s*|desc="(?P<description>.(?s)+?)"\s*)*\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'branch': self.cleanvalue(matchobj.group('branch')),
            'description': self.cleanvalue(matchobj.group('description')),
        }
        return '{{{{< tails_gitweb_branch {} >}}}}'.format(self.concatargumentdict(namedarguments))
