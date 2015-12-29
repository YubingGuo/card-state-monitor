# -*- coding: utf-8 -*-
"""
:copyright: NSN
:author: Pawel Kunat
:contact: pawel.kunat@nsn.com
"""
import time


class Timeout(object):

    _10000_YEARS = 60 * 60 * 24 * 365.25 * 10000

    def __init__(self, duration):
        """
        Creates a new timeout object with given duration that immediately starts counting time.
        If duration is None or infinite, resulting timeout is (near) infinite.
        If duration is non-positive, timeout is reached at once.
        """
        self.start_time = self._current_time()
        if duration is None or duration == float('inf'):
            self.end_time = self.start_time + Timeout._10000_YEARS  # should be enough and much safer than float('inf')
        else:
            self.end_time = self.start_time + duration

    def is_reached(self):
        """Returns True if timeout was exceeded, False otherwise."""
        return self._current_time() > self.end_time

    def is_not_reached(self):
        """Returns False if timeout was exceeded, True otherwise."""
        return not self.is_reached()

    def _current_time(self):
        return time.time()

    def time_left(self):
        """
        Returns time left in seconds until timeout is reached.
        :note: Returned value is a non-negative floating point number.
        """
        time_left = self.end_time - self._current_time()
        return max(0, time_left)

    def time_left_but_no_more_than(self, max_time):
        """
        Returns time left in seconds until timeout is reached or max_time, whichever is smaller.
        :note: Returned value is a non-negative floating point number.
        """
        nonnegative_max = max(max_time, 0)
        return min(self.time_left(), nonnegative_max)

    def time_elapsed(self):
        """
        Returns time elapsed in seconds since this timeout object was created.
        :note: Returned value is a non-negative floating point number.
        """
        return self._current_time() - self.start_time

    def sleep_until_reached(self):
        """Sleeps until timeout is reached."""
        time_to_sleep = self.time_left()
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    def sleep_until_reached_but_no_longer_than(self, max_time):
        """Sleeps until timeout is reached."""
        nonnegative_max = max(max_time, 0)
        time_to_sleep = min(self.time_left(), nonnegative_max)
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)
