#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testCreateTournament():
    newTournament = Tournament()
    print "1. Tournament can be created."
    return newTournament

def testDeleteMatches():
    newTournament.deleteMatches()
    print "2. Old matches can be deleted."


def testDeletePlayers():
    newTournament.deleteMatches()
    newTournament.deletePlayers()
    print "3. Player records can be deleted."


def testCountPlayers():
    newTournament.deleteMatches()
    newTournament.deletePlayers()
    c = newTournament.countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "4. After deleting, countPlayers() returns zero."


def testCreateAndRegisterPlayer():
    newTournament.deleteMatches()
    newTournament.deletePlayers()
    newPlayerId = createPlayer("Chandra Nalaar")
    newTournament.registerPlayer(newPlayerId)
    c = newTournament.countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "5. After creating and registering a player, countPlayers() returns 1."

def testRegisterCountDelete():
    newTournament.deleteMatches()
    newTournament.deletePlayers()
    newPlayers = ["Markov Chaney", "Joe Malik", "Mao Tsu-hsi", "Atlanta Hope"]

    for player in newPlayers:
        playerId = createPlayer(player)
        newTournament.registerPlayer(playerId)

    c = newTournament.countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    newTournament.deletePlayers()
    c = newTournament.countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "6. Players can be registered and deleted."

def testStandingsBeforeMatches():
    newTournament.deleteMatches()
    newTournament.deletePlayers()
    newPlayers = ["Melpomene Murray", "Randy Schwartz"]
    for player in newPlayers:
        playerId = createPlayer(player)
        newTournament.registerPlayer(playerId)
    standings = newTournament.playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 7:
        raise ValueError("Each playerStandings row should have seven columns.")
        
    [(id1, name1, wins1, draws2, losses1, matches1, tournament1),
     (id2, name2, wins2, draws2, losses2, matches2, tournament2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")

    if tournament1 != newTournament.id or tournament2 != newTournament.id:
        raise ValueError(
            "Newly created standings should match the given tournament id.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "7. Newly registered players appear in the standings with no matches."


def testReportMatches():
    newTournament.deleteMatches()
    newTournament.deletePlayers()
    newPlayers = ["Bruno Walton", "Boots O'Neal", "Cathy Burton", "Diane Grant"]
    for player in newPlayers:
        playerId = createPlayer(player)
        newTournament.registerPlayer(playerId)
    standings = newTournament.playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    newTournament.reportMatch(id1, id2, id1) # record match as a win for id1
    newTournament.reportMatch(id3, id4, None) # record match as a draw
    standings = newTournament.playerStandings()
    for (i, n, w, d, l, m, t) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1,) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2,) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
        elif i in (id3, id4) and d != 1:
            raise ValueError("Player whose match resulted in a draw should have one draw recorded.")
    print "8. After a match, players have updated standings."


def testPairings():
    newTournament.deleteMatches()
    newTournament.deletePlayers()
    newPlayers = ["Twilight Sparkle", "Fluttershy", "Applejack", "Pinkie Pie"]
    for player in newPlayers:
        playerId = createPlayer(player)
        newTournament.registerPlayer(playerId)
    standings = newTournament.playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    newTournament.reportMatch(id1, id2, id1)
    newTournament.reportMatch(id3, id4, id3)
    pairings = newTournament.swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "9. After one match, players with one win are paired."

if __name__ == '__main__':
    newTournament = testCreateTournament()
    testDeleteMatches()
    testDeletePlayers()
    testCountPlayers()
    testCreateAndRegisterPlayer()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"


