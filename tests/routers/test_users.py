from unittest import TestCase
from unittest.mock import MagicMock, patch

from app.schemas.users import UserBase as UserRequest
from app.database.models import Users as UsersModel
from app.routers.users import get_all_users, create_user


@patch("app.routers.users.get_db")
class UsersRouterTest(TestCase):
    def setUp(self):
        self.model_user_request = UserRequest(
            name="itsfakename",
        )
        self.model_user_response = UsersModel(
            name="itsfakename",
            id=1,
        )

    def test_when_I_call_get_all_users_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.query(UsersModel).all = MagicMock(
            return_value=[self.model_user_response]
        )
        response = get_all_users(get_db_mock)
        self.assertEqual(response, [self.model_user_response])

    def test_when_I_call_create_user_should_be_success(self, get_db_mock):
        get_db_mock = get_db_mock.return_value
        get_db_mock.add = MagicMock(return_value=self.model_user_response)
        response = create_user(self.model_user_request, get_db_mock)
        print(response)
        self.assertEqual(response.name, self.model_user_response.name)
