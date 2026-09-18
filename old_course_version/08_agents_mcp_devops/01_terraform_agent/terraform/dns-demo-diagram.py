with Diagram("DNS Reliability Demo - Terraform Infrastructure", show=False, direction="TB"):

    # IAM resources (shared across regions)
    with Cluster("IAM"):
        role = IAMRole("EC2-SSM-Role")
        ssm_policy = IAMPermissions("SSM Managed\nInstance Core")
        role - ssm_policy

    # Primary Region
    with Cluster("Primary Region (us-east-2)"):
        with Cluster("Default VPC"):
            with Cluster("Subnet"):
                primary_ec2 = EC2Instance("Primary Web Server\nt4g.micro")
            primary_sg = Nacl("Security Group\nHTTP/HTTPS")

        primary_ami = AMI("Amazon Linux 2023\nARM64")

    # Secondary Region
    with Cluster("Secondary Region (us-west-2)"):
        with Cluster("Default VPC "):
            with Cluster("Subnet "):
                secondary_ec2 = EC2Instance("Secondary Web Server\nt4g.micro")
            secondary_sg = Nacl("Security Group\nHTTP/HTTPS")

        secondary_ami = AMI("Amazon Linux 2023\nARM64")

    # SSM Service
    ssm = SystemsManager("SSM Session\nManager")

    # Connections
    role >> Edge(label="Instance Profile") >> primary_ec2
    role >> Edge(label="Instance Profile") >> secondary_ec2

    primary_ami >> Edge(style="dashed") >> primary_ec2
    secondary_ami >> Edge(style="dashed") >> secondary_ec2

    primary_sg >> primary_ec2
    secondary_sg >> secondary_ec2

    primary_ec2 >> Edge(style="dashed", color="gray") >> ssm
    secondary_ec2 >> Edge(style="dashed", color="gray") >> ssm
