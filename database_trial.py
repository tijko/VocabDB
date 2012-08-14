#! /usr/bin/env python
import mechanize
from BeautifulSoup import BeautifulSoup
import sys
import sqlite3

def dictionary(word):
    br = mechanize.Browser()
    response = br.open('http://www.dictionary.reference.com')
    br.select_form(nr=0)
    br.form['q'] = word 
    br.submit()
    definition = BeautifulSoup(br.response().read())
    trans = definition.findAll('td',{'class':'td3n2'})
    fin = [i.text for i in trans]
    query = {}
    word_count = 1
    def_count = 1
    for i in fin: 
        query[fin.index(i)] = i
    con = sqlite3.connect('/home/oberon/vocab_database/vocab.db')
    with con:
        spot = con.cursor()
        spot.execute("SELECT * FROM Words")
        rows = spot.fetchall()
        for row in rows:
            word_count += 1
        spot.execute("INSERT INTO Words VALUES(?,?)", (word_count,word))
        spot.execute("SELECT * FROM Definitions")
        rows = spot.fetchall()
        for row in rows:
            def_count += 1
        for q in query:
            spot.execute("INSERT INTO Definitions VALUES(?,?,?)", (def_count,query[q],word_count))
            def_count += 1
    return query

print dictionary(sys.argv[1])  

