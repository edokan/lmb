#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
        test_core.py
        ~~~~~

        :copyright: (c) by Lambda Labs, Inc.
        :license: BSD. See LICENSE.
"""
from contextlib import closing
from lmb import DEFAULT_PORT
import json
import urllib2
import urlparse


SERVER = "http://localhost:%s" % DEFAULT_PORT


def path(p, base=SERVER):
    return urlparse.urljoin(base, p)


def assert_online(url=SERVER):
    assert server_online(url), "Expected to see the server online at %s." % url


def assert_with(url, pred):
    """Assert predicate function.

    Predicate function takes pydata, request obj -> returns result, string
    """
    with closing(urllib2.urlopen(url)) as r:
        pydata = json.loads(r.read())
        pred, strn = pred(pydata, r)
        assert pred, strn


def code_is(code=200, resp=None):
    got = resp.code
    assert got == code, 'HTTP code expected: %d, got %d' % (code, got)


def successful_response(pydata, resp):
    code_is(200, resp)
    return 'status' in pydata


def server_online(url):
    try:
        urllib2.urlopen(url)
        return True
    except urllib2.URLError:
        return False
    return False


def test_server(url=SERVER):
    assert_online()
    with closing(urllib2.urlopen(url)) as u:
        pydata = json.loads(u.read())
        assert successful_response(pydata, u), \
            'Response should be json deserializable, got: %s' % pydata
