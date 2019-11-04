from . import Directive


class Tails_gitweb_commit(Directive):
    regex = r'\[\[!tails_gitweb_commit\s+(?P<commit>[^\s\]]+)\s*(desc="(?P<description>[^"]+?)")?[^\]]*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'commit': self.cleanvalue(matchobj.group('commit')),
            'description': self.cleanvalue(matchobj.group('description'))
        }
        return '{{{{ tails_gitweb_repo_commit {} >}}}}'.format(self.concatargumentdict(namedarguments))
