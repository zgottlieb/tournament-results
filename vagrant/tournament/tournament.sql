-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (id serial primary key, name text);

CREATE TABLE tournaments (id serial primary key);

CREATE TABLE player_registration (player_id int references players(id),
								  tournament_id int references tournaments(id));

CREATE TABLE matches (player1 int references players(id),
					  player2 int references players(id),
					  winner int,
					  tournament_id int references tournaments(id));

CREATE TABLE standings (player_id int references players(id),
						wins int,
						draws int,
						losses int,
						tournament_id int references tournaments(id));
