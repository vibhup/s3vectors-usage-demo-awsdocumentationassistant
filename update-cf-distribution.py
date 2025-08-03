#!/usr/bin/env python3
import json

# Read the current distribution config
with open('/Users/vibhup/Downloads/embeddingdataset/dist-config.json', 'r') as f:
    config = json.load(f)

# Add custom domain to aliases
config['Aliases'] = {
    'Quantity': 1,
    'Items': ['your-custom-domain.com']
}

# Update SSL certificate configuration
config['ViewerCertificate'] = {
    'ACMCertificateArn': 'arn:aws:acm:us-east-1:YOUR-ACCOUNT-ID:certificate/YOUR-CERTIFICATE-ID',
    'SSLSupportMethod': 'sni-only',
    'MinimumProtocolVersion': 'TLSv1.2_2021',
    'CertificateSource': 'acm'
}

# Write the updated config
with open('/Users/vibhup/Downloads/embeddingdataset/updated-dist-config.json', 'w') as f:
    json.dump(config, f, indent=2)

print("Updated CloudFront distribution configuration created successfully!")
