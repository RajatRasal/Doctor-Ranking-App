"""
Test wiring of the Flask server controller functions which connect to the
backend model.
"""
import mock
import pytest

from tests.helper import does_not_raise
from src.server import create_app
from src.model.tables import DatabaseAbstraction, PostgresDatabase
from src.ranking_engine import HcpRankingEngine 


class TestRankingEngine:

    def test_list_diseases_gets_all_diseases_from_db(self, test_db_conn):
        mock_db_abstraction = mock.create_autospec(DatabaseAbstraction)

        db = mock_db_abstraction(test_db_conn) 
        db.findall_records_in_table.return_value = [('disease 1',)]
        ranking_engine = HcpRankingEngine(db)

        res = ranking_engine.list_diseases()
        db.findall_records_in_table.assert_called_once_with('diseases', 'type')
        assert res == ['disease 1'] 

    @pytest.mark.parametrize('engine', [PostgresDatabase])
    def test_list_diseases_gets_all_diseases_from_postgres(self, test_db_conn,
                                                           engine):
        db = engine(test_db_conn) 
        ranking_engine = HcpRankingEngine(db)
        res = ranking_engine.list_diseases()
        assert res == ['test disease 1', 'test disease 2', 'test disease 3'] 

    @pytest.mark.parametrize('engine', [PostgresDatabase])
    def test_list_diseases_gets_params_and_importances_3(self, test_db_conn,
                                                         engine):
        db = engine(test_db_conn) 
        ranking_engine = HcpRankingEngine(db)
        res = ranking_engine.list_parameters('test disease 3')
        params_for_disease = [('activity - n', 0), ('distance', 1), 
                              ('hospital', 1), ('influencer', 1),
                              ('open to meet', 1), ('publications', 1),
                              ('specialization', 0), ('volume of patients', 0)]
        assert res == params_for_disease

    @pytest.mark.parametrize('engine', [PostgresDatabase])
    def test_list_diseases_gets_params_and_importances_1(self, test_db_conn,
                                                         engine):
        db = engine(test_db_conn) 
        ranking_engine = HcpRankingEngine(db)
        res = ranking_engine.list_parameters('test disease 1')
        params_for_disease = [('activity - n', 1), ('distance', 3), 
                              ('hospital', 2), ('influencer', 5),
                              ('open to meet', 5), ('publications', 3),
                              ('specialization', 3), ('volume of patients', 4)]
        assert res == params_for_disease
