import re
import sqlite3

def do_karma(bot, user, channel, karma):
    if karma[1] == '++':
        k = 1
    else:
        k = -1

    conn = sqlite3.connect('karma.db')
    c = conn.cursor()
    t = (karma[0],)
    c.execute('select * from karma where word=?', t)
    res = c.fetchone()

    if res != None:
        u = k + res[2]
        q = (u,karma[0],)
        c.execute('update karma set karma = ? where word=?', q)
    else:
        u = k
        q = (karma[0],u,)
        c.execute('insert into karma (word, karma) VALUES (?,?)',q)
    
    conn.commit()
        
  
    return bot.say(channel, "Karma for %s is now %s" % (karma[0], u))


def handle_privmsg(bot, user, reply, msg):
    """Grab karma changes from the messages and handle them"""

    m = re.findall('([a-zA-Z0-9.-_]*)(\+\+|\-\-)', msg)
    if len(m) == 0: return None

    for k in m:
        do_karma(bot, user, reply, k)

    return

