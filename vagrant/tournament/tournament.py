#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def createTournament():
    """Adds a tournament to the tournament database.

    The database assigns a unique serial id number for the tournmanet.

    Takes no arguments.
    """

    conn = connect()
    cur = conn.cursor()

    cur.execute('''INSERT INTO tournaments DEFAULT VALUES
                   RETURNING id
                ''')

    tournament_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return tournament_id

def createPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()

    cur.execute("INSERT INTO players (name) VALUES (%s)", (name,))

    conn.commit()

    cur.execute("SELECT id FROM players ORDER BY id DESC LIMIT 1")

    player_id = int(cur.fetchone()[0])

    conn.commit()
    conn.close()

    return player_id

class Tournament():
    """ A class for a single tournament. On init, creates an entry
        in the tournaments table and stores the created id in the
        'id' class variable.

        Takes no arguments on init.
    """
    def __init__(self):
        self.id = createTournament()

    def deleteMatches(self):
        """Remove all the match records for this tournament from the database."""
        conn = connect()
        cur = conn.cursor()

        cur.execute("DELETE FROM matches WHERE tournament_id = (%s)", (self.id,))
        conn.commit()
        conn.close()

    def deletePlayers(self):
        """Remove all the player records for this tournament from the database."""
        conn = connect()
        cur = conn.cursor()

        cur.execute("DELETE FROM standings WHERE tournament_id = (%s)", (self.id,))
        cur.execute("DELETE FROM player_registration WHERE tournament_id = (%s)", (self.id,))

        conn.commit()
        conn.close()

    def countPlayers(self):
        """Returns the number of players currently registered for this tournament."""
        conn = connect()
        cur = conn.cursor()

        cur.execute("SELECT count(*) FROM player_registration WHERE tournament_id = (%s)", (self.id,))
        playerCount = cur.fetchall()[0][0]

        conn.close()
        return playerCount

    def registerPlayer(self, player_id):
        """Adds the given player to this tournament in the player_registration table."""

        conn = connect()
        cur = conn.cursor()

        cur.execute("INSERT INTO player_registration VALUES (%s, %s)", (player_id, self.id));

        cur.execute("INSERT INTO standings VALUES (%s, %s, %s, %s, %s)", (player_id, 0, 0, 0, self.id))

        conn.commit()
        conn.close()

    def playerStandings(self):
        """Returns a list of the players and their win records sorted by wins, for a given tournnament.

        The first entry in the list should be the player in first place, or a player
        tied for first place if there is currently a tie.

        Returns:
          A list of tuples, each of which contains (id, name, wins, matches):
            id: the player's unique id (assigned by the database)
            name: the player's full name (as registered)
            wins: the number of matches the player has won
            matches: the number of matches the player has played
        """
        conn = connect()
        cur = conn.cursor()

        cur.execute('''SELECT players.id,
                              players.name,
                              standings.wins,
                              standings.draws,
                              standings.losses,
                              standings.wins + standings.losses + standings.draws as matches_played,
                              standings.tournament_id
                       FROM players
                       LEFT JOIN standings ON players.id = standings.player_id
                       INNER JOIN player_registration ON players.id = player_registration.player_id
                       WHERE players.id = standings.player_id
                       AND standings.tournament_id = player_registration.tournament_id
                       AND standings.tournament_id = (%s)
                       ORDER BY standings.wins''', (self.id,))

        player_standings = cur.fetchall()

        conn.close()
        return player_standings

    def reportMatch(self, player1, player2, winner):
        """Records the outcome of a single match between two players.

        Args:
          player1, player2: the id numbers of the two players in the match
          winner:  the id number of the player who won; if None, match will be recorded as draw
        """
        conn = connect()
        cur = conn.cursor()

        cur.execute("INSERT INTO matches VALUES (%s, %s, %s, %s)", (player1, player2, winner, self.id))

        if winner is None:
            cur.execute("UPDATE standings SET draws = draws + 1 WHERE player_id IN (%s, %s)", (player1, player2))
        else:
            loser = player1 if winner == player2 else player2
            cur.execute("UPDATE standings SET wins = wins + 1 WHERE player_id = (%s)", (winner,))
            cur.execute("UPDATE standings SET losses = losses + 1 WHERE player_id = (%s)", (loser,))

        conn.commit()
        conn.close()
     
    def swissPairings(self):
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

        conn = connect()
        cur = conn.cursor()

        cur.execute('''SELECT player1.id AS id1, 
                              player1.name AS name1, 
                              player2.id AS id2, 
                              player2.name AS name2
                        FROM players AS player1
                        JOIN players AS player2 ON player1.id < player2.id
                        JOIN player_registration AS pr ON pr.player_id = player1.id
                        WHERE (SELECT wins FROM standings WHERE player_id = player1.id AND tournament_id = (%s)) =
                              (SELECT wins FROM standings WHERE player_id = player2.id AND tournament_id = (%s))
                        AND pr.tournament_id = (%s)
                        ''', (self.id,self.id,self.id))

        pairings = cur.fetchall()
        conn.close()

        return pairings
