from src.utils.activity_tracker import ActivityTracker, does_match, does_time_period_overlap, \
    get_activity_tracker_union, contains_overlapping_time_periods, get_non_overlapping_activity_tracker_set, \
    get_activity_tracker_non_overlap_union, get_uniquely_non_overlapping_activity_tracker_set
from src.utils.time_period import TimePeriod

who1 = 'Bob'
time_period1 = TimePeriod(20000, 28000)
at1 = ActivityTracker(who1, 1.0, time_period1)
print('1: ' + at1.to_string())

print()
who2 = 'Larry'
time_period2 = TimePeriod(24000, -1)
at2 = ActivityTracker(who2, 0.5, time_period2)
print('2: ' + at2.to_string())

print()
print("TEST does_match")
at1 = ActivityTracker('Bob', 1.0, time_period1)
at2 = ActivityTracker('Larry', 0.0, time_period1)
print("does " + str(at1) + " match " + str(at2) + " = " + str(does_match(at1, at2)))
at3 = ActivityTracker('Bob', 0.0, time_period1)
print("does " + str(at1) + " match " + str(at3) + " = " + str(does_match(at1, at3)))
at4 = ActivityTracker('Larry', 1.0, time_period1)
print("does " + str(at1) + " match " + str(at4) + " = " + str(does_match(at1, at4)))
at5 = ActivityTracker('Bob', 1.0, time_period1)
print("does " + str(at1) + " match " + str(at5) + " = " + str(does_match(at1, at5)))

print()
print("TEST equals")
at1 = ActivityTracker('Bob', 1.0, time_period1)
at2 = ActivityTracker('Larry', 0.0, time_period1)
at3 = ActivityTracker('Bob', 0.0, time_period1)
at4 = ActivityTracker('Bob', 1.0, time_period2)
at5 = ActivityTracker('Bob', 1.0, time_period1)
print("does " + str(at1) + " == " + str(at1) + " = " + str(at1 == at1))
print("does " + str(at1) + " == " + str(at2) + " = " + str(at1 == at2))
print("does " + str(at1) + " == " + str(at3) + " = " + str(at1 == at3))
print("does " + str(at1) + " == " + str(at4) + " = " + str(at1 == at4))
print("does " + str(at1) + " == " + str(at5) + " = " + str(at1 == at5))

print()
print("TEST does_time_period_overlap")
time_period1 = TimePeriod(20000, 28000)
time_period2 = TimePeriod(20000, 28000)
at1 = ActivityTracker('Bob', 1.0, time_period1)
at2 = ActivityTracker('Bob', 1.0, time_period2)
print("does " + str(time_period1) + " overlap " + str(time_period2) + " = " + str(does_time_period_overlap(at1, at2)))
time_period3 = TimePeriod(26000, 30000)
at2 = ActivityTracker('Bob', 1.0, time_period3)
print("does " + str(time_period1) + " overlap " + str(time_period3) + " = " + str(does_time_period_overlap(at1, at2)))
time_period4 = TimePeriod(29000, 30000)
at2 = ActivityTracker('Bob', 1.0, time_period4)
print("does " + str(time_period1) + " overlap " + str(time_period4) + " = " + str(does_time_period_overlap(at1, at2)))
time_period5 = TimePeriod(20000, 20000)
at2 = ActivityTracker('Bob', 1.0, time_period5)
print("does " + str(time_period1) + " overlap " + str(time_period5) + " = " + str(does_time_period_overlap(at1, at2)))
time_period6 = TimePeriod(28000, 28000)
at2 = ActivityTracker('Bob', 1.0, time_period6)
print("does " + str(time_period1) + " overlap " + str(time_period6) + " = " + str(does_time_period_overlap(at1, at2)))

print()
print("TEST get_activity_tracker_union")
time_period1 = TimePeriod(20000, 24000)
time_period2 = TimePeriod(22000, 26000)
at1 = ActivityTracker('Bob', 1.0, time_period1)
at2 = ActivityTracker('Bob', 1.0, time_period2)
print("merging " + str(time_period1) + " and " + str(time_period2) + " = " + str(get_activity_tracker_union(at1, at2)))

