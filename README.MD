### Story Time

### Deploy to Digital Ocean manually
1. Create droplet with Docker image from marketplace attaching your ssh key
2. Test ssh connection: `ssh root@<droplet-ip>`
3. Upload all the files from repo to the droplet: `scp -r * root@64.225.100.127:/root/`
4. Login with ssh: `ssh root@<droplet-ip>`
5. Run the app: `docker-compose up -d`
6. Stop the app: `docker stop <containter-id>` (`docker ps` to find container id and running containers status)

### Authors:
* Nino Basilaia ninucabas@gmail.com
* Somesh Khandelia  
