# Copyright (C) 2025 Francisco Bartolo (See LICENCE)

"""rrss"""

from urllib.error import HTTPError
from flask import current_app
import fastfeedparser
import re
from core.dispatcher import Dispatcher # pylint: disable=import-error
from . import rrss_bp


class DispatcherRrss(Dispatcher):
    """Read RSS."""

    def __init__(self, request, route):
        super().__init__(request, route)
        self.schema_data['template_route'] = rrss_bp.template_route

    def get_rss(self, url_rss_name='') -> bool:
        """Get RSS."""

        try:
            url_rss = self.schema_data['rrss_urls'].get(url_rss_name, self.schema_data['rrss_default'])
            rrss = fastfeedparser.parse(url_rss)

        except HTTPError as e:
            if current_app.debug:
                raise e

            self.schema_data['rrss_feed_error'] = str(e.reason)
            return False

        except ImportError as e:
            if current_app.debug:
                raise e

            self.schema_data['rrss_feed_error'] = str(e)
            return False

        except Exception as e: # pylint: disable=broad-except
            if current_app.debug:
                raise e

            self.schema_data['rrss_feed_error'] = str(e)
            return False

        if not rrss.feed and not rrss.entries:
            self.schema_data['rrss_feed_error'] = "No feed or entries found"
            return False

        if url_rss_name == 'yups':
            url = rrss.entries[0]['id']
            start = re.search(r'/(\d+)$', url).group(1)
            self.schema_data['rrss_yups_start'] = start
            self.schema_data['rrss_yups_num'] = 50

        self.schema_data['rrss_feed_url'] = url_rss
        self.schema_data['rrss_feed_feed'] = rrss.feed or {}
        self.schema_data['rrss_feed_entries'] = rrss.entries  or {}

        return True
