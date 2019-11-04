from . import Directive


class Ikiwikilink_with_name(Directive):
    regex = r'\[\[(?P<text>\w.(?s)+?)\|(?P<target>.(?s)+?)\]\]'

    def newvalue(self, matchobj):
        path = self.cleanvalue(matchobj.group('target'))
        text = self.cleanvalue(matchobj.group('text'))
        if path.split('/')[0] in self.firstlevel:
            path = '/' + matchobj.group('target')
        return "[{}]({})".format(text, path)
