from unittest import TestCase
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from pytest import raises as pytest_raises

from app.schemas.product import ProductBase as ProductBaseRequest
from app.database.models import Product as ProductModel
from app.routers.product import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
)


@patch("app.routers.product.get_db")
class ProductRouterTest(TestCase):
    def setUp(self):
        self.model_request = ProductBaseRequest(
            name="Smartphone", value=1000.00, quant=10
        )
        self.model_response = ProductModel(
            name="Smartphone",
            value=1000.00,
            quant=10,
            id=1,
        )

    def test_when_I_call_get_all_products_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(ProductModel).all = MagicMock(
            return_value=[self.model_response]
        )
        response = get_all_products(get_db_mock)
        self.assertEqual(response, [self.model_response])

    def test_when_I_call_get_product_by_id_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(ProductModel).get = MagicMock(
            return_value=self.model_response
        )
        response = get_product_by_id(
            2,
            get_db_mock,
        )
        self.assertEqual(response, self.model_response)

    def test_when_I_call_get_product_by_id_should_be_404_exception(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(ProductModel).get = MagicMock(return_value=None)
        with pytest_raises(HTTPException):
            get_product_by_id(
                2,
                get_db_mock,
            )

    def test_when_I_call_create_product_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.add = MagicMock(return_value=self.model_response)
        response = create_product(self.model_request, get_db_mock)
        self.assertEqual(response.name, self.model_response.name)
        self.assertEqual(response.value, self.model_response.value)
        self.assertEqual(response.quant, self.model_response.quant)

    def test_when_I_call_update_product_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(ProductModel).get = MagicMock(
            return_value=self.model_response
        )

        response = update_product(2, self.model_request, get_db_mock)
        self.assertEqual(response.name, self.model_response.name)
        self.assertEqual(response.value, self.model_response.value)
        self.assertEqual(response.quant, self.model_response.quant)

    def test_when_I_call_update_product_should_be_404_exception(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(ProductModel).get = MagicMock(return_value=None)
        with pytest_raises(HTTPException):
            update_product(2, self.model_request, get_db_mock)
