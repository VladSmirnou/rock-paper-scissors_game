import psycopg2

from .constants import DSN

# I've never worked with psycopg2 directly, and I don't know
# if I'll need to use it like this in the future. Because of that
# this is the most basic configuration that was made just to 'make it work'.
# I have no idea how to create, manage and move those connectors and cursors
# properly, and, what's the most important, idk if need to know :P

conn = psycopg2.connect(dsn=DSN)

cur = conn.cursor()

cur.execute("""create table if not exists game_data (
    game_id uuid primary key,
    games_won smallint not null,
    games_lost smallint not null,
    max_rounds_per_game smallint not null
);
""")

cur.execute("""create table if not exists round_data (
    game_id uuid unique not null,
    round smallint not null,
    rounds_lost smallint not null,
    total_draws smallint not null,
    rounds_won smallint not null,
    user_choice varchar(1) not null,
    computer_choice varchar(1) not null,
    foreign key (game_id) references game_data on delete cascade,
    primary key (game_id, round)
);
""")

conn.commit()
