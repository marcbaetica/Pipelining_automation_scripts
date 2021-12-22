provider "aws" {
  profile = "default"
  region  = var.aws_region
}

data "external" "my_ip_address" {
  program = ["python", "retrieve_public_ip_address.py"]
  working_dir = var.external_directory
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
  key_name      = var.aws_key_pair
  ami           = "ami-0fb653ca2d3203ac1"
  instance_type = var.ec2_instance_type

  tags = {
    Name = "ubuntu"
  }

  vpc_security_group_ids = [aws_security_group.marcb_access.id]
}

// Separate from ec2 provisioning step to allow step to run on future ec2s.
resource "null_resource" "enable_rdp" {
  connection {
    type        = "ssh"
    user        = "ubuntu"
    host        = aws_instance.my_ubuntu_machine.public_ip
    private_key = file("${var.external_directory}/${var.pem_key_file_name}")  // TODO: Put inside var.
  }

  provisioner "file" {
    source = "${var.external_directory}/enable_rdp.sh"
    destination = "/home/ubuntu/enable_rdp.sh"  // TODO: Put inside var.
  }

  provisioner "remote-exec" {
    inline = [
      // "lsb_release -a",  // Logging OS version for debugging purposes.
//      "sed -i -e 's/\r$//' /home/ubuntu/enable_rdp.sh",  # Line endings conversion (if copied from Win FS).
//      "sudo chmod 777 /home/ubuntu/enable_rdp.sh",  // TODO: Put inside var.
//      "sudo /home/ubuntu/enable_rdp.sh",  // TODO: Put inside var.
      "echo '${var.rdp_password}\\n${var.rdp_password}' | sudo passwd ubuntu"  // XRDP looks for a user password during login. TODO: Put inside var and output at the end.
    ]
  }

  depends_on = [aws_instance.my_ubuntu_machine]
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

output "ec2_username" {
  value = aws_instance.my_ubuntu_machine.user_data
}

output "ec2_rdp_password" {
  value = var.rdp_password
}
