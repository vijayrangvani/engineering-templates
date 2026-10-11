# TEMPLATE: pin Terraform + provider versions so runs are reproducible.
terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"     # any 5.x, never 6.x automatically
    }
  }
  # Remote state (team use): uncomment and create the bucket first.
  # backend "s3" {
  #   bucket = "my-tf-state"
  #   key    = "items/terraform.tfstate"
  #   region = "ap-south-1"
  # }
}

provider "aws" {
  region = var.region        # credentials come from env / ~/.aws, NEVER hard-coded here
  default_tags {
    tags = { Project = var.project, ManagedBy = "terraform" }   # applied to every resource
  }
}
