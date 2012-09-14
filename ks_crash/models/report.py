import os
import json
import redis
import rbase

class Report(rbase.Base):

    def __init__(self, crash_id, report_dict={}):
        self.crash_id = crash_id
        self.timestamp = report_dict.get('timestamp', None)
        self.content = json.dumps(report_dict)
        super(Report, self).__init__(crash_id, crash_id)

    def update(self):
        super(Report, self).update()
        self.content = json.loads(self.content)
