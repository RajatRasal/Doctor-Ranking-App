"""
Test wiring of the Flask server controller functions which connect to the
backend model.
"""
import mock
import pytest

from tests.helper import does_not_raise
from src.server import create_app

class TestFlaskServer:

    def test_sanity_check(self, test_client):
        response = test_client.get('/test')
        assert response.status_code == 200
        assert response.get_data() == b'Hello World!'

    @mock.patch('src.ranking_engine.HcpRankingEngine.list_diseases')
    def test_server_gets_list_of_diseases_and_returns_200(self, patch_engine,
                                                          test_client):
        all_diseases = ['disease 1', 'disease 2']
        patch_engine.return_value = all_diseases

        response = test_client.get('/diseases')

        assert response.status_code == 200
        assert response.is_json

        patch_engine.assert_called_once()

        assert response.get_json() == {'diseases': all_diseases} 

    @mock.patch('src.ranking_engine.HcpRankingEngine.list_parameters')
    def test_server_gets_list_of_diseases_and_returns_200(self, patch_engine,
                                                          test_client):
        disease = 'test disease 1'
        parameters = [('x', 4), ('y', 3)]

        patch_engine.return_value = parameters

        print(f'/diseases/{disease}')

        response = test_client.post(f'/diseases/{disease}')

        assert response.status_code == 200
        assert response.is_json

        patch_engine.assert_called_once_with(disease)

        assert response.get_json() == [{'parameter': 'x', 'importance': 3},
                                       {'parameter': 'y', 'importance': 4}]

    @mock.patch('src.ranking_engine.HcpRankingEngine.count_doctors')
    def test_server_gets_list_of_diseases_and_returns_200(self, patch_engine,
                                                          test_client):
        patch_engine.return_value = 5 

        response = test_client.get(f'/doctors/count')

        assert response.status_code == 200
        assert response.is_json

        patch_engine.assert_called_once_with()

        assert response.get_json() == {'count': 5}

    @mock.patch('src.ranking_engine.HcpRankingEngine.rank_doctors')
    def test_server_rank_doctors_and_returns_200(self, patch_engine, 
                                                 test_client):
        result = [('doctor 1', 10), ('doctor 2', 9), ('doctor 3', 8)]
        disease = 'test disease 1'

        patch_engine.return_value = result 

        response = test_client.get(f'/doctors/rank/{disease}/1/2')

        assert response.status_code == 200
        assert response.is_json

        patch_engine.assert_called_once_with(disease)

        expected_res_top = [{'hcp_name': 'doctor 1', 'score': 10}]
        expected_res_bottom = [{'hcp_name': 'doctor 2', 'score': 9},
                               {'hcp_name': 'doctor 3', 'score': 8}]

        assert response.get_json() == {'top': expected_res_top, 
                                       'bottom': expected_res_bottom}

    @mock.patch('src.ranking_engine.HcpRankingEngine.rank_doctors')
    def test_server_rank_doctors_bigger_limit_and_returns_200(self,
                                                              patch_engine,
                                                              test_client):
        result = [('doctor 1', 10), ('doctor 2', 9), ('doctor 3', 8)]
        disease = 'test disease 1'

        patch_engine.return_value = result 

        response = test_client.get(f'/doctors/rank/{disease}/5/0')

        assert response.status_code == 200
        assert response.is_json

        patch_engine.assert_called_once_with(disease)

        expected_res_top = [{'hcp_name': 'doctor 1', 'score': 10},
                            {'hcp_name': 'doctor 2', 'score': 9},
                            {'hcp_name': 'doctor 3', 'score': 8}]

        assert response.get_json()['top'] == expected_res_top

    @mock.patch('src.ranking_engine.HcpRankingEngine.rank_doctors')
    def test_server_rank_doctors_negative_bottom_limit_return_400(self,
                                                                  patch_engine,
                                                                  test_client):
        disease = 'test disease 1'

        response = test_client.get(f'/doctors/rank/{disease}/1/-1')

        patch_engine.assert_not_called()

        assert response.status_code == 404
        assert not response.is_json

    @mock.patch('src.ranking_engine.HcpRankingEngine.rank_doctors')
    def test_server_rank_doctors_negative_top_limit_return_400(self,
                                                               patch_engine,
                                                               test_client):
        disease = 'test disease 1'

        response = test_client.get(f'/doctors/rank/{disease}/-1/1')

        patch_engine.assert_not_called()

        assert response.status_code == 404
        assert not response.is_json

    @mock.patch('src.ranking_engine.HcpRankingEngine.rank_doctors')
    def test_server_rank_doctors_bottom_lim_zero(self, patch_engine,
                                                 test_client):
        result = [('doctor 1', 10), ('doctor 2', 9), ('doctor 3', 8)]
        disease = 'test disease 1'

        patch_engine.return_value = result 

        response = test_client.get(f'/doctors/rank/{disease}/1/0')

        assert response.status_code == 200
        assert response.is_json

        patch_engine.assert_called_once_with(disease)

        expected_res_top = [{'hcp_name': 'doctor 1', 'score': 10}]

        assert response.get_json()['top'] == expected_res_top
        assert response.get_json()['bottom'] == []

    @mock.patch('src.ranking_engine.HcpRankingEngine.rank_doctors')
    def test_server_rank_doctors_zero_top_limit_return_empty_top_list(self,
                                                                      patch_engine,
                                                                      test_client):
        result = [('doctor 1', 10), ('doctor 2', 9), ('doctor 3', 8)]
        disease = 'test disease 1'

        patch_engine.return_value = result 

        response = test_client.get(f'/doctors/rank/{disease}/0/1')

        assert not response.get_json()['top']
        assert response.get_json()['bottom'] == [{'hcp_name': 'doctor 3',
                                                  'score': 8}]

    @mock.patch('src.ranking_engine.HcpRankingEngine.rank_doctors')
    def test_server_rank_doctors_zero_limits_return_400(self, patch_engine, 
                                                        test_client):
        patch_engine.return_value = []

        disease = 'test disease 1'
        response = test_client.get(f'/doctors/rank/{disease}/0/0')

        patch_engine.assert_not_called()

        assert response.status_code == 400
        assert not response.is_json
