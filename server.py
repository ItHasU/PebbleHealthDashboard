#!/usr/bin/python2
#-*- coding: utf-8 -*-

import sqlite3, json

#-- Database part -------------------------------------------------------------

class HealthDatabase:
    def __init__(self, filename="health.db"):
        self.db = sqlite3.connect(filename)
        c = self.db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS health (user text, date text, steps integer, heartrate integer, mask integer)''')
        c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS user_date ON health (user, date);''')

    def push(self, line, userId=""):
        print(line)
        # Parse line
        try:
            values = line.split(",")
            if len(values) != 7:
                return False
            date = values[0] #time.mktime(time.strptime(values[0], '%Y-%m-%dT%H:%M:00Z'))
            steps = int(values[1])
            heartrate = 0
            mask = int(values[6])
        except Exception as e:
            print("%s: %s" % (e, line.strip()))
            return False
        # Insert
        c = self.db.cursor()
        try:
            c.execute("INSERT INTO health VALUES (?, ?, ?, ?, ?)", (userId, date, steps, None, mask, ))
        except sqlite3.IntegrityError:
            pass
        return True

    def get_all(self, userId = ""):
        c = self.db.cursor()
        c.execute("SELECT * FROM health WHERE user=?", (userId,))
        return c

    def get_steps_by_day_json(self, userId=''):
        c = self.db.cursor()
        steps = []
        heartrate = []
        c.execute("SELECT strftime('%s', date, 'localtime'), SUM(steps), AVG(heartrate) FROM health WHERE user=? GROUP BY strftime('%Y-%m-%d', date, 'localtime')", (userId,))
        while True:
            r = c.fetchone()
            if not r:
                break
            steps.append([int(r[0])*1000, r[1]])
            heartrate.append([int(r[0])*1000, r[2]])
        return json.dumps({"steps": steps, "heartrate": heartrate})

    def get_sleep_by_day_json(self, userId=''):
        c = self.db.cursor()
        sleep = []
        c.execute("""SELECT strftime('%s', date, 'localtime'), COUNT(*) FROM health WHERE user=? AND (mask = 3 OR mask = 1) GROUP BY strftime('%Y-%m-%d', date, '+12 hours', 'localtime')""", (userId,))
        while True:
            r = c.fetchone()
            if not r:
                break
            sleep.append([int(r[0])*1000, r[1]])
        return json.dumps({"sleep": sleep})

    def get_by_week(self, userId = ""):
        return self.get_by_format('%Y-%W', userId)

    def get_by_format(self, format, userId):
        c = self.db.cursor()
        c.execute("SELECT strftime(?, date), SUM(steps), AVG(heartrate) FROM health WHERE user=? GROUP BY strftime(?, date)", (format, userId, format,))
        return c

    def close(self):
        self.db.commit()
        self.db.close()

#-- Server part ---------------------------------------------------------------

from sys import version as python_version
from cgi import parse_header, parse_multipart
from urlparse import parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SimpleHTTPServer

class HealthRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length), 
                    keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def do_POST(self):
        global db
        self._set_headers()
        postvars = self.parse_POST()
        # We don't care about key, just get all
        for v in postvars.values():
            for line in v[0].split('|'):
                db.push(line)
        # Terminate
        self.wfile.write("{}")
        self.wfile.close()
        return

    def do_GET(self):
        global db
        if self.path == "/api/data":
            self._set_headers()
            self.wfile.write(db.get_steps_by_day_json())
            self.wfile.close()
        elif self.path == "/api/data2":
            self._set_headers()
            self.wfile.write(db.get_sleep_by_day_json())
            self.wfile.close()
        else:
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

#-- Script --------------------------------------------------------------------

def script_insert(csv_filename, db_filename):
    db = HealthDatabase(db_filename)

    print("Pushing data ...")
    fp = open(csv_filename, "r")
    count = 0
    while True:
        line = fp.readline()
        if not line:
            break
        if db.push(line):
            count += 1
    fp.close()
    print("Pushed %d line(s)" % (count))
    return db

if __name__ == "__main__":
    import sys
    #script_insert("data.csv", "health.db")
    global db
    db = HealthDatabase()

    server = HTTPServer(("", 5000), HealthRequestHandler)
    server.serve_forever()

    db.close()
    exit(0)

    c = db.get_by_day()
    while True:
        r = c.fetchone()
        if not r:
            break
        print r

    c = db.get_by_week()
    while True:
        r = c.fetchone()
        if not r:
            break
        print r

