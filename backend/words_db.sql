CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    difficulty TEXT NOT NULL
);

INSERT INTO words (word, difficulty) VALUES ('cat', 'easy');
INSERT INTO words (word, difficulty) VALUES ('bat', 'easy');
INSERT INTO words (word, difficulty) VALUES ('ball', 'easy');
INSERT INTO words (word, difficulty) VALUES ('Banana', 'easy');
INSERT INTO words (word, difficulty) VALUES ('Apple', 'easy');
INSERT INTO words (word, difficulty) VALUES ('Orange', 'easy');

INSERT INTO words (word, difficulty) VALUES ('firetruck', 'medium');
INSERT INTO words (word, difficulty) VALUES ('planet', 'medium');
INSERT INTO words (word, difficulty) VALUES ('camera', 'medium');

INSERT INTO words (word, difficulty) VALUES ('architecture', 'hard');
INSERT INTO words (word, difficulty) VALUES ('exemplary', 'hard');
INSERT INTO words (word, difficulty) VALUES ('hypothesis', 'hard');