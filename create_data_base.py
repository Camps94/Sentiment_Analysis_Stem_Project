

import json
import sqlite3
db = "twit_data.db"
conn = sqlite3.connect(db)
c = conn.cursor()
cmd = "CREATE TABLE BaseTweets (tweet_id TEXT , User TEXT, Created_at TEXT, content TEXT, Polarity TEXT)"
c.execute(cmd)
conn.commit()
conn.close()
