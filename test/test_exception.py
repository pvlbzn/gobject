import pytest

from gobject import exception

# mock the data
data = {'result': [], 'status': ''}


def test_ok_status():
    data['status'] = 'OK'
    assert data['status'] == exception.Status.OK.name


def test_zero_results_status():
    data['status'] = 'ZERO_RESULTS'
    assert data['status'] == exception.Status.ZERO_RESULTS.name


def test_over_query_status():
    data['status'] = 'OVER_QUERY_LIMIT'
    assert data['status'] == exception.Status.OVER_QUERY_LIMIT.name


def test_request_denied_status():
    data['status'] = 'REQUEST_DENIED'
    assert data['status'] == exception.Status.REQUEST_DENIED.name


def test_invalid_request_status():
    data['status'] = 'INVALID_REQUEST'
    assert data['status'] == exception.Status.INVALID_REQUEST.name


def test_unknown_error_status():
    data['status'] = 'UNKNOWN_ERROR'
    assert data['status'] == exception.Status.UNKNOWN_ERROR.name


def test_raise_zero_results_exception():
    if (data['status'] == exception.Status.UNKNOWN_ERROR.name):
        with pytest.raises(exception.UnknownError):
            raise exception.Status(
                exception.Status.UNKNOWN_ERROR).exception_pool['UNKNOWN_ERROR']
