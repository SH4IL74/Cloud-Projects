from scripts.step1_network import create_network
from scripts.step2_security import create_security_groups
from scripts.step3_storage_db import create_storage_and_database
from scripts.step4_app_messaging import deploy_compute_and_messaging

def main():
    print(" Starting Private Cloud Deployment inside /private-cloud... ")

    # Step 1: Network
    vpc_id,public_sub,private_subs = create_network()

    # Step 2: Security
    web_sg,db_sg = create_security_groups(vpc_id)

    # Step 3: Stprage and Database
    create_storage_and_database(private_subs, db_sg)

    # Step 4: Compute and Messaging
    deploy_compute_and_messaging(public_sub,web_sg)

    print("\n Private Cloud Successfully Provisioned")

if __name__ == "__main__":
    main()