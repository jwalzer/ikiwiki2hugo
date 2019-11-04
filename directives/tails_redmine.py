from . import Directive


class Tails_redmine(Directive):
    regex = r'\[\[!tails_redmine.*?desc="?(?P<description>.(?s)+?)"?\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'description': self.cleanvalue(matchobj.group('description'))
        }
        return '{{{{< tails_redmine {} >}}}}'.format(self.concatargumentdict(namedarguments))
