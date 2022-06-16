from unittest import TestCase
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from pytest import raises as pytest_raises

from app.schemas.delivery import DeliveryBase as DeliveryRequest
from app.database.models import Delivery as DeliveryModel
from app.routers.delivery import (
    get_all_deliverys,
    get_delivery_by_id,
    create_delivery,
    update_delivery,
)


@patch("app.routers.delivery.get_db")
class DeliveryRouterTest(TestCase):
    def setUp(self):
        self.model_request = DeliveryRequest(
            idBuyer=1,
            idProduct=1,
            idDeliveryman=1,
            deliverymanLat=-23.5613544,
            deliverymanLong=-46.660979,
            receiverCpf="11111111111",
            statusDelivery="DELIVERED",
        )
        self.model_response = DeliveryModel(
            id_buyer=1,
            id_product=1,
            id_deliveryman=1,
            deliveryman_lat=-23.5613544,
            deliveryman_long=-46.660979,
            receiver_cpf="11111111111",
            status_delivery="DELIVERED",
            id=1,
        )

    def test_when_I_call_get_all_deliverys_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(DeliveryModel).all = MagicMock(
            return_value=[self.model_response]
        )
        response = get_all_deliverys(get_db_mock)
        self.assertEqual(response, [self.model_response])

    def test_when_I_call_get_delivery_by_id_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(DeliveryModel).get = MagicMock(
            return_value=self.model_response
        )
        response = get_delivery_by_id(
            2,
            get_db_mock,
        )
        self.assertEqual(response, self.model_response)

    def test_when_I_call_get_delivery_by_id_should_be_404_exception(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(DeliveryModel).get = MagicMock(return_value=None)
        with pytest_raises(HTTPException):
            get_delivery_by_id(
                2,
                get_db_mock,
            )

    def test_when_I_call_create_delivery_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.add = MagicMock(return_value=self.model_response)
        response = create_delivery(self.model_request, get_db_mock)
        self.assertEqual(response.id_buyer, self.model_response.id_buyer)
        self.assertEqual(response.id_product, self.model_response.id_product)
        self.assertEqual(response.id_deliveryman, self.model_response.id_deliveryman)
        self.assertEqual(response.deliveryman_lat, self.model_response.deliveryman_lat)
        self.assertEqual(
            response.deliveryman_long, self.model_response.deliveryman_long
        )
        self.assertEqual(response.receiver_cpf, self.model_response.receiver_cpf)
        self.assertEqual(response.status_delivery, self.model_response.status_delivery)

    def test_when_I_call_update_delivery_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(DeliveryModel).get = MagicMock(
            return_value=self.model_response
        )

        response = update_delivery(2, self.model_request, get_db_mock)
        self.assertEqual(response.id_buyer, self.model_response.id_buyer)
        self.assertEqual(response.id_product, self.model_response.id_product)
        self.assertEqual(response.id_deliveryman, self.model_response.id_deliveryman)
        self.assertEqual(response.deliveryman_lat, self.model_response.deliveryman_lat)
        self.assertEqual(
            response.deliveryman_long, self.model_response.deliveryman_long
        )
        self.assertEqual(response.receiver_cpf, self.model_response.receiver_cpf)
        self.assertEqual(response.status_delivery, self.model_response.status_delivery)

    def test_when_I_call_update_delivery_should_be_404_exception(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(DeliveryModel).get = MagicMock(return_value=None)
        with pytest_raises(HTTPException):
            update_delivery(2, self.model_request, get_db_mock)
