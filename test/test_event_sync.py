##############################################################################
#
# Copyright (C) BBC 2018
#
##############################################################################

import unittest
from copy import deepcopy

from src import event
from data import test_data


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.events_src_new_acks = deepcopy(test_data.events_src_new_acks)
        self.events_src_new = deepcopy(test_data.events_src_new)
        self.events_src_acks = deepcopy(test_data.events_src_acks)
        self.events_src_closed = deepcopy(test_data.events_src_closed)
        self.events_dest_new_acks = deepcopy(test_data.events_dest_new_acks)
        self.events_dest_new = deepcopy(test_data.events_dest_new)
        self.events_dest_closed = deepcopy(test_data.events_dest_closed)

    def test_no_events_to_be_closed_does_not_find_any_events_to_close(self):
        event_dest_differences = event.compare_events(self.events_src_new_acks, test_data.events_dest_new_acks, 'extra dest events')
        event_states_to_be_changed = event.find_event_states_to_be_changed(test_data.events_src_closed, event_dest_differences, 'Closed')
        self.assertEqual(event_states_to_be_changed, [])

    def test_1_event_closure_in_src_has_1_item_to_close_in_dest(self):
        event_key_to_close = u'mon040.local|@Live |/Status/DNS|check_telhc_dc_active|4'
        self.events_src_new_acks[event_key_to_close]
        del self.events_src_new_acks[event_key_to_close]
        extra_dest_events = event.compare_events(self.events_src_new_acks, test_data.events_dest_new_acks, 'extra dest events')
        event_states_to_be_changed = event.find_event_states_to_be_changed(test_data.events_src_closed, extra_dest_events, 'Closed')
        dest_event_that_matches = [self.events_dest_new_acks[event_key_to_close]['evid']]
        self.assertEqual(event_states_to_be_changed, dest_event_that_matches)

    def test_3_event_closures_in_src_results_in_3_items_to_close_in_dest(self):
        event_keys_to_remove = {
        u'mon148.local|@Stage zencommand|/Cmd/Fail|4|@alert SSH login to mon148.local with username root failed',
        u'mon150.local|@Stage mariadb-events_13306|/Status|mysql_result|4',
        u'mon150.local|@Stage mariadb-model_23306|/Status|mysql_result|4'}
        for event_key in event_keys_to_remove:
            del self.events_src_new_acks[event_key]

        extra_dest_events = event.compare_events(self.events_src_new_acks, test_data.events_dest_new_acks, 'extra dest events')
        event_states_to_be_changed = event.find_event_states_to_be_changed(extra_dest_events, self.events_src_closed, 'Closed')
        self.assertEqual(len(event_states_to_be_changed), 3)

    def test_1_event_reopen_in_src_has_1_item_to_reopen_in_dest(self):
        event_key = u'mon150.local|@Stage mariadb-events_13306|/Status|mysql_result|4'
        self.events_src_new[event_key]['eventState'] = 'New'
        event_states_to_be_changed = event.find_event_states_to_be_changed(test_data.events_src_new, self.events_dest_closed, 'New')
        self.assertEqual(event_states_to_be_changed, [self.events_dest_closed[event_key]['evid']])

    # test is weak but show we need care of ack's
    def test_1_event_ack_in_src_has_1_item_to_reopen_in_dest(self):
        event_key = u'mon150.local|@Stage mariadb-events_13306|/Status|mysql_result|4'
        self.events_src_acks[event_key]['eventState'] = 'Acknowledged'
        event_states_to_be_changed = event.find_event_states_to_be_changed(test_data.events_src_acks, self.events_dest_closed, 'New')
        self.assertEqual(event_states_to_be_changed, [self.events_dest_closed[event_key]['evid']])

    def test_1_ack_in_src_has_1_item_to_ack_in_dest(self):
        event_key1 = u'mon150.local|@Stage mariadb-events_13306|/Status|mysql_result|4'
        event_key2 = u'mon061.local|@Live memcached|/Cmd/Fail|1121|4'
        del self.events_src_acks[event_key1]
        event_states_to_be_changed = event.find_event_states_to_be_changed(self.events_src_acks, self.events_dest_new, 'Acknowledged')
        self.assertEqual(event_states_to_be_changed, [self.events_dest_new[event_key2]['evid']])

    def test_2_ack_in_src_has_2_item_to_ack_in_dest(self):
        event_key1 = u'mon150.local|@Stage mariadb-events_13306|/Status|mysql_result|4'
        event_key2 = u'mon061.local|@Live memcached|/Cmd/Fail|1121|4'
        self.events_dest_new[event_key1]['eventState'] = 'New'
        self.events_dest_new[event_key2]['eventState'] = 'New'
        event_states_to_be_changed = event.find_event_states_to_be_changed(self.events_src_acks, self.events_dest_new, 'Acknowledged')
        self.assertEqual(len(event_states_to_be_changed), 2)

    def test_2_unack_in_src_has_2_item_to_unack_in_dest(self):
        # to check u'mon150.local|@Stage mariadb-model_23306|/Status|mysql_result|4'
        # to check u'mon150.local|@Stage mariadb-events_13306|/Status|mysql_result|4'
        event_states_to_be_changed = event.find_event_states_to_be_changed(self.events_src_acks, self.events_dest_new, 'New')
        self.assertEqual(len(event_states_to_be_changed), 2)

    def test_1_log_entry_on_event_in_src_has_to_update_on_entry_in_dest(self):
        event_key = 'mon040.local|@Live |/Status/DNS|check_telhc_dc_active|4'
        self.events_src_new_acks[event_key]['log'].append([u'someone@company.co.uk',
                                                         u'2017-07-03 16:32:08',
                                                         u'test'])
        event_logs_to_be_changed = event.find_event_logs_to_be_changed(self.events_src_new_acks, self.events_dest_new_acks)
        self.assertEqual(len(event_logs_to_be_changed), 1)

    def test_2_log_entry_on_same_event_in_src_has_to_update_on_entries_in_dest(self):
        event_key = 'mon040.local|@Live |/Status/DNS|check_telhc_dc_active|4'
        self.events_src_new_acks[event_key]['log'].append([u'someone@company.co.uk',
                                                         u'2017-07-03 16:00:00',
                                                         u'test111'])
        self.events_src_new_acks[event_key]['log'].append([u'someone@company.co.uk',
                                                         u'2017-07-03 17:00:00',
                                                         u'test 2222'])
        log_changeset = event.find_event_logs_to_be_changed(self.events_src_new_acks, self.events_dest_new_acks)
        self.assertEqual(len(log_changeset), 2)
        # print '@@@', log_changeset

    def test_ack_log_entry_on_event_in_src_does_not_update_on_dest(self):
        event_key = 'mon040.local|@Live |/Status/DNS|check_telhc_dc_active|4'
        self.events_src_new_acks[event_key]['log'].append([u'someone@company.co.uk',
                                                         u'2017-07-03 17:03:05',
                                                         u'state changed to Acknowledged'])
        event_states_to_be_changed = event.find_event_logs_to_be_changed(self.events_src_new_acks, self.events_dest_new_acks)
        self.assertEqual(len(event_states_to_be_changed), 0)

    def test_1_new_log_entry_returns_as_new(self):
        src_event_log = [u'someone@company.co.uk', u'2017-07-03 16:32:08', u'new message !!!']
        dest_event_logs = [[u'someone@company.co.uk', u'2017-07-03 21:54:44', u'state changed to New'],
                        [u'someone@company.co.uk', u'2017-07-03 16:45:58',
                         u'<p>someone@company.co.uk, 2017-07-03 16:31:39, state changed to Closed</p>'],
                        [u'someone@company.co.uk', u'2017-07-03 16:45:58',
                         u'<p>someone@company.co.uk, 2017-07-03 16:32:08, state changed to New</p>']]
        self.assertTrue(event._is_log_new(src_event_log, dest_event_logs), 'event is already in B')

    def test_already_existing_log_entry_returns_as_old_when_entered_by_sync(self):
        src_event_log = [u'someone@company.co.uk', u'2017-07-03 16:32:08', u'old message !!!']
        dest_event_logs = [[u'someone@company.co.uk', u'2017-07-03 16:32:08',
                         u'someone@company.co.uk, 2017-07-03 16:32:08 , old message !!!'],
                        [u'someone@company.co.uk', u'2017-07-03 16:45:58',
                         u'<p>someone@company.co.uk, 2017-07-03 16:31:39, state changed to Closed</p>'],
                        [u'someone@company.co.uk', u'2017-07-03 16:45:58',
                         u'<p>someone@company.co.uk, 2017-07-03 16:32:08, state changed to New</p>']]
        self.assertFalse(event._is_log_new(src_event_log, dest_event_logs), 'event is new on B')

    # assumed to work because message on each system cannot be identical
    def test_already_existing_log_entry_returns_as_old(self):
        src_event_log = [u'someone@company.co.uk', u'2017-07-03 16:32:08', u'old message !!!']
        dest_event_logs = [[u'someone@company.co.uk', u'2017-07-03 16:45:58',
                         u'<p>someone@company.co.uk, 2017-07-03 16:31:39, state changed to Closed</p>'],
                        [u'someone@company.co.uk', u'2017-07-03 16:32:08', u'old message !!!'],
                        [u'someone@company.co.uk', u'2017-07-03 16:45:58',
                         u'<p>someone@company.co.uk, 2017-07-03 16:32:08, state changed to New</p>']]
        self.assertTrue(event._is_log_new(src_event_log, dest_event_logs), 'event is old on B')

    # in the event of reverse the direction of the sync DEST -> SRC check we avoid duplicating logs
    def test_already_existing_log_entry_skips_if_written_by_servim(self):
        src_event_log = [u'admin', u'2017-07-03 16:32:08', u'<div><p>someone@company.co.uk, 2017-07-03 16:32:08, </p><p>test</p></div>']
        dest_event_logs = [[u'someone@company.co.uk', u'2017-07-03 16:32:08', u'test']]
        self.assertFalse(event._is_log_new(src_event_log, dest_event_logs), 'problemo')

    def test_system_message_skips(self):
        src_event_logs = [[u'someone@company.co.uk', u'2017-07-03 16:32:08', u'state changed to New'],
                        [u'someone@company.co.uk', u'2017-07-03 16:31:39', u'state changed to Closed'],
                        [u'someone@company.co.uk', u'2017-07-03 16:32:08', u'state changed to Ack'],
                        [u'someone@company.co.uk', u'2017-07-03 16:32:08', u'Please refer Case']]
        dest_event_that_matches_value = {
            'log': [[u'someone@company.co.uk', u'2017-07-03 16:32:08', u'hello']],
            'severity': 4, 'evid': u'0242ac11-0019-9d66-11e7-600dc0965b97', 'eventState': u'New'}
        new_logs_in_events = event._find_new_logs_in_events(src_event_logs, dest_event_that_matches_value)
        self.assertEqual(len(new_logs_in_events), 0)

    # This is a test to show that users will create messages on one system only and that message when
    # synchronised will be in a different format on the destination system (due to monservice cert making the entry)
    # e.g. message field when copied will contain a sum of user, timestamp , message (so all properties are copied)
    # main problem is I can't override the user and timestamp field via the rest API  - thus only message field is used.
    # this example below shows the unlikely situation a user creates the exact same entry on system a and b
    # at the same time
    def test_same_message_on_src_and_dest_appears_as_new_message(self):
        src_event_logs = [[u'someone@company.co.uk', u'2017-07-03 16:32:08', u'hello']]
        dest_event_that_matches_value = {
            'log': [[u'someone@company.co.uk', u'2017-07-03 16:32:08', u'hello']],
            'severity': 4, 'evid': u'0242ac11-0019-9d66-11e7-600dc0965b97', 'eventState': u'New'}
        new_logs_in_events = event._find_new_logs_in_events(src_event_logs, dest_event_that_matches_value)
        self.assertEqual(len(new_logs_in_events), 1)

    def test_that_message_already_exists(self):
        src_event_logs = [[u'someone@company.co.uk', u'2017-07-03 16:32:08', u'<div><p>someone@company.co.uk, 2017-07-03 16:32:08, </p><p>new entry</p></div>']]
        dest_event_that_matches_value = {
            'log': [[u'someone@company.co.uk', u'2017-07-03 16:32:08', u'new entry']],
            'severity': 4, 'evid': u'0242ac11-0019-9d66-11e7-600dc0965b97', 'eventState': u'New'}
        new_logs_in_events = event._find_new_logs_in_events(src_event_logs, dest_event_that_matches_value)
        self.assertEqual(len(new_logs_in_events), 0)

    def test_sanitise_dedupid_sanitises(self):
        sane = u'app848.back.live.lbh.local|var_cache_httpd_cache-root|/Perf/Filesystem|inodeUsage_inodeUsage|Inode usage over 90 percent|5'
        src = u'app848.back.live.lbh.local|var_cache_httpd_cache-root|/Perf/Filesystem|inodeUsage_inodeUsage|Inode usage over 90 percent|5'
        dst = u'app848.back.live.lbh.local|var_cache_httpd_cache-root|/Perf/Filesystem|app848.back.live.lbh.local/inodeUsage_inodeUsage|Inode usage over 90 percent|5'
        self.assertEquals(event.sanitise_dedupid(src), sane)
        self.assertEquals(event.sanitise_dedupid(dst), sane)

if __name__ == "__main__":
    unittest.main()
