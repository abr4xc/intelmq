# -*- coding: utf-8 -*-

import requests

from intelmq.lib.bot import CollectorBot
from intelmq.lib.message import Report
from intelmq.lib.utils import decode


class HTTPStreamCollectorBot(CollectorBot):

    def process(self):
        try:
            req = requests.get(self.parameters.url, stream=True)
        except requests.exceptions.ConnectionError:
            raise ValueError('Connection Failed.')
        else:
            for line in req.iter_lines():
                if self.parameters.strip_lines:
                    line = line.strip()

                if not line:
                    # filter out keep-alive new lines and empty lines
                    continue

                report = Report()
                report.add("raw", decode(line))
                self.send_message(report)
            self.logger.info('Stream stopped.')
