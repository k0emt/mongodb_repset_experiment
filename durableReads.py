# this code will do "safe" reads from a replica set
# we'll be kicking the master out from under the program to verify roll over
import datetime
from time import sleep
import pymongo

def read_one():
	need_to_read_one = True

	while(need_to_read_one):
		try:
			readDoc = collection.find_one()
			need_to_read_one = False
		except pymongo.errors.AutoReconnect, e:
			print 'WARNING AR:', e
			sleep(2)
		except pymongo.errors.ConnectionFailure, ecf:
			print 'WARNING CF:', ecf
			sleep(2)	

	return readDoc

print 'durable test'
db = pymongo.ReplicaSetConnection('localhost:27001,localhost:27002,localhost:27003', replicaSet="experiment").durable
collection = db.testdata

print 'Reading...'
for counter in range(30):
		document = read_one()
		print counter, document
		sleep(1)

db.close
print 'DONE'

