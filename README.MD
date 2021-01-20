### Story Time

### Deploy to Digital Ocean manually
1. Create droplet with Docker image from marketplace attaching your ssh key
2. Test ssh connection: `ssh root@<droplet-ip>`
3. Upload all the files from repo to the droplet: `scp -r * root@<droplet-ip>:/root/`
4. Login with ssh: `ssh root@<droplet-ip>`
5. Run the app: `docker-compose up -d`
6. Stop the app: `docker-compose down`

### Install dependencies for the DL model
<pre>
pip install torch

pip install tqdm boto3 requests regex sentencepiece sacremoses

pip install pytorch-transformers
</pre>

### Authors:
* Nino Basilaia ninucabas@gmail.com
* Somesh Khandelia  someshkhandelia@gmail.com
