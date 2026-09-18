# --- Aurora Subnet Group ---

resource "aws_db_subnet_group" "main" {
  name       = "${local.name_prefix}-db-subnet"
  subnet_ids = aws_subnet.private_data[*].id
  tags       = { Name = "${local.name_prefix}-db-subnet" }
}

# --- Aurora Cluster ---

resource "aws_rds_cluster" "main" {
  cluster_identifier     = "${local.name_prefix}-aurora"
  engine                 = "aurora-postgresql"
  engine_mode            = "provisioned"
  database_name          = var.db_name
  master_username        = var.db_master_username
  manage_master_user_password = true
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.aurora.id]

  storage_encrypted   = true
  deletion_protection = true
  skip_final_snapshot = false
  final_snapshot_identifier = "${local.name_prefix}-aurora-final"

  backup_retention_period      = 7
  preferred_backup_window      = "03:00-04:00"
  preferred_maintenance_window = "sun:04:00-sun:05:00"

  tags = { Name = "${local.name_prefix}-aurora" }
}

# --- Aurora Instances (writer + reader across AZs) ---

resource "aws_rds_cluster_instance" "main" {
  count              = 2
  identifier         = "${local.name_prefix}-aurora-${count.index}"
  cluster_identifier = aws_rds_cluster.main.id
  instance_class     = var.db_instance_class
  engine             = aws_rds_cluster.main.engine

  publicly_accessible  = false
  db_subnet_group_name = aws_db_subnet_group.main.name

  tags = { Name = "${local.name_prefix}-aurora-${count.index}" }
}
