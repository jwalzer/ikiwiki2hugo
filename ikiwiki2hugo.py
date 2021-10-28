#!/usr/bin/python3
#
# Copyright (c) 2019 Birger Schacht
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.
#
# pylint: disable=C0301,C0111
import importlib
import re
import pathlib
import shutil
import sys
import pkgutil
import polib
import yaml
import os
import time

import directives


class Convert:
    firstlevel = set()
    directives = None

    def __init__(self, directory):
        # some directives need info about existing structure
        # so we are generating a list of first level elements
        self.genfirstlevel(directory)

        # get a list of all directive plugins
        self.directives = {
            name.split('.')[-1].capitalize(): importlib.import_module(name)
            for finder, name, ispkg
            in self.iter_namespace(directives)
        }

    #####
    # helper functions
    #####

    def genfirstlevel(self, directory):
        firstleveldirs = [x.name for x in pathlib.Path(directory).glob('*') if x.is_dir()]
        firstlevelfiles = [x.name.split('.')[0] for x in pathlib.Path(directory).glob('*') if x.is_file()]
        for name in firstleveldirs:
            self.firstlevel.add(name)
        for name in firstlevelfiles:
            self.firstlevel.add(name)

    # this is based on  https://packaging.python.org/guides/creating-and-discovering-plugins/
    def iter_namespace(self, ns_pkg):
        # Specifying the second argument (prefix) to iter_modules makes the
        # returned name an absolute name instead of a relative one. This allows
        # import_module to work without having to do additional modification to
        # the name.
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

    #####
    # more complex replacements
    #####

    def toggleable_repl(self, matchobj):
        return ''

    def toggle_repl(self, matchobj):
        tid = matchobj.group('id')
        text = matchobj.group('text')
        if text and text != 'X':
            toggleable_re = re.compile(r'\[\[!toggleable id="' + tid + r'" text="""(?P<text>.+?)"""\]\]', re.DOTALL)
            toggleable = re.search(toggleable_re, matchobj.string)
            details = toggleable.group('text')
            return '<details>\n<summary>{}</summary>\n{}\n</details>'.format(text, details)
        return ''

    def ikiwikilink(self, content):
        openbrackets_re = re.compile(r'\[\[[^!]')
        match = True
        while match:
            match = re.search(openbrackets_re, content)
            if match:
                openingbracket = match.start()
                closingbracket = match.start()
                bracketcounter = 0
                for i in range(openingbracket, len(content) - 1):
                    if content[i] == '[' and content[i + 1] == '[':
                        bracketcounter = bracketcounter + 1
                    if content[i] == ']' and content[i + 1] == ']':
                        bracketcounter = bracketcounter - 1
                    if bracketcounter == 0:
                        closingbracket = i
                        break
                if closingbracket > openingbracket:
                    pipeindex = content.rfind('|', openingbracket, closingbracket)
                    if pipeindex != -1:
                        text = content[openingbracket + 2:pipeindex]
                        target = content[pipeindex + 1:closingbracket].replace(' ', '_')
                    else:
                        text = content[openingbracket + 2:closingbracket]
                        target = text.replace(' ', '_')
                    content = content.replace(content[openingbracket:closingbracket + 2], "[{}]({})".format(text, target))
                else:
                    content = content.replace(content[openingbracket:closingbracket + 2], "[ [")
        return content

    #####
    # convert the content
    #####

    def ikiwiki2hugocontent(self, content):
        # go through all the directive plugins and let them
        # do their thing on the content strings
        for key in self.directives:
            class_ = getattr(self.directives[key], key)
            instance = class_(self.firstlevel)
            content = instance.replace(content)

        content = self.ikiwikilink(content)
        # here the order is important: we access the toggleable directives
        # in the toggle replacement function, so toglleablerepl, which
        # removes them, should only be called after togglere
        # also we are calling the togglere function two times to
        # catch nested [[!toggle's
        toggle = re.compile(r'\[\[!toggle\s+id="(?P<id>.+?)"\s+text="(?P<text>.*?)"\]\]', re.DOTALL)
        toggleable = re.compile(r'\[\[!toggleable id="(?P<id>.+?)" text="""(?P<text>.+?)"""\]\]', re.DOTALL)

        content = re.sub(toggle, self.toggle_repl, content)
        content = re.sub(toggle, self.toggle_repl, content)
        content = re.sub(toggleable, self.toggleable_repl, content)
        return content

    #####
    # generate the hugo frontmatter
    #####

    def ikiwiki2hugofrontmatter(self, content, file_stat):
        data = {}

        # replace [[!pagetemplate ...]] with a layout entry
        pagetemplate = re.compile(r'\[\[!pagetemplate\s+template="(?P<template>\w+).tmpl"\]\]')
        layout = pagetemplate.search(content)
        if layout:
            data['layout'] = layout.group('template')
        content = pagetemplate.sub('', content)

        # replace [[!tag ...]] with an array of tags
        tag = re.compile(r'\[\[!tag (?P<tag>.+)\]\]')
        taglist = tag.findall(content)
        if taglist:

            data['tags'] = " ".join(taglist).split()
        content = tag.sub('', content)

        # replace [[!meta stylesheet...]] with a stylesheets array
        stylesheet = re.compile(r'\[\[!meta stylesheet="(?P<path>.+?)" rel="stylesheet"( title="")?\]\]')
        stylesheets = stylesheet.finditer(content)
        if stylesheets:
            data['stylesheets'] = [stylesheet.group('path') for stylesheet in stylesheets]
        content = stylesheet.sub('', content)

        # replace [[!meta link...]] with a links array
        meta_link = re.compile(r'\[\[!meta link="(?P<url>.+?)" rel="(?P<rel>[\w-]+?)"\]\]')
        links = meta_link.finditer(content)
        if links:
            data['links'] = dict([(link.group('rel'), link.group('url')) for link in links])
        content = meta_link.sub('', content)

        meta = re.compile(r'\[\[!meta\s+(?P<key>[\w-]+)="?(?P<value>[^"\]]+)"?\]\]')
        metas = meta.findall(content)
        for key, value in metas:
            if key == 'updated':
                data['lastmod'] = value
            else:
                data[key] = value
        content = meta.sub('', content)

        # replace [[!meta title...]] with a title
        meta_title = re.compile(r'\[\[!meta title="(?P<title>.+?)" *\]\]')
        titles = meta_title.findall(content)
        if titles:
            data['title'] = "".join(titles)

        # replace [[!meta description...]] with a description
        meta_description = re.compile(r'\[\[!meta description="(?P<description>.+?)" *\]\]')
        descriptions = meta_description.findall(content)
        if descriptions:
            data['description'] = "".join(descriptions)

        # when no meta tag for lastmod then use file mtime
        if not "lastmod" in data:
            data['lastmod']=time.ctime(file_stat.st_mtime)

        return "{}{}\n{}".format(yaml.dump(data, indent=2, explicit_start=True, default_flow_style=False), '---', content)


class Wiki:
    ignore = []
    languages = []

    def __init__(self, path, outputdir, ignore, languages):
        self.path = path
        self.outputdir = outputdir
        self.ignore = ignore
        self.languages = languages

    def translate(self, file, pofile):
        original = file.read_text()
        poentries = polib.pofile(pofile)
        for entry in poentries.translated_entries():
            original = original.replace(entry.msgid, entry.msgstr)
        return original

    def work(self):
        out = pathlib.Path(self.outputdir)
        try:
            out.mkdir()
        except FileExistsError:
            print("The directory\n>> {}\nexists and I don't want to overwrite existing data, so I'm quitting for now...".format(out))
            exit(1)

        for file in pathlib.Path(self.path).rglob('*'):
            if file.name in self.ignore:
                continue
            if file.is_dir():
                pathlib.Path(out / file.relative_to(self.path)).mkdir(exist_ok=True)
            if file.match('*.mdwn') or file.match('*.html'):
                markdown = pathlib.Path(out / file.relative_to(self.path).with_suffix('.md'))
                if markdown.name == 'index.md':
                    markdown = markdown.parent / '_index.md'
                shutil.copy(file, markdown)
                shutil.copystat(file, markdown)
                for language in languages:
                    pofile = file.with_suffix('.' + language + '.po')
                    if pofile.exists():
                        translated = markdown.with_suffix('.' + language + '.md')
                        translated.write_text(self.translate(file, pofile))

            if file.match('*.css') or file.match('*.png') or file.match('*.jpg'):
                target = pathlib.Path(out / file.relative_to(self.path))
                shutil.copy(file, target)
                shutil.copystat(file, target)

        newfiles = pathlib.Path(outputdir).rglob('*.md')

        converter = Convert(out)
        for file in newfiles:
            print(file)
            stat=os.stat(file)
            newcontent = converter.ikiwiki2hugofrontmatter(file.read_text(),stat)
            newcontent = converter.ikiwiki2hugocontent(newcontent)
            file.write_text(newcontent)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: {} <ikiwikidirectory> <hugocontentdirectory>".format(sys.argv[0]))
        exit(1)

    ignore = ['brokenlinks.mdwn', 'shortcuts.mdwn']
    languages = ['de', 'es', 'fa', 'fr', 'it', 'pt']

    path = sys.argv[1]
    outputdir = sys.argv[2]
    w = Wiki(path, outputdir, ignore, languages)
    w.work()
