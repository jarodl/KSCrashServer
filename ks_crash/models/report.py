import os
import json
import redis

class BaseItem(object):
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost')
    _redis = redis.Redis(host=redis_url, port=6379)

    def __init__(self, ident, object_id=None):
        self.name = self.__class__.__name__
        self.ident = ident
        self.object_id = object_id
        self.redis_key = self.make_key(self.name, self.ident)

    @classmethod
    def all(cls):
        identifiers = cls._redis.smembers(cls.__name__)
        return [cls.get(ident) for ident in identifiers]

    @classmethod
    def clear(cls):
        all_items = cls.all()
        for item in all_items:
            item.delete()

    @classmethod
    def get(cls, ident):
        item = cls(ident)
        if cls.exists(item):
            item.update()
            return item
        else:
            return None

    @classmethod
    def exists(cls, item):
        return cls._redis.get(item.redis_key) is not None

    def make_key(self, *args):
        """
        Creates a redis key from a list

        Format is:
        ClassName:identifier:attribute
        """
        return str.join(':', args)

    def update(self):
        """
        Update all of the attributes from redis.
        """
        unsafe_attrs = set(('redis_key', 'ident', 'name'))
        for attr, value in self.__dict__.iteritems():
            if attr not in unsafe_attrs:
                key = self.make_key(self.redis_key, attr)
                self.__dict__[attr] = BaseItem._redis.get(key)

    def save(self):
        """
        Save all of the attributes to redis
        """
        BaseItem._redis.sadd(self.name, self.ident)
        BaseItem._redis.set(self.redis_key, self.object_id)
        for attr, value in self.__dict__.iteritems():
            key = self.make_key(self.redis_key, attr)
            BaseItem._redis.set(key, value)

    def delete(self):
        """
        Delete this object from redis
        """
        BaseItem._redis.delete(self.redis_key)
        BaseItem._redis.srem(self.name, self.ident)
        for attr in self.__dict__.keys():
            key = self.make_key(self.redis_key, attr)
            BaseItem._redis.delete(key)

class Report(BaseItem):

    def __init__(self, crash_id, report_dict={}):
        self.crash_id = crash_id
        self.timestamp = report_dict.get('timestamp', None)
        self.content = json.dumps(report_dict)
        super(Report, self).__init__(crash_id, crash_id)

    def update(self):
        super(Report, self).update()
        self.content = json.loads(self.content)
