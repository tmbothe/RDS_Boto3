from dynamodb import DynamoDB
from client_factory import DynamoDBClient


def get_dynamodb():
    dynamodb_client = DynamoDBClient().get_client()
    dynamodb = DynamoDB(dynamodb_client)
    return dynamodb


def create_dynamodb_table():
    dynamodb_client = DynamoDBClient().get_client()
    dynamodb = DynamoDB(dynamodb_client)

    table_name = 'Movies'

    # define attributes
    attribute_definitions = [
        {
            'AttributeName': 'year',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },

    ]

    # key schema
    key_schema = [
        {
            'AttributeName': 'year',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'title',
            'KeyType': 'RANGE'
        }
    ]

    initial_iops = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }

    dynamodb_create_table_response = dynamodb.create_table(
        table_name, attribute_definitions, key_schema, initial_iops
    )

    print(
        f'Created table {table_name} : {str(dynamodb_create_table_response)}')


def describe_table(table_name):
    print(str(get_dynamodb().describe_table(table_name)))


def update_table_iops():
    get_dynamodb().update_read_write_capacity("Movies", 10, 10)


def delete_table(table_name):
    get_dynamodb().delete_table_with_name(table_name)


if __name__ == '__main__':
    # create_dynamodb_table()
    # describe_table("Movies")
    # update_table_iops()
    # describe_table("Movies")
    delete_table("Movies")
