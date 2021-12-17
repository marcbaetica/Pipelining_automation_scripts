provider "aws" {
  profile = "default"
  region  = "us-east-2"
}

data "external" "my_ip_address" {
  program = ["python", "external_computation/retrieve_public_ip_address.py"]
}

resource "aws_security_group" "marcb_access" {
  name        = "marcb-access"
  description = "Allow SSH, RDP traffic from personal pc."

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${data.external.my_ip_address.result.ip}/32"]
  }

  ingress {
    description = "RDP"
    from_port   = 3389
    to_port     = 3389
    protocol    = "tcp"
    cidr_blocks = ["${data.external.my_ip_address.result.ip}/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "my_ubuntu_machine" {
  key_name      = "Automation-Ohio"
  ami           = "ami-0fb653ca2d3203ac1"
  instance_type = "t2.micro"

  tags = {
    Name = "ubuntu"
  }

  vpc_security_group_ids = [aws_security_group.marcb_access.id]
}

output "your_ip" {
  value = data.external.my_ip_address.result.ip
}

output "security_group" {
  value = [aws_security_group.marcb_access.name, aws_security_group.marcb_access.id]
}

output "ec2_public_ip" {
  value = aws_instance.my_ubuntu_machine.public_ip
}
