from unittest import TestCase
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from pytest import raises as pytest_raises

from app.schemas.buyer import BuyerBase as BuyerRequest
from app.database.models import Buyer as BuyerModel
from app.routers.buyer import (
    get_all_buyers,
    get_buyer_by_id,
    create_buyer,
    update_buyer,
)


@patch("app.routers.buyer.get_db")
class BuyerRouterTest(TestCase):
    def setUp(self):
        self.model_request = BuyerRequest(
            name="Batata",
            cpf="11111111111",
            cep="00000000",
            addressNumber=10,
            addressLat=-23.5613544,
            addressLong=-46.660979,
        )
        self.model_response = BuyerModel(
            name="Batata",
            cpf="11111111111",
            cep="00000000",
            address_number=10,
            address_lat=-23.5613544,
            address_long=-46.660979,
            id=1,
        )

    def test_when_I_call_get_all_buyers_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(BuyerModel).all = MagicMock(
            return_value=[self.model_response]
        )
        response = get_all_buyers(get_db_mock)
        self.assertEqual(response, [self.model_response])

    def test_when_I_call_get_buyer_by_id_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(BuyerModel).get = MagicMock(return_value=self.model_response)
        response = get_buyer_by_id(
            2,
            get_db_mock,
        )
        self.assertEqual(response, self.model_response)

    def test_when_I_call_get_buyer_by_id_should_be_404_exception(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(BuyerModel).get = MagicMock(return_value=None)
        with pytest_raises(HTTPException):
            get_buyer_by_id(
                2,
                get_db_mock,
            )

    def test_when_I_call_create_buyer_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.add = MagicMock(return_value=self.model_response)
        response = create_buyer(self.model_request, get_db_mock)
        self.assertEqual(response.name, self.model_response.name)
        self.assertEqual(response.cpf, self.model_response.cpf)
        self.assertEqual(response.cep, self.model_response.cep)
        self.assertEqual(response.address_number, self.model_response.address_number)
        self.assertEqual(response.address_lat, self.model_response.address_lat)
        self.assertEqual(response.address_long, self.model_response.address_long)

    def test_when_I_call_update_buyer_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(BuyerModel).get = MagicMock(return_value=self.model_response)

        response = update_buyer(2, self.model_request, get_db_mock)
        self.assertEqual(response.name, self.model_response.name)
        self.assertEqual(response.cpf, self.model_response.cpf)
        self.assertEqual(response.cep, self.model_response.cep)
        self.assertEqual(response.address_number, self.model_response.address_number)
        self.assertEqual(response.address_lat, self.model_response.address_lat)
        self.assertEqual(response.address_long, self.model_response.address_long)

    def test_when_I_call_update_buyer_should_be_404_exception(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(BuyerModel).get = MagicMock(return_value=None)
        with pytest_raises(HTTPException):
            update_buyer(2, self.model_request, get_db_mock)
