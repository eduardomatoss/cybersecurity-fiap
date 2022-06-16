from unittest import TestCase
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from pytest import raises as pytest_raises

from app.schemas.deliveryman import DeliverymanBase as DeliverymanRequest
from app.database.models import Deliveryman as DeliverymanModel
from app.routers.deliveryman import (
    get_all_deliverymans,
    get_deliveryman_by_id,
    create_deliveryman,
    update_deliveryman,
)


@patch("app.routers.deliveryman.get_db")
class DeliverymanRouterTest(TestCase):
    def setUp(self):
        self.model_request = DeliverymanRequest(
            name="Jose",
            vehicle="Car",
        )
        self.model_response = DeliverymanModel(
            name="Jose",
            vehicle="Car",
            id=1,
        )

    def test_when_I_call_get_all_deliverymans_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(DeliverymanModel).all = MagicMock(
            return_value=[self.model_response]
        )
        response = get_all_deliverymans(get_db_mock)
        self.assertEqual(response, [self.model_response])

    def test_when_I_call_get_deliveryman_by_id_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(DeliverymanModel).get = MagicMock(
            return_value=self.model_response
        )
        response = get_deliveryman_by_id(
            2,
            get_db_mock,
        )
        self.assertEqual(response, self.model_response)

    def test_when_I_call_get_deliveryman_by_id_should_be_404_exception(
        self, get_db_mock
    ):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(DeliverymanModel).get = MagicMock(return_value=None)
        with pytest_raises(HTTPException):
            get_deliveryman_by_id(
                2,
                get_db_mock,
            )

    def test_when_I_call_create_deliveryman_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.add = MagicMock(return_value=self.model_response)
        response = create_deliveryman(self.model_request, get_db_mock)
        self.assertEqual(response.name, self.model_response.name)
        self.assertEqual(response.vehicle, self.model_response.vehicle)

    def test_when_I_call_update_deliveryman_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(DeliverymanModel).get = MagicMock(
            return_value=self.model_response
        )

        response = update_deliveryman(2, self.model_request, get_db_mock)
        self.assertEqual(response.name, self.model_response.name)
        self.assertEqual(response.vehicle, self.model_response.vehicle)

    def test_when_I_call_update_deliveryman_should_be_404_exception(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(DeliverymanModel).get = MagicMock(return_value=None)
        with pytest_raises(HTTPException):
            update_deliveryman(2, self.model_request, get_db_mock)
