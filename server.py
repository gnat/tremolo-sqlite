import asyncio, time, sqlite3, json
from tremolo import Tremolo

con = sqlite3.connect("test.sqlite")
con.cursor().execute(open("install.sql").read())
html = open("index.html").read()

app = Tremolo()

@app.route('/')
async def hello_world(**server):
	cur = con.cursor()
	cur.execute("INSERT INTO clicks(time) VALUES (unixepoch())")
	con.commit()
	res = cur.execute("SELECT * FROM clicks")
	out = html.replace('__DATA__', json.dumps(res.fetchall())).replace("],","],\n")
	return out

if __name__ == '__main__':
	app.run('0.0.0.0', 8080, worker_num=1, reload=True, debug=True)
