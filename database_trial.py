#! /usr/bin/env python
import mechanize
from BeautifulSoup import BeautifulSoup
import sys
import sqlite3

class Vocab:
    def __init__(self):
        self.word = sys.argv[1] 
        self.def_count = 1
        self.query = {}
        
    def dictionary(self,word):
        br = mechanize.Browser()
        response = br.open('http://www.dictionary.reference.com')
        br.select_form(nr=0)
        br.form['q'] = word 
        br.submit()
        definition = BeautifulSoup(br.response().read())
        trans = definition.findAll('td',{'class':'td3n2'})
        fin = [i.text for i in trans]
        for i in fin: 
            self.query[fin.index(i)] = i
        self.word_database()
        return self.query

    def word_database(self):
        con = sqlite3.connect('/home/oberon/vocab_database/vocab.db')
        with con:
            spot = con.cursor()
            spot.execute("SELECT * FROM Words")
            rows = spot.fetchall() 
            spot.execute("INSERT INTO Words VALUES(?,?)", (len(rows),self.word))
            spot = con.cursor()
            spot.execute("SELECT * FROM Definitions")
            rows_two = spot.fetchall()
            for row in rows_two:
                self.def_count += 1
            for q in self.query:
                spot.execute("INSERT INTO Definitions VALUES(?,?,?)", (self.def_count,self.query[q],len(rows)))
                self.def_count += 1
        
print Vocab().dictionary(sys.argv[1])  



