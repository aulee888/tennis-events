/* 
 * Recommend storing all timestamp data as YYYY-MM-DD HH:MI:SS
 */

CREATE TABLE player (
    id INTEGER PRIMARY KEY
    , discord_id INTEGER
    , username TEXT
    , nickname TEXT  -- Recommend enforcing as IRL name
    , created_timestamp TEXT  -- When the player joins the server
    , verified_by INTEGER  -- Mod that verifies incoming player
    , verified_timestamp TEXT
)
;


CREATE TABLE events (
    id INTEGER PRIMARY KEY
    , event_timestamp TEXT  -- When the event is/was
    , event_location TEXT
    , capacity INTEGER
    , created_by INTEGER
    , created_timestamp TEXT  -- When the event was entered into the db
    , comment TEXT  -- To be used for making comments regarding event, can be NULL
)
;


CREATE TABLE registration (
    id INTEGER PRIMARY KEY
    , event_id INTEGER
    , player1_id INTEGER
    , player2_id INTEGER  -- Designates doubles partner, otherwise NULL if singles event
    , status INTEGER  -- Boolean for if registration went through and player(s) participated in event
    , created_by INTEGER  -- Not necessarily always the same as player1, could be registered by another person/mod/bot
    , created_timestamp TEXT
)
;


CREATE TABLE confirmations (
    id INTEGER PRIMARY KEY
    , event_id INTEGER
    , player_id INTEGER
    , status INTEGER  -- Boolean
    , sent_timestamp TEXT  -- When the confirmation was created and sent to player
    , confirmation_timestamp TEXT  -- When the status was updated
)
;