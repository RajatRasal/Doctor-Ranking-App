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
        print('CODE TO INSERT ALL RECORDS INTO DB DIRECTLY')
        pass

    def __test_res(self, result_file):
        test_src_dir = os.path.dirname(os.path.abspath(__file__))
        sorted_res = os.path.join(test_src_dir, result_file)
        res_df = pd.read_csv(sorted_res, usecols=['hcp_number', 'score'])
        return [tuple(row) for row in res_df.values]
    
    @pytest.fixture()
    def test_res_1(self):
        res_file = 'sort_res_1.csv'
        return self.__test_res(res_file)
    
    @pytest.fixture()
    def test_res_3(self):
        res_file = 'sort_res_3.csv'
        return self.__test_res(res_file)

    def test_calculate_score_using_db(self, test_res_1, test_db_conn):
        disease_name = 'test disease 1'
        res = calculate_score_using_db(test_db_conn, disease_name)
        print('res:', len(res))
        print('test_res_1:', len(test_res_1))
        doctors_rank, score_rank = zip(*res)
        doctors_rank_exp, score_rank_exp = zip(*test_res_1)
        assert doctors_rank == doctors_rank_exp
        assert score_rank == score_rank_exp

    def test_calculate_score_using_db_matching_scores(self, test_res_3, test_db_conn):
        disease_name = 'test disease 3'
        res = calculate_score_using_db(test_db_conn, disease_name)
        print('res:', len(res))
        print('test_res_1:', len(test_res_3))
        doctors_rank, score_rank = zip(*res)
        doctors_rank_exp, score_rank_exp = zip(*test_res_3)
        assert doctors_rank == doctors_rank_exp
        assert score_rank == score_rank_exp
        assert res == test_res_3
