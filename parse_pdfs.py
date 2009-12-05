import re,os,csv

# setup outputs
out_e = csv.writer(open('data/entities.csv','w'),lineterminator='\n')
out_o = csv.writer(open('data/owners.csv','w'),lineterminator='\n')
out_p = csv.writer(open('data/persons.csv','w'),lineterminator='\n')
out_cc = csv.writer(open('data/curr_clients.csv','w'),lineterminator='\n')
out_pc = csv.writer(open('data/prev_clients.csv','w'),lineterminator='\n')

txt_files = [f for f in os.listdir('assets') if f[-3:]=='txt']
for f in txt_files:
  data = [r.strip('\n') for r in open('assets/'+f).readlines() if len(r.strip())>0]
  ptr,mode = 0,''

  while ptr<len(data):
    if data[ptr][0]=='\x0c': data[ptr]=data[ptr][1:]  # strip formfeed
    # decide what section of the file we are in and setup variables
    if re.match('BUSINESS ENTITY NAME',data[ptr]): mode,field = 'entity','name'
    elif re.match('TRADING NAME',data[ptr]): mode,field = 'entity','trading'
    elif re.match('A.B.N.',data[ptr]): mode,field = 'entity','abn'
    elif re.match('OWNER DETAILS',data[ptr]): mode,ptr,owners = 'owners',ptr+1,[]
    elif re.match('DETAILS OF ALL PERSONS OR EMPLOYEES',data[ptr]): mode,ptr,persons = 'persons',ptr+1,[]
    elif re.match('CURRENT THIRD PARTY CLIENT DETAILS',data[ptr]): mode,ptr,curr = 'curr_clients',ptr+3,[]
    elif re.match('PREVIOUS THIRD PARTY CLIENT DETAILS',data[ptr]): mode,ptr,prev = 'prev_clients',ptr+2,[]
    else: # we haven't hit a heading so actually do something
      t = data[ptr].strip()
      if mode=='entity' and field=='name':
        if t!='': entity = t
      if mode=='entity' and field=='trading':
        if t!='': trading = t
      if mode=='entity' and field=='abn':
        if t!='': abn = t.replace(' ','')
      if mode=='owners':
        if t!='': owners.append([abn,t])
      if mode=='persons':
        if t!='': 
          d = re.split('\s{2,}',t)
          if len(d)==1: d.append('NA')
          name,position=d
          persons.append([abn,name,position])
      if mode=='curr_clients':
        if t!='': 
          d = re.split('\s{2,}',t)
          if len(d)==3:
            name,paid,success = d
            curr.append([abn,name,paid,success])
          if len(d)==1 and t!='Nil':
            curr[-1][1]+=' '+t
          if len(d)==1 and t=='Nil':
            curr.append([abn,'Nil','',''])
      if mode=='prev_clients':
        if t!='': prev.append([abn,t])

    ptr += 1
  out_e.writerow([entity,trading,abn])
  out_o.writerows(owners)
  out_p.writerows(persons)
  out_cc.writerows(curr)
  out_pc.writerows(prev)
