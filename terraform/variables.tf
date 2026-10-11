# TEMPLATE: inputs. Override with terraform.tfvars or -var="project=x".
variable "region" {
  type    = string
  default = "ap-south-1"     # Mumbai
}

variable "project" {
  type    = string
  default = "items"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}
