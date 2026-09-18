"""
AWS Three-Tier Architecture Diagram
Generates: three-tier architecture with ALB, ECS Fargate, Aurora PostgreSQL
Usage: python diagram.py (requires diagrams package: pip install diagrams)
"""
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.general import Users
from diagrams.aws.security import ACM, IAMRole
from diagrams.aws.network import InternetGateway, ALB, NATGateway
from diagrams.aws.compute import Fargate, EC2AutoScaling
from diagrams.aws.management import CloudwatchLogs
from diagrams.aws.database import AuroraInstance

with Diagram("AWS Three-Tier Architecture", show=False, filename="diagram", direction="TB"):

    users = Users("Users")
    acm = ACM("ACM Certificate")

    with Cluster("VPC (10.0.0.0/16)"):

        with Cluster("Public Subnets - Presentation Tier"):
            igw = InternetGateway("Internet\nGateway")
            alb = ALB("ALB\nHTTPS:443\nTLS 1.3")
            nat1 = NATGateway("NAT GW AZ-1")
            nat2 = NATGateway("NAT GW AZ-2")

        with Cluster("Private App Subnets - Application Tier"):
            with Cluster("ECS Fargate Cluster"):
                task1 = Fargate("Fargate Task\nAZ-1 (Node.js)")
                task2 = Fargate("Fargate Task\nAZ-2 (Node.js)")
            scaling = EC2AutoScaling("Auto Scaling\nCPU 70%")
            logs = CloudwatchLogs("CloudWatch\nLogs")

        with Cluster("Private Data Subnets - Data Tier"):
            with Cluster("Aurora PostgreSQL Cluster"):
                writer = AuroraInstance("Writer\ndb.r6g.large")
                reader = AuroraInstance("Reader\ndb.r6g.large")

    exec_role = IAMRole("ECS Exec Role")
    task_role = IAMRole("ECS Task Role")

    # Main data flow: Users -> IGW -> ALB -> Fargate -> Aurora
    users >> Edge(label="HTTPS") >> igw
    igw >> alb
    acm >> Edge(style="dashed") >> alb
    alb >> task1
    alb >> task2
    task1 >> writer
    task2 >> writer
    writer - Edge(style="dashed", label="replication") - reader

    # Auto scaling and logging
    scaling >> Edge(style="dashed") >> task1
    scaling >> Edge(style="dashed") >> task2
