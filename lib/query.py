#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mechanize

from storage import WordLog
from BeautifulSoup import BeautifulSoup


def reference(word):
    br = mechanize.Browser()
    response = br.open('http://www.dictionary.reference.com')
    br.select_form(nr=0)
    br.form['q'] = word
    br.submit()
    definition = BeautifulSoup(br.response().read())
    trans = definition.findAll('td', {'class':'td3n2'})
    if not trans:
        return '\nNo Definitions! Check your spelling...\n'
    else:
        definitions = {trans.index(i):i.text for i in trans}
        print '\n%s:' % word.capitalize() 
        print '-' * 10
        for entry in definitions:
            print '\n    Definition %d: %s' % (entry + 1, definitions[entry])
        print ''
    return definitions
