# F5 Self-Signed Certificate Generation

This repository contains files and instructions to generate a self-signed CA and sign a server certificate with SAN for `my_new_server.self` to use with F5 BIG-IP.

---

## Steps to generate certificates

### Option 1: Create a new self-signed CA and sign the server certificate

#### 1. Generate the CA private key and self-signed certificate (unencrypted):

```bash
openssl genrsa -out self_ca.key 4096

openssl req -new -x509 -days 3650 -key self_ca.key -out self_ca.crt \
  -subj "/C=US/ST=NY/L=Buffalo/O=My Org/CN=My Self-Signed CA"
2. Generate the server private key and CSR using the config file:
bash
Copy
Edit
openssl req -new -sha256 -nodes -out my_new_server.self.csr -newkey rsa:2048 \
  -keyout my_new_server.self.key -config my_new_server.self.txt
3. Sign the CSR with the CA certificate and key, including SAN extension:
bash
Copy
Edit
openssl x509 -req -in my_new_server.self.csr -CA self_ca.crt -CAkey self_ca.key -CAcreateserial \
  -out my_new_server.self.crt -days 730 -extfile v3.ext
4. Verify the generated certificate:
bash
Copy
Edit
openssl x509 -in my_new_server.self.crt -text -noout
Look for the Subject Alternative Name section in the output to confirm SAN is included.

Option 2: Sign a server certificate using an existing CA certificate and key
If you already have a CA certificate and private key (for example, existing_ca.crt and existing_ca.key), you can sign the CSR without generating a new CA.

1. Generate the server private key and CSR (same as above):
bash
Copy
Edit
openssl req -new -sha256 -nodes -out my_new_server.self.csr -newkey rsa:2048 \
  -keyout my_new_server.self.key -config my_new_server.self.txt
2. Sign the CSR with your existing CA certificate and key, including SAN extension:
bash
Copy
Edit
openssl x509 -req -in my_new_server.self.csr -CA existing_ca.crt -CAkey existing_ca.key -CAcreateserial \
  -out my_new_server.self.crt -days 730 -extfile v3.ext
Note: You will be prompted for the CA key password if the CA key is encrypted.

3. Verify the generated certificate:
bash
Copy
Edit
openssl x509 -in my_new_server.self.crt -text -noout