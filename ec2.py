
RDS_SECURITY_GROUP_NAME = "my-rds-public-sg"


class EC2:
    def __init__(self, client):
        self._client = client

    def create_security_group(self):
        print(f'creating RDS Security group {RDS_SECURITY_GROUP_NAME}')
        return self._client.create_security_group(
            GroupName=RDS_SECURITY_GROUP_NAME,
            Description='RDS security group for postgres dd',
            VpcId='vpc-6b26b613'
        )

    def add_inbound_rule_to_sg(self, security_group_id):
        print(f'Adding inbound access rule to Sg {security_group_id}')
        self._client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 5432,
                    'ToPort': 5432,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]

                }

            ]
        )
