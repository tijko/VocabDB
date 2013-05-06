#!/usr/bin/env python

import sqlite3
import argparse

from lib.query import reference
from lib.storage import WordLog 

##      find word of the day?

def options():
    parser = argparse.ArgumentParser(description='Vocabulary Database')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-L', '--lookup', help='Lookup a word\'s definition/s', 
                        action='store_true')
    group.add_argument('-R', '--retrieval', help='Attempt to retrieve a word from local database',
                        action='store_true')
    parser.add_argument('-D', '--dump', help='Empty the contents of local database',
                        action='store_true')
    parse = parser.parse_args()
    return parse


class Vocab(object):

    def __init__(self, options, word_to_lookup=''):
        wrdlg = WordLog()
        if options.lookup:
            while not word_to_lookup.isalpha():
                word_to_lookup = raw_input('Enter a word to lookup: ')
            definitions = reference(word_to_lookup)
            if not definitions:
                return
            store = raw_input('\nEnter "y" if you would like to store "%s"?: ' % 
                                                      word_to_lookup.capitalize())
            if store.lower() == 'y':
                wrdlg.create_database()
                wrdlg.word_entry(word_to_lookup, definitions)

        if options.retrieval:    
            while not word_to_lookup.isalpha():
                word_to_lookup = raw_input('Enter a word to lookup: ')    
            logged = wrdlg.word_retrieval(word_to_lookup)
            if not logged:
                print '\n"%s" has not been looked up before' % word_to_lookup
                ans = raw_input('\nEnter "y" if you would like to now?: ')
                if ans.lower() == 'y':
                    definitions = reference(word_to_lookup)
                    if not definitions:
                        return
                    wrdlg.create_database() 
                    wrdlg.word_entry(word_to_lookup, definitions)
            return

        if options.dump:
            print 'Saving to vocab.txt in home directory'
            wrdlg.all_word_dump()

        if (not options.dump and
            not options.retrieval and
            not options.lookup):
            print """Supply an argument when running the program. 
                     see help -- python main.py -h"""
            return


if __name__ == '__main__':
    opts = options()
    vcab = Vocab(opts)



