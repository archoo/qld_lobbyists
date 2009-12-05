import urllib,re
import xml.etree.ElementTree as et
import BeautifulSoup as bs

rawfile = urllib.urlopen('http://www.premiers.qld.gov.au/community-issues/open-transparent-gov/lobbyists-register/the-register.aspx')
rawdata = rawfile.read()
for a in re.findall('href="(assets/.*.pdf)"',rawdata):
  urllib.urlretrieve('http://www.premiers.qld.gov.au/community-issues/open-transparent-gov/lobbyists-register/'+a,a)
  print a,'downloaded..'
