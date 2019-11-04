from . import Directive


class Tails_redmine_starter(Directive):
    regex = r'\[\[!tails_redmine_starter\]\]'

    def newvalue(self, matchobj):
        return '{{{{< tails_redmine_starter >}}}}'
