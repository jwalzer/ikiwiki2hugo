import re


class Directive:
    firstlevel = set()
    regex = None

    def __init__(self, firstlevel):
        self.firstlevel = firstlevel

    def getregex(self):
        return re.compile(self.regex)

    def replace(self, content):
        return re.sub(self.getregex(), self.newvalue, content)

    def newvalue(self, matchobj):
        raise NotImplementedError

    #####
    # helper functions
    #####

    def cleanvalue(self, value):
        if value:
            return value.replace('\n', ' ')
        return None

    def concatargumentdict(self, argumentdict):
        arguments = []
        for key in argumentdict:
            if argumentdict[key]:
                arguments.append('{}="{}"'.format(key, argumentdict[key]))
        return " ".join(arguments)
