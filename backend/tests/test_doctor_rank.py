"""
Tests for the doctor ranking algorithm.
"""
import os
import pytest
import pandas as pd

from src.scoring import calculate_score_using_db

class TestCalculatingEngineWithDatabaseBackend:

    @pytest.fixture(autouse=True)
    def setup_load_into_db(self):
        print('SETUP----------------')
        pass
    
    @pytest.fixture()
    def test_res_1(self):
        test_src_dir = os.path.dirname(os.path.abspath(__file__))
        sorted_res = os.path.join(test_src_dir, 'sort_res_1.csv')
        res_df = pd.read_csv(sorted_res, usecols=['hcp_number', 'score'])
        return [tuple(row) for row in res_df.values]
    
    def test_calculate_score_using_db(self, test_res_1, test_db_conn):
        disease_name = 'Test Disease 1'
        print(test_res_1[:5])
        res = calculate_score_using_db(test_db_conn, disease_name)
        assert res == test_res_1
