terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "1.22.2"
    }
  }
}

variable "do_token" {}
variable "pvt_key" {}

provider "digitalocean" {
  token = var.do_token
}

data "digitalocean_ssh_key" "basil-mac-ssh-key" {
  name = "Basil Mac"
}

resource "digitalocean_droplet" "story-time-tr" {
  image = "docker-20-04"
  name = "story-time-tr"
  region = "fra1"
  size = "s-2vcpu-4gb"
  ssh_keys = [
    data.digitalocean_ssh_key.basil-mac-ssh-key.id
  ]
  connection {
    host = self.ipv4_address
    user = "root"
    type = "ssh"
    private_key = file(var.pvt_key)
    timeout = "2m"
  }

  provisioner "file" {
    source = "docker-compose.yml"
    destination = "/root/docker-compose.yml"
  }

  provisioner "remote-exec" {
    inline = [
      "docker-compose up -d"
    ]
  }
}