from uuid import uuid4

from adobe_config_mgmt_lib.dal import dynamodb


class TestDynamodbTableCreation:
    def test_create_new_random_table(self):
        """
        Create a new table with random name
        :return:
        """
        current_table_name = dynamodb.SERVICES_CONFIG_TABLE
        # Temporarily changing the table name to a random name to create a completely new table
        dynamodb.SERVICES_CONFIG_TABLE = uuid4().hex
        result = dynamodb.create_services_config_table()
        # Resetting the table name to actual name
        dynamodb.SERVICES_CONFIG_TABLE = current_table_name
        assert result is True

    def test_create_services_config_table(self):
        """
        Create a new table with actual/production table name
        It is possible that the table already exists
        :return:
        """
        result = dynamodb.create_services_config_table()
        assert result is True
