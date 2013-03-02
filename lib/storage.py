import sqlite3
import collections

from os import environ


class WordLog(object):
    
    @staticmethod
    def create_database():
        con = sqlite3.connect(environ['HOME'] + '/.vocab.db')
        with con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Words(vocab_id INTEGER PRIMARY KEY, vocab TEXT)""")
            cur.execute("""CREATE TABLE IF NOT EXISTS Definitions
                                                    (def_id INTEGER, 
                                                     def  TEXT, 
                                                     def_word INTEGER, 
                                                     FOREIGN KEY(def_word) REFERENCES Words(vocab_id))""")
        con.commit()
        con.close()

    def word_entry(self, word, definitions):
        def_cnt = 1
        self.word = word
        self.definitions = definitions
        con = sqlite3.connect(environ['HOME'] + '/.vocab.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Words")
            wrd_tbl = cur.fetchall()
            cur.execute("INSERT INTO Words VALUES(?,?)", (len(wrd_tbl),
                                                            self.word))
            cur = con.cursor()
            cur.execute("SELECT * FROM Definitions")
            def_tbl = cur.fetchall()
            for row in def_tbl:
                def_cnt += 1
            for entry in self.definitions:
                cur.execute("INSERT INTO Definitions VALUES(?,?,?)", (def_cnt, 
                                                                      self.definitions[entry], 
                                                                      len(wrd_tbl)))
                def_cnt += 1
            print '-' * 10
            print "You now have %d entries\n" % (len(wrd_tbl) + 1)

    def word_retrieval(self, word):
        self.word = word
        con = sqlite3.connect(environ['HOME'] + '/.vocab.db')
        with con:
            cur = con.cursor()
            cur.execute('SELECT * FROM Words WHERE vocab=?', [self.word])
            query_wrd = cur.fetchone()
        if not query_wrd:
            return 0 
        if query_wrd:
            with con:
                cur = con.cursor()
                cur.execute('SELECT * FROM Definitions where def_word=?', [query_wrd[0]])
                query_def = cur.fetchall()     
            print '\n%s:' % self.word.capitalize()
            print '-' * 10
            for entry in query_def:
                print '\n    Definition %d: %s' % (query_def.index(entry) + 1,
                                                    entry[1])
            print ''
            return 1
    
    def all_word_dump(self):
        con = sqlite3.connect(environ['HOME'] + '/.vocab.db')
        with con:
            cur = con.cursor()
            cur.execute('SELECT * FROM Words')
            all_wrds = {str(k):v for k,v in [i for i in cur.fetchall()]}
            cur = con.cursor()
            cur.execute('SELECT * FROM Definitions')
            all_defs = cur.fetchall()
        wrd_def = collections.defaultdict(list)
        for entry in all_defs:      
            wrd_def[str(entry[2])].append(entry[1])
        with open(environ['HOME'] + '/vocab.txt', 'a+') as f:
            for k in wrd_def:
                f.write('\n'+all_wrds[k].capitalize()+'\n')
                for d in wrd_def[k]:
                    f.write('\n    '+d+'\n')

