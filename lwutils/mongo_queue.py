from pymongo import MongoClient, DESCENDING
from time import time
from base64 import b64decode, b64encode
from bson.objectid import ObjectId


class MongoQueue(object):

    def __init__(self, config):
        self.config = config
        self.client = MongoClient(self.config['MONGODB_INSTANCE'], connect=False)
        self.db = self.client[self.config['MONGODB_QUEUE_DB']]

    def get(self, queue):
        """
            returns next (msg_id msg from given queue and marks it as in processing
        """
        result = {}
        m = self.db[queue].find_one_and_update({'inProg': False, 'done': False}, {'$set': {'inProg': True, 't': time()}}, sort=[('_id', DESCENDING)])
        if m is not None:
            result['id'] = str(m['_id'])
            result['msg'] = b64decode(m['msg'])
        return result

    def add(self, queue, msg):
        """
            adds given message to given queue
        """
        self.db[queue].insert_one({'inProg': False, 'done': False, 'msg': b64encode(msg)})

    def ping(self, queue, msg_id):
        """
            extends processing ttl
        """
        self.db[queue].update_one({'_id': ObjectId(msg_id)}, {'$set': {'t': time()}})

    def ack(self, queue, msg_id):
        """
            marks msgs as processed
        """
        self.db[queue].update_one({'_id': ObjectId(msg_id)}, {'$set': {'inProg': False, 'done': True}, '$unset': {'t': 0}})

    def delete(self, queue, msg_id):
        """
            deletes msg from queue
        """
        self.db[queue].delete_one({'_id': ObjectId(msg_id)})

    def gc(self, queue, delete=False):
        """
            reactivates processed messages once they are past proccesing max time
            and if delete is True removes all processed messages from queue
        """
        if delete:
            self.db[queue].delete_many({'done': True})
        processing_expiry = time() - self.config['MONGO_QUEUE_MSG_EXPIRY_SEC']
        self.db[queue].update_many({'t': {'$lt': processing_expiry}, 'inProg': True, 'done': False}, {'$set': {'inProg': False}, '$unset': {'t': 0}})

    def drop(self, queue):
        """
            removes the queue and all it's content from mongodb
        """
        self.db.drop_collection(queue)
