# this code will do "safe" writes to a replica set
# we'll be kicking the master out from under the program to verify roll over

import datetime
from time import sleep
import pymongo
import bson

def insert_document():
	need_to_insert_document = True 
	my_ID = bson.ObjectId()
	testDocument = {"_id": my_ID, "ts": datetime.datetime.now(), "data": "something or other" }

	while(need_to_insert_document):
		try:
			collection.insert(testDocument, safe=True)
			need_to_insert_document = False
			
		except pymongo.errors.AutoReconnect, e:
			print 'W WARNING AR:', e
			sleep(1)

		except pymongo.errors.ConnectionFailure, ecf:
			print 'W WARNING CF:', ecf
			sleep(1)

		except pymongo.errors.DuplicateKeyError, dk:
			# It worked the first time
			print 'W WARNING DK:', dk
			need_to_insert_document = False
			pass


print 'durable test'
db = pymongo.ReplicaSetConnection('localhost:27001,localhost:27002,localhost:27003', replicaSet="experiment").durable
collection = db.testdata

for counter in range(0,20):
	insert_document()
	print counter,
	sleep(1)
	
db.close
print 'DONE'
