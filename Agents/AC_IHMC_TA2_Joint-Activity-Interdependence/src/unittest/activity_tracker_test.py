import json
import unittest

from ..utils.activity_tracker import ActivityTracker, does_match, does_time_period_overlap, \
    get_activity_tracker_union, contains_overlapping_time_periods, get_non_overlapping_activity_tracker_set, \
    get_activity_tracker_non_overlap_union, get_uniquely_non_overlapping_activity_tracker_set
from ..utils.time_period import TimePeriod


class ActivityTrackerTest(unittest.TestCase):

    def test_serialization(self):
        test_cases = [
            (
                ActivityTracker('alice'),
                '{"participant_id": "alice", "confidence": 0.0, "time_period": {"start": 0, "end": -1}}'
            ),
            (
                ActivityTracker('alice', 0.5),
                '{"participant_id": "alice", "confidence": 0.5, "time_period": {"start": 0, "end": -1}}'
            ),
            (
                ActivityTracker('alice', 1.0),
                '{"participant_id": "alice", "confidence": 1.0, "time_period": {"start": 0, "end": -1}}'
            ),
            (
                ActivityTracker('alice', 1.0, TimePeriod()),
                '{"participant_id": "alice", "confidence": 1.0, "time_period": {"start": 0, "end": -1}}'
            ),
            (
                ActivityTracker('alice', 1.0, TimePeriod(10)),
                '{"participant_id": "alice", "confidence": 1.0, "time_period": {"start": 10, "end": -1}}'
            ),
            (
                ActivityTracker('alice', 1.0, TimePeriod(10, 15)),
                '{"participant_id": "alice", "confidence": 1.0, "time_period": {"start": 10, "end": 15}}'
            ),
        ]

        for activity_tracker, expected_json in test_cases:
            self.assertEqual(
                json.dumps(activity_tracker.dict()),
                expected_json
            )

    def test_doesMatch(self):
        time_period1 = TimePeriod(20000, 28000)
        time_period2 = TimePeriod(24000, -1)
        at1 = ActivityTracker('Bob', 1.0, time_period1)
        at2 = ActivityTracker('Larry', 0.0, time_period1)
        result = does_match(at1, at2)
        msg = "does " + str(at1) + " match " + str(at2)
        self.assertFalse(result, msg)

        at3 = ActivityTracker('Bob', 0.0, time_period1)
        result = does_match(at1, at3)
        msg = "does " + str(at1) + " match " + str(at3)
        self.assertFalse(result, msg)

        at4 = ActivityTracker('Larry', 1.0, time_period1)
        result = does_match(at1, at4)
        msg = "does " + str(at1) + " match " + str(at4)
        self.assertFalse(result, msg)

        at5 = ActivityTracker('Bob', 1.0, time_period1)
        result = does_match(at1, at5)
        msg = "does " + str(at1) + " match " + str(at5)
        self.assertTrue(result, msg)

        at6 = ActivityTracker('Bob', 1.0, time_period2)
        result = does_match(at1, at6)
        msg = "does " + str(at1) + " match " + str(at6)
        self.assertTrue(result, msg)

    def test_timePeriodOverlap(self):
        time_period1 = TimePeriod(20000, 28000)
        time_period2 = TimePeriod(20000, 28000)
        at1 = ActivityTracker('Bob', 1.0, time_period1)
        at2 = ActivityTracker('Bob', 1.0, time_period2)
        result = str(does_time_period_overlap(at1, at2))
        msg = "does " + str(time_period1) + " overlap " + str(time_period2)
        self.assertTrue(result, msg)

        time_period3 = TimePeriod(26000, 30000)
        at2 = ActivityTracker('Bob', 1.0, time_period3)
        result = does_time_period_overlap(at1, at2)
        msg = "does " + str(time_period1) + " overlap " + str(time_period3)
        self.assertTrue(result, msg)

        time_period4 = TimePeriod(29000, 30000)
        at2 = ActivityTracker('Bob', 1.0, time_period4)
        result = does_time_period_overlap(at1, at2)
        msg = "does " + str(time_period1) + " overlap " + str(time_period4)
        self.assertFalse(result, msg)

        time_period5 = TimePeriod(20000, 20000)
        at2 = ActivityTracker('Bob', 1.0, time_period5)
        result = does_time_period_overlap(at1, at2)
        msg = "does " + str(time_period1) + " overlap " + str(time_period5)
        self.assertTrue(result, msg);

        time_period6 = TimePeriod(28000, 28000)
        at2 = ActivityTracker('Bob', 1.0, time_period6)
        result = does_time_period_overlap(at1, at2)
        msg = "does " + str(time_period1) + " overlap " + str(time_period6)
        self.assertTrue(result, msg);

    def test_activityTrackerUnion(self):
        time_period1 = TimePeriod(20000, 24000)
        time_period2 = TimePeriod(22000, 26000)
        at1 = ActivityTracker('Bob', 1.0, time_period1)
        at2 = ActivityTracker('Bob', 1.0, time_period2)
        result = get_activity_tracker_union(at1, at2)
        msg = "union " + str(time_period1) + " and " + str(time_period2)
        self.assertEqual(result, ActivityTracker('Bob', 1.0, TimePeriod(20000, 26000)), msg);

    def test_containsOverlappingTimePeriods(self):
        time_period1 = TimePeriod(20000, 28000)
        time_period2 = TimePeriod(20000, 28000)
        at1 = ActivityTracker('Bob', 1.0, time_period1)
        at2 = ActivityTracker('Bob', 1.0, time_period2)
        at_set = [at1, at2]

        result = contains_overlapping_time_periods(at_set)
        msg = "contains_overlapping " + str(time_period1) + " and " + str(time_period2)
        self.assertTrue(result, msg)

        time_period3 = TimePeriod(26000, 30000)
        at2 = ActivityTracker('Bob', 1.0, time_period3)
        at_set = [at1, at2]
        result = contains_overlapping_time_periods(at_set)
        msg = "contains_overlapping " + str(time_period1) + " and " + str(time_period3)
        self.assertTrue(result, msg)

        time_period4 = TimePeriod(29000, 30000)
        at2 = ActivityTracker('Bob', 1.0, time_period4)
        at_set = [at1, at2]
        result = contains_overlapping_time_periods(at_set)
        msg = "contains_overlapping " + str(time_period1) + " and " + str(time_period4)
        self.assertFalse(result, msg)

        time_period5 = TimePeriod(20000, 20000)
        at2 = ActivityTracker('Bob', 1.0, time_period5)
        at_set = [at1, at2]
        result = contains_overlapping_time_periods(at_set)
        msg = "contains_overlapping " + str(time_period1) + " and " + str(time_period5)
        self.assertTrue(result, msg)

        time_period6 = TimePeriod(28000, 28000)
        at2 = ActivityTracker('Bob', 1.0, time_period6)
        at_set = [at1, at2]
        result = contains_overlapping_time_periods(at_set)
        msg = "contains_overlapping " + str(time_period1) + " and " + str(time_period6)
        self.assertTrue(result, msg)

    def test_nonOverlappingActivityTrackerSet(self):
        time_period1 = TimePeriod(20000, 28000)
        time_period2 = TimePeriod(20000, 28000)
        at1 = ActivityTracker('Bob', 1.0, time_period1)
        at2 = ActivityTracker('Bob', 1.0, time_period2)
        at_set = [at1, at2]
        result = get_non_overlapping_activity_tracker_set(at_set)
        msg = "non-overlapping " + str(time_period1) + " and " + str(time_period2)
        self.assertEqual(result,
                         [ActivityTracker('Bob', 1.0, TimePeriod(20000, 28000))],
                         msg)

        time_period3 = TimePeriod(26000, 30000)
        at2 = ActivityTracker('Bob', 1.0, time_period3)
        at_set = [at1, at2]
        result = get_non_overlapping_activity_tracker_set(at_set)
        msg = "non-overlapping " + str(time_period1) + " and " + str(time_period3)
        self.assertEqual(result,
                         [ActivityTracker('Bob', 1.0, TimePeriod(20000, 30000))],
                         msg)

        time_period4 = TimePeriod(29000, 30000)
        at2 = ActivityTracker('Bob', 1.0, time_period4)
        at_set = [at1, at2]
        result = get_non_overlapping_activity_tracker_set(at_set)
        msg = "non-overlapping " + str(time_period1) + " and " + str(time_period4)
        self.assertEqual(result,
                         [ActivityTracker('Bob', 1.0, TimePeriod(20000, 28000)),
                          ActivityTracker('Bob', 1.0, TimePeriod(29000, 30000))],
                         msg)

    def test_ongoingActivities(self):
        time_period1 = TimePeriod(20000, 28000)
        time_period2 = TimePeriod(24000, -1)
        at1 = ActivityTracker('Bob', 1.0, time_period1)
        at2 = ActivityTracker('Bob', 1.0, time_period2)
        result = does_time_period_overlap(at1, at2)
        # TODO: known failure, returns false, due to time_period bug... but we don't want to fix it yet
        msg = "overlap " + str(time_period1) + " and " + str(time_period2)
        self.assertTrue(result, msg)

        at_set = [at1, at2]
        result = get_non_overlapping_activity_tracker_set(at_set)
        msg = "non-overlap " + str(time_period1) + " and " + str(time_period2)
        # TODO: known failure, returns the original time periods -- should be two time periods correspoding to the non-overlap...
        self.assertEqual(result,
                         [ActivityTracker('Bob', 1.0, TimePeriod(20000, 24000)),
                          ActivityTracker('Bob', 1.0, TimePeriod(28000, -1))],
                         msg)

    def test_sameOngoingActivities(self):
        time_period1 = TimePeriod(24000, -1)
        time_period2 = TimePeriod(24000, -1)
        at1 = ActivityTracker('Bob', 1.0, time_period1)
        at2 = ActivityTracker('Bob', 1.0, time_period2)
        result = does_time_period_overlap(at1, at2)
        msg = "does " + str(time_period1) + " overlap " + str(time_period2)
        self.assertTrue(result, msg)

        at_set = [at1, at2]
        result = get_non_overlapping_activity_tracker_set(at_set)
        msg = "non-overlap " + str(time_period1) + " and " + str(time_period2)
        self.assertEqual(result, [at1], msg)

    def test_nonOverlapUnion(self):
        time_period1 = TimePeriod(20000, 24000)
        time_period2 = TimePeriod(22000, 26000)
        at1 = ActivityTracker('Bob', 1.0, time_period1)
        at2 = ActivityTracker('Bob', 1.0, time_period2)
        result = get_activity_tracker_non_overlap_union(at1, at2)
        msg = "merging " + str(time_period1) + " and " + str(time_period2)
        self.assertEqual(result,
                         [ActivityTracker('Bob', 1.0, TimePeriod(20000, 22000)),
                          ActivityTracker('Bob', 1.0, TimePeriod(24000, 26000))],
                         msg)

    def test_uniqueNonOverlapActivityTrackerSet(self):
        time_period1 = TimePeriod(20000, 28000)
        time_period2 = TimePeriod(20000, 28000)
        at1 = ActivityTracker('Bob', 1.0, time_period1)
        at2 = ActivityTracker('Bob', 1.0, time_period2)
        at_set = [at1, at2]
        result = get_uniquely_non_overlapping_activity_tracker_set(at_set)
        msg = "unique-non-overlap " + str(time_period1) + " and " + str(time_period2)
        # TODO: known failure, returns two endpoints of duration 0... but shouldn't it return an empty set?
        self.assertEqual(result, [], msg)

        time_period3 = TimePeriod(26000, 30000)
        at2 = ActivityTracker('Bob', 1.0, time_period3)
        at_set = [at1, at2]
        result = get_uniquely_non_overlapping_activity_tracker_set(at_set)
        msg = "unique-non-overlap " + str(time_period1) + " and " + str(time_period3)
        self.assertEqual(result,
                         [ActivityTracker('Bob', 1.0, TimePeriod(20000, 26000)),
                          ActivityTracker('Bob', 1.0, TimePeriod(28000, 30000))],
                         msg)

        time_period4 = TimePeriod(29000, 30000)
        at2 = ActivityTracker('Bob', 1.0, time_period4)
        at_set = [at1, at2]
        result = get_uniquely_non_overlapping_activity_tracker_set(at_set)
        msg = "unique-non-overlap " + str(time_period1) + " and " + str(time_period4)
        self.assertEqual(result, [at1, at2], msg)


if __name__ == '__main__':
    unittest.main()
