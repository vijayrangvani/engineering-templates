# TEMPLATE: S3 bucket + a small EC2 instance with a security group.
# Shape of every resource:  resource "<provider>_<type>" "<local name>" { args }
# Reference another resource: <type>.<local name>.<attribute>

resource "aws_s3_bucket" "data" {
  bucket_prefix = "${var.project}-data-"   # prefix -> AWS adds a unique suffix (names are global)
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id   # reference -> Terraform orders creation for you
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Look up existing things with data sources (read-only).
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]   # Canonical
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd*/ubuntu-*-24.04-amd64-server-*"]
  }
}

resource "aws_security_group" "api" {
  name_prefix = "${var.project}-api-"
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {                          # allow all outbound
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "api" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.api.id]
  tags                   = { Name = "${var.project}-api" }
}
