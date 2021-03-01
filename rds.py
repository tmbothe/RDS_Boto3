import boto3
from client_factory import ECSClient
from ec2 import EC2


RDS_DB_SUBNET_NAME ='my-rds-subnet-group'

class RDS:
    def __init__(self,client):
        self._client = client
        """ :type :pyboto3.rds   """

    def create_postgresql_instance(self):
        print("Creating Amazon RDS PostgresSQL DB instance !")

        security_group_id = self.create_db_security_group_and_rules()

        #create subnet group
        self.create_db_subnet_group()
        print('Subnet group created')
        
        self._client.create_db_instance(
            DBName = 'MyPostgresSQLDB',
            DBInstanceIdentifier='mypostgresdb',
            DBInstanceClass='db.t2.micro',
            Engine = 'postgres',
            EngineVersion='9.6.6',
            Port = 5432,
            MasterUsername='postgres',
            masterUserPassword='mypostgrespassword',
            Allocatestorage = 20,
            MultiAZ=False,
            StorageType='gp2',
            PubliclyAccessible=True,
            VpcSecurityGroupIds=[security_group_id],
            DBSubnetGroupName = RDS_DB_SUBNET_NAME,
            Tags = [
                {
                    'Key' : 'Name',
                    'Value':'Thim'
                }
            ]
        )  

    def create_db_subnet_group(self):
        print('created RDS subnet group {RDS_DB_SUBNET_NAME}')
        self._client.create_db_subnet_group(
            DBSubnetGroupName=RDS_DB_SUBNET_NAME,
            DBSubnetGroupDescription='My own subnet group for RDS DB',
            SubnetIds = ['subnet-e65324cd','subnet-5e282615','subnet-ebb847b6','subnet-0902ef71']
        )

    def create_db_security_group_and_rules(self):
        ec2_client = ECSClient().get_client()
        ec2 = EC2(ec2_client)

        #Security group
        security_group = ec2.create_security_group()

        #get id of sg
        security_group_id = security_group['GroupId']

        print(f"created RD with security group {security_group_id}")

        #add public access rule to sg
        ec2.add_inbound_rule_to_sg(security_group_id)
        print(f'Added inbound public access rule to sg with id ={security_group_id}')

        return security_group_id



