import csv
import sqlite3

QUERY_GAME_TAGS_FROM_CURATION = """
WITH tag_aliases AS (
  SELECT tagId, name FROM tag_alias
  GROUP BY tagId
)
SELECT tag_aliases.name
FROM game
INNER JOIN game_tags_tag on game_tags_tag.gameId = game.id
INNER JOIN tag_aliases on tag_aliases.tagId = game_tags_tag.tagId
WHERE game.id = '{}'
"""

EXTREME_TAGS = ["Adult", "Sexual Content", "LEGACY-EXTREME"] #Nope not listing all in the repo

def sql_escape(phrase):
    return phrase.replace("'", "\'").replace("\\", "\\\\")
   
def list_games():
    tag_sugg_list = []
    missing_tags = []

    print('Getting tag suggestion list...')
    with open('tag_suggestions.csv', newline='', encoding="utf-8") as csvfile:
        cvsreader = csv.reader(csvfile)
        for row in cvsreader:
            tag_sugg_list.append(row)

    con = sqlite3.connect('flashpoint.sqlite')
    cur = con.cursor()

    # Game ids and names from db
    cur.execute("SELECT id, title, alternateTitles, tagsStr, dateAdded FROM game")
    curation_list = cur.fetchall()

    # Cursor returns arrays instead of tuples
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()

    print('Checking curations...')
    with open('../db/init.sql', 'w', encoding="utf-8") as sqlfile:
        sqlfile.write("""
        CREATE SCHEMA IF NOT EXISTS fpgames CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
        USE fpgames;
        CREATE TABLE IF NOT EXISTS game (
            id	CHAR(62),
            title	VARCHAR(255),
            tagsStr	VARCHAR(500),
            dateAdded	DATE,
            suggestedTag	VARCHAR(40),
            isExtreme	INTEGER,
            vote_yes	INTEGER,
            vote_no	INTEGER
        );
        INSERT INTO game (`id`, `title`, `tagsStr`, `dateAdded`, `suggestedTag`, `isExtreme`, `vote_yes`, `vote_no`) VALUES
        """)
        first_entry = True
        for game in curation_list:
            # game[0] = id, game[1] = title, game[2] = alt_title, game[3] = tagsStr, game[4] = dateAdded
            for row in tag_sugg_list:
                for tag_suggestion in filter(None, row[1:]):
                    tag_suggestion = tag_suggestion.lower()
                    if (tag_suggestion in game[1].lower() or tag_suggestion in game[2].lower()):
                        cur.execute(QUERY_GAME_TAGS_FROM_CURATION.format(game[0]))
                        are_there_tags = cur.fetchall()
                        #We want to know if this game has any of the tags from row[0]
                        if not row[0] in are_there_tags:
                            print(f"{game[1]} has no tag {row[0]}")
                            if not first_entry:
                                sqlfile.write(",\n");
                            is_extreme = int(row[0] in EXTREME_TAGS or game[3] in ";".join(EXTREME_TAGS))
                            sqlfile.write(sql_escape(f"('{game[0]}', '{game[1]}', '{game[3]}', '{game[4]}', '{row[0]}', {is_extreme}, 0, 0)"))
                            first_entry = False
        sqlfile.write(";\nCOMMIT;")

list_games()