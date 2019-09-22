"""
Fixtures and constants for pytest files.
"""
import os
import sys

import pytest
from sqlalchemy import MetaData

from src.server import create_app

_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(_PROJECT_ROOT, 'src'))
sys.path.append(os.path.join(_PROJECT_ROOT, 'src/model'))

def _get_test_db_conn():
    """
    Wrapper for getting test database engine.
    """
    from src.model.db_connection import get_db_connection
    # Add configurations for test db AWS instance.
    return get_db_connection()

@pytest.fixture()
def test_db_conn():
    """
    Test fixture for connection to test database instance.
    """
    return _get_test_db_conn()

@pytest.fixture()
def test_db_metadata():
    """
    Test fixture for metadata for test database instance.
    """
    return MetaData(_get_test_db_conn())

@pytest.fixture()
def test_client():
    """
    Generate test client instance for Flask server.
    """
    return create_app().test_client()
