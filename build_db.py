import sqlite3,csv

db = sqlite3.connect('qld_lobbyists.db')

db.execute('CREATE TABLE entities(name,trading,abn)')
db.execute('CREATE TABLE owners(abn,name)')
db.execute('CREATE TABLE persons(abn,name,position)')
db.execute('CREATE TABLE curr_clients(abn,name,paid,success)')
db.execute('CREATE TABLE prev_clients(abn,name)')

for t in ['entities','owners','persons','curr_clients','prev_clients']:
  infile = csv.reader(open('data/'+t+'.csv'))
  for r in infile:
    print r
    sql = 'insert into '+t+' values ("'
    sql+= '","'.join(r)
    sql+= '")'
    db.execute(sql)
  db.commit()