print()
print("TEST contains_overlapping_time_periods")
time_period1 = TimePeriod(20000, 28000)
time_period2 = TimePeriod(20000, 28000)
at1 = ActivityTracker('Bob', 1.0, time_period1)
at2 = ActivityTracker('Bob', 1.0, time_period2)
at_set = [at1, at2]
print("does " + str(time_period1) + " overlap " + str(time_period2) + " = " + str(contains_overlapping_time_periods(at_set)))
time_period3 = TimePeriod(26000, 30000)
at2 = ActivityTracker('Bob', 1.0, time_period3)
at_set = [at1, at2]
print("does " + str(time_period1) + " overlap " + str(time_period3) + " = " + str(contains_overlapping_time_periods(at_set)))
time_period4 = TimePeriod(29000, 30000)
at2 = ActivityTracker('Bob', 1.0, time_period4)
at_set = [at1, at2]
print("does " + str(time_period1) + " overlap " + str(time_period4) + " = " + str(contains_overlapping_time_periods(at_set)))
time_period5 = TimePeriod(20000, 20000)
at2 = ActivityTracker('Bob', 1.0, time_period5)
at_set = [at1, at2]
print("does " + str(time_period1) + " overlap " + str(time_period5) + " = " + str(contains_overlapping_time_periods(at_set)))
time_period6 = TimePeriod(28000, 28000)
at2 = ActivityTracker('Bob', 1.0, time_period6)
at_set = [at1, at2]
print("does " + str(time_period1) + " overlap " + str(time_period6) + " = " + str(contains_overlapping_time_periods(at_set)))

print()
print("TEST get_non_overlapping_activity_tracker_set")
time_period1 = TimePeriod(20000, 28000)
time_period2 = TimePeriod(20000, 28000)
at1 = ActivityTracker('Bob', 1.0, time_period1)
at2 = ActivityTracker('Bob', 1.0, time_period2)
at_set = [at1, at2]
print("merge " + str(time_period1) + " and " + str(time_period2) + " = " + str(get_non_overlapping_activity_tracker_set(at_set)))
time_period3 = TimePeriod(26000, 30000)
at2 = ActivityTracker('Bob', 1.0, time_period3)
at_set = [at1, at2]
print("merge " + str(time_period1) + " and " + str(time_period3) + " = " + str(get_non_overlapping_activity_tracker_set(at_set)))
time_period4 = TimePeriod(29000, 30000)
at2 = ActivityTracker('Bob', 1.0, time_period4)
at_set = [at1, at2]
print("merge " + str(time_period1) + " and " + str(time_period4) + " = " + str(get_non_overlapping_activity_tracker_set(at_set)))

print()
print("TEST ONGOING ACTIVITIES")
time_period1 = TimePeriod(20000, 28000)
time_period2 = TimePeriod(24000, -1)
at1 = ActivityTracker('Bob', 1.0, time_period1)
at2 = ActivityTracker('Bob', 1.0, time_period2)
print("does " + str(time_period1) + " overlap " + str(time_period2) + " = " + str(does_time_period_overlap(at1, at2)))
at_set = [at1, at2]
print("merge " + str(time_period1) + " and " + str(time_period2) + " = " + str(get_non_overlapping_activity_tracker_set(at_set)))

print("TEST SAME ONGOING ACTIVITIES")
time_period1 = TimePeriod(24000, -1)
time_period2 = TimePeriod(24000, -1)
at1 = ActivityTracker('Bob', 1.0, time_period1)
at2 = ActivityTracker('Bob', 1.0, time_period2)
print("does " + str(time_period1) + " overlap " + str(time_period2) + " = " + str(does_time_period_overlap(at1, at2)))
at_set = [at1, at2]
print("merge " + str(time_period1) + " and " + str(time_period2) + " = " + str(get_non_overlapping_activity_tracker_set(at_set)))

print()
print("TEST get_non_overlap_union")
time_period1 = TimePeriod(20000, 24000)
time_period2 = TimePeriod(22000, 26000)
at1 = ActivityTracker('Bob', 1.0, time_period1)
at2 = ActivityTracker('Bob', 1.0, time_period2)
print("merging " + str(time_period1) + " and " + str(time_period2) + " = " + str(get_activity_tracker_non_overlap_union(at1, at2)))

print()
print("TEST get_uniquely_non_overlapping_activity_tracker_set")
time_period1 = TimePeriod(20000, 28000)
time_period2 = TimePeriod(20000, 28000)
at1 = ActivityTracker('Bob', 1.0, time_period1)
at2 = ActivityTracker('Bob', 1.0, time_period2)
at_set = [at1, at2]
print("merge " + str(time_period1) + " and " + str(time_period2) + " = " + str(get_uniquely_non_overlapping_activity_tracker_set(at_set)))
time_period3 = TimePeriod(26000, 30000)
at2 = ActivityTracker('Bob', 1.0, time_period3)
at_set = [at1, at2]
print("merge " + str(time_period1) + " and " + str(time_period3) + " = " + str(get_uniquely_non_overlapping_activity_tracker_set(at_set)))
time_period4 = TimePeriod(29000, 30000)
at2 = ActivityTracker('Bob', 1.0, time_period4)
at_set = [at1, at2]
print("merge " + str(time_period1) + " and " + str(time_period4) + " = " + str(get_uniquely_non_overlapping_activity_tracker_set(at_set)))
