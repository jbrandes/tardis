from tardis.utilities.utils import async_run_command
from tardis.utilities.utils import htcondor_cmd_option_formatter
from tardis.utilities.utils import htcondor_csv_parser
from tardis.exceptions.tardisexceptions import AsyncRunCommandFailure

from ..utilities.utilities import run_async

from unittest import TestCase


class TestAsyncRunCommand(TestCase):
    def test_async_run_command(self):
        run_async(async_run_command, 'exit 0')
        run_async(async_run_command,'exit 255')

        with self.assertRaises(AsyncRunCommandFailure):
            run_async(async_run_command, 'exit 1')

        self.assertEqual(run_async(async_run_command, 'echo "Test"'), "Test")


class TestHTCondorCMDOptionFormatter(TestCase):
    def test_htcondor_cmd_option_formatter(self):
        options = {'pool': 'my-htcondor.local',
                   'test': None}
        options_string = htcondor_cmd_option_formatter(options)

        self.assertEqual(options_string, "-pool my-htcondor.local -test")


class TestHTCondorCSVParser(TestCase):
    def test_htcondor_csv_parser(self):
        htcondor_input = "\n".join(["exoscale-26d361290f\tUnclaimed\tIdle\t0.125\t0.125",
                                    "test_replace\tOwner\tIdle\tundefined\tundefined"])

        parsed_rows = htcondor_csv_parser(htcondor_input=htcondor_input,
                                          fieldnames=('Machine', 'State', 'Activity', 'Test1', 'Test2'),
                                          replacements=dict(undefined=None))

        self.assertEqual(next(parsed_rows), dict(Machine="exoscale-26d361290f",
                                                 State="Unclaimed",
                                                 Activity="Idle",
                                                 Test1="0.125",
                                                 Test2="0.125"))

        self.assertEqual(next(parsed_rows), dict(Machine="test_replace",
                                                 State="Owner",
                                                 Activity="Idle",
                                                 Test1=None,
                                                 Test2=None))
