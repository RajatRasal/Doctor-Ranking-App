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
