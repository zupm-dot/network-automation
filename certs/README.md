# Self-Signed Certificate Generation

This repository contains files and instructions to generate a self-signed CA and sign a server certificate with SAN for `my_new_server.self` to use with F5 BIG-IP.

Option 1: Create a new self-signed CA and sign the server certificate

Generate the CA private key and self-signed certificate (unencrypted):

```bash
openssl genrsa -out self_ca.key 4096

openssl req -new -x509 -days 3650 -key self_ca.key -out self_ca.crt \
  -subj "/C=US/ST=NY/L=Buffalo/O=My Org/CN=My Self-Signed CA"
```

Create text file for server configuration DN:

```ini
[req]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[dn]
C=US
ST=NY
L=Buffalo
O=My Org
CN=my_new_server.self

[req_ext]
subjectAltName = @alt_names

[alt_names]
DNS.1 = my_new_server.self
```

Create CSR:

```bash
openssl req -new -sha256 -nodes -out my_new_server.f5.com.csr -newkey rsa:2048 -keyout my_new_server.f5.key -config <( cat my_new_server.f5.com.txt )
```

Generate the server private key and CSR using the config file:

```bash
openssl req -new -sha256 -nodes -out  my_new_server.f5.com.csr -newkey rsa:2048 \
  -keyout  my_new_server.f5.com.key -config  my_new_server.f5.com.txt
```

Sign the CSR with the CA certificate and key, including SAN extension:

```bash
openssl x509 -req -in  my_new_server.f5.com.csr -CA self_ca.crt -CAkey self_ca.key -CAcreateserial \
  -out  my_new_server.f5.com.crt -days 730 -extfile v3.ext
```

Verify the generated certificate:

```bash
openssl x509 -in  my_new_server.f5.com.crt -text -noout


```

Option 2: Sign a server certificate using an existing CA certificate and key

Generate the server private key and CSR (same as above):

```bash
openssl req -new -sha256 -nodes -out  my_new_server.f5.com.csr -newkey rsa:2048 \
  -keyout  my_new_server.f5.com.key -config  my_new_server.f5.com.txt
```

Sign the CSR with your existing CA certificate and key, including SAN extension:

```bash
openssl x509 -req -in  my_new_server.f5.com.csr -CA existing_ca.crt -CAkey existing_ca.key -CAcreateserial \
  -out  my_new_server.f5.com.crt -days 730 -extfile v3.ext
```
Note: You will be prompted for the CA key password if the CA key is encrypted.

Verify the generated certificate:

```bash
openssl x509 -in  my_new_server.f5.com.crt -text -noout
```



Files description:
- my_new_server.self.txt: OpenSSL config file to generate the CSR with SAN
- v3.ext: Extension file used when signing the CSR to include SANs in the certificate
- self_ca.key and self_ca.crt: The generated CA private key and self-signed certificate (Option 1)
- my_new_server.self.key and my_new_server.self.crt: The server private key and signed certificate
- my_new_server.self.csr: The certificate signing request



