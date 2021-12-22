variable "aws_region" {
  type = string
  default = "us-east-2"
}

variable "ec2_instance_type" {
  type = string
}

variable "external_directory" {
  type = string
  default = "external"
}

variable "aws_key_pair" {
  type = string
}

variable "pem_key_file_name" {
  type = string
}

variable "rdp_password" {
  type = string
}