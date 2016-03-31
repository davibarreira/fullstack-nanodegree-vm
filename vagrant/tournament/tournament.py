#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
# db = connect()
# c  = db.cursor()
# c.execute(query,options)
# db.commit()
# db.close()

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    query = "delete from matches;"
    db = connect()
    c  = db.cursor()
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    query = "delete from players;"
    db = connect()
    c  = db.cursor()
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    query = "select count(*) as num from players;"
    db = connect()
    c  = db.cursor()
    c.execute(query)
    num = c.fetchall()[0][0]
    db.close()
    #print(num)
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c  = db.cursor()
    c.execute("insert into players (name) values (%s)",(name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    #query = "select id, name, wins, wins as matches from players where wins = (select max(wins) as mp from players);"
    query  = """
    select m.id, m.name,w.wins, m.match from (select id, name, count(idm) as match from players left join matches on (id = winner or id = loser) group by id) as m, (select id, count(idm) as wins from players left join matches on (id = winner) group by id) as w where w.id = m.id;
    """
    db = connect()
    c  = db.cursor()
    c.execute(query)
    standing = c.fetchall()
    db.close()
    #print(standing)
    return standing


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c  = db.cursor()
    #c.execute("update players set wins = 1 where id=%s",
    #        (winner,))
    c.execute("insert into matches (winner,loser) values (%s,%s);",
            (winner,loser))
    db.commit()
    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    query  = """
    drop view if exists pairings;
    create view pairings as select m.id, m.name,w.wins, m.match from (select id, name, count(idm) as match from players left join matches on (id = winner or id = loser) group by id) as m, (select id, count(idm) as wins from players left join matches on (id = winner) group by id) as w where w.id = m.id;
    """
    db = connect()
    c  = db.cursor()
    c.execute(query)
    db.commit()
    db.close()


    query = """
    select * from pairings order by wins;
    """
    db = connect()
    c  = db.cursor()
    c.execute(query)
    list = c.fetchall()
    pairs = []
    for i in range(0,len(list),2):
        pairs.append((list[i][0],list[i][1],list[i+1][0],list[i+1][1]))
    db.close()
    return pairs



if __name__ == "__main__":

    registerPlayer('Will')
    registerPlayer('Gill')
    registerPlayer('Billy')
    registerPlayer('Nilly')
    playerStandings()
    swissPairings()

    reportMatch(1,2)
    reportMatch(3,4)
    playerStandings()
    swissPairings()



