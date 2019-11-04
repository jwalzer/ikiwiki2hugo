from . import Directive


class Ikiwikilink(Directive):
    regex = r'\[\[(?P<targetandtext>[^\!]\w[^|]+?)\]\]'

    def newvalue(self, matchobj):
        target = self.cleanvalue(matchobj.group('targetandtext'))
        text = target
        if not target.startswith('http'):
            target = '/' + target
        return "[{}]({})".format(target, text)
