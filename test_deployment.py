from client_factory import RDSClient
from rds import RDS


def deploy_resources():
    rds_client = RDSClient().get_client()
    print(f'RDs client {rds_client}')
    
    rds = RDS(rds_client)

    rds.create_postgresql_instance()

    print("creating RDS PostGreSQL Instance")



if __name__=='__main__':
    deploy_resources()