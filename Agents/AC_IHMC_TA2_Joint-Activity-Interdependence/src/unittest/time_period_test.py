import unittest
import json

from ..utils.time_period import TimePeriod, does_overlap, get_overlap_union, contains_overlapping_set, \
    get_non_overlapping_set, get_non_overlap_union, get_uniquely_non_overlapping_set


class TimePeriodTest(unittest.TestCase):

    def test_serialization(self):
        test_cases = [
            (TimePeriod(), '{"start": 0, "end": -1}'),
            (TimePeriod(start=10), '{"start": 10, "end": -1}'),
            (TimePeriod(end=10), '{"start": 0, "end": 10}'),
            (TimePeriod(start=10, end=-1), '{"start": 10, "end": -1}'),
            (TimePeriod(start=10, end=15), '{"start": 10, "end": 15}'),
            (TimePeriod(start=10.2837, end=10.3944), '{"start": 10.2837, "end": 10.3944}'),
        ]

        for time_period, expected_json in test_cases:
            self.assertEqual(
                json.dumps(time_period.dict()),
                expected_json
            )

    def test_checkUnion(self):
        time_period1 = TimePeriod(3, 6)
        self.assertEqual(3, time_period1.duration)

        time_period2 = TimePeriod(5, 10)
        self.assertEqual(5, time_period2.duration)

        msg = "does_overlap " + str(time_period1) + " and " + str(time_period2)
        self.assertTrue(does_overlap(time_period1, time_period2), msg)
        
        msg = "union " + str(time_period1) + " and " + str(time_period2)
        union_period = get_overlap_union(time_period1, time_period2)
        self.assertEqual(7, union_period.duration, msg)

    def test_checkSets(self):
        time_period1 = TimePeriod(3, 6)
        time_period2 = TimePeriod(5, 10)
        time_period3 = TimePeriod(12, 14)
        msg = "duration " + str(time_period3)
        self.assertEqual(2, time_period3.duration, msg)

        time_period_set1 = [time_period3, time_period1, time_period2]
        time_period_set1.sort(key=lambda x: (x.start, x.end))
        msg = "contains-overlapping-set " + str(time_period_set1)
        self.assertTrue(contains_overlapping_set(time_period_set1), msg)

        not_overlapping_set = get_non_overlapping_set(time_period_set1)
        msg = "contains-overlapping-set " + str(not_overlapping_set)
        self.assertFalse(contains_overlapping_set(not_overlapping_set), msg)

    def test_checkFullContainmentInUnion(self):
        tp1 = TimePeriod(64412, 64412)
        tp2 = TimePeriod(45593, 64416)
        msg = "does-overlap " + str(tp1) + " and " + str(tp2)
        self.assertTrue(does_overlap(tp1, tp2), msg)

        tp_set = [tp1, tp2]
        msg = "contains-overlapping-set " + str(tp_set)
        self.assertTrue(contains_overlapping_set(tp_set), msg)

        not_overlapping_set = get_non_overlapping_set(tp_set)
        union_period = get_overlap_union(tp1, tp2)
        msg = "union duration " + str(union_period)
        self.assertEqual(18823, union_period.duration, msg)

    def test_checkDurationForIncompleteTasks(self):
        tp0 = TimePeriod(64412, -1)
        msg = "duration for " + str(tp0)
        self.assertIsNone(tp0.duration, msg)

        tp0.end = 70000
        msg = "duration for " + str(tp0)
        self.assertEqual(tp0.duration, 5588, msg)

    def test_checkBugs(self):
        tp01 = TimePeriod(54292, 66147)
        tp02 = TimePeriod(54292, 54292)
        tp03 = TimePeriod(54292, 66147)
        tp04 = TimePeriod(54292, 54292)
        msg = "does-overlap " + str(tp02) + " and " + str(tp04)
        self.assertTrue(does_overlap(tp02, tp04), msg)

        tp_set = [tp02, tp04]
        msg = "contains-overlapping-set " + str(tp_set)
        self.assertTrue(contains_overlapping_set(tp_set), msg)

        msg = "non-overlapping-set " + str(tp_set)
        not_overlapping_set = get_non_overlapping_set(tp_set)
        self.assertEqual([tp02], not_overlapping_set, msg)

        msg = "does-overlap " + str(tp02) + " and " + str(tp03)
        self.assertTrue(does_overlap(tp02, tp03), msg)
        
        msg = "contains-overlapping-set " + str(tp_set)
        tp_set = [tp02, tp03]        
        self.assertTrue(contains_overlapping_set(tp_set), msg)
        
        msg = "non-overlapping-set " + str(tp_set)
        not_overlapping_set = get_non_overlapping_set(tp_set)
        self.assertEqual([tp01], not_overlapping_set, msg)

        msg = "contains-overlapping-set " + str(tp_set)
        tp_set = [tp01, tp02, tp03, tp04]
        self.assertTrue(contains_overlapping_set(tp_set), msg)
        
        msg = "non-overlapping-set " + str(tp_set)
        not_overlapping_set = get_non_overlapping_set(tp_set)
        self.assertEqual([tp01], not_overlapping_set, msg)

    def test_checkNonOverlapping(self):
        tp01 = TimePeriod(1000, 5000)
        tp02 = TimePeriod(4000, 7000)
        tp03 = TimePeriod(6000, 7000)
        tp04 = TimePeriod(5000, 5000)
        self.assertTrue(does_overlap(tp01, tp02))

        non_overlap = [TimePeriod(1000,4000), TimePeriod(5000,7000)]
        msg = "non-overlap-union " + str(tp01) + " and " + str(tp02)
        self.assertEqual(non_overlap, get_non_overlap_union(tp01, tp02), msg)

        msg = "does-overlap " + str(tp02) + " and " + str(tp03)
        self.assertTrue(does_overlap(tp02, tp03), msg)
        
        msg = "non-overlap-union " + str(tp02) + " and " + str(tp03)
        self.assertEqual([TimePeriod(4000,6000), TimePeriod(7000,7000)], get_non_overlap_union(tp02, tp03))
        
        msg = "does-overlap " + str(tp01) + " and " + str(tp03)
        self.assertFalse(does_overlap(tp01, tp03), msg)
        
        msg = "non-overlap-union " + str(tp01) + " and " + str(tp03)
        self.assertEqual([tp01,tp03], get_non_overlap_union(tp01, tp03), msg)

        msg = "does-overlap " + str(tp01) + " and " + str(tp04)
        self.assertTrue(does_overlap(tp01, tp04), msg)
        
        msg = "non-overlap-union " + str(tp01) + " and " + str(tp04)
        self.assertEqual([tp01, tp04], get_non_overlap_union(tp01, tp04), msg)

    def test_checkNonOverlappingSet(self):
        tp01 = TimePeriod(1000, 5000)
        tp02 = TimePeriod(4000, 7000)
        tp03 = TimePeriod(6000, 7000)

        tp_set = [tp01, tp02]
        msg = "contains-overlapping-set " + str(tp_set)
        self.assertTrue(contains_overlapping_set(tp_set), msg)

        #[from 1000 to 4000, from 5000 to 7000]        
        not_overlapping_set = get_uniquely_non_overlapping_set(tp_set)        
        msg = "non-overlapping-set " + str(tp_set)
        self.assertEqual([TimePeriod(1000,4000), TimePeriod(5000,7000)], not_overlapping_set, msg)

        tp_set = [tp01, tp02, tp03]
        msg = "contains-overlapping-set" + str(tp_set)
        self.assertTrue(contains_overlapping_set(tp_set), msg)
        
        msg = "non-overlapping-set " + str(tp_set)
        not_overlapping_set = get_uniquely_non_overlapping_set(tp_set)
        #[from 1000 to 4000, from 5000 to 6000, from 7000 to 7000]
        self.assertEqual([TimePeriod(1000,4000), TimePeriod(5000,6000), TimePeriod(7000,7000)], not_overlapping_set, msg)

        tp01 = TimePeriod(1000, 5000)
        tp02 = TimePeriod(3000, 4000)
        tp03 = TimePeriod(6000, 7000)
        tp_set = [tp01, tp02]
        msg = "contains-overlapping-set" + str(tp_set)
        self.assertTrue(contains_overlapping_set(tp_set), msg)
        
        msg = "non-overlapping-set " + str(tp_set)
        not_overlapping_set = get_uniquely_non_overlapping_set(tp_set)
        #[from 1000 to 3000, from 4000 to 5000]
        self.assertEqual([TimePeriod(1000,3000), TimePeriod(4000,5000)], not_overlapping_set, msg)

        tp_set = [tp01, tp02, tp03]
        msg = "contains-overlapping-set" + str(tp_set)
        self.assertTrue(contains_overlapping_set(tp_set), msg)
        
        msg = "non-overlapping-set " + str(tp_set)
        not_overlapping_set = get_uniquely_non_overlapping_set(tp_set)
        #[from 1000 to 3000, from 4000 to 5000, from 6000 to 7000]
        self.assertEqual([TimePeriod(1000,3000), TimePeriod(4000,5000), TimePeriod(6000,7000)], not_overlapping_set, msg)

    def test_checkNonOverlappingSetEqual(self):
        tp01 = TimePeriod(1000, 5000)
        tp02 = TimePeriod(1000, 5000)
        tp_set = [tp01, tp02]
        msg = "contains-overlapping-set" + str(tp_set)
        self.assertTrue(contains_overlapping_set(tp_set), msg)
        
        msg = "unique-non-overlapping-set" + str(tp_set)
        not_overlapping_set = get_uniquely_non_overlapping_set(tp_set)
        self.assertEqual([TimePeriod(1000,1000), TimePeriod(5000,5000)], not_overlapping_set, msg)

if __name__ == '__main__':
    unittest.main()
