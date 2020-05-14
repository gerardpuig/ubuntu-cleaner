import mock
import unittest

from ubuntucleaner.daemon.service import DaemonService


class TestDaemonService(unittest.TestCase):

    def test_get_cmd_pipe_no_process(self):
        with mock.patch.object(DaemonService, '__init__') as mocked_service:
            mocked_service.return_value = None

            mocked_service = DaemonService()
            assert mocked_service.get_cmd_pipe() == ('', 'None')

    def test_get_cmd_pipe_terminaled_none(self):
        with mock.patch.object(DaemonService, '__init__') as mocked_service:
            mocked_service.return_value = None

            mocked_service = DaemonService()
            mocked_service.p = mock.Mock()
            mocked_service.p.poll.return_value = None
            mocked_service.p.stdout.readline.return_value = "test"
            assert mocked_service.get_cmd_pipe() == ('test', 'None')

    def test_get_cmd_pipe_terminaled(self):
        with mock.patch.object(DaemonService, '__init__') as mocked_service:
            mocked_service.return_value = None

            mocked_service = DaemonService()
            mocked_service.p = mock.Mock()
            mocked_service.p.stdout.readlines.return_value = [b'test', b'stdout']
            assert mocked_service.get_cmd_pipe()[0] == b'test stdout'
