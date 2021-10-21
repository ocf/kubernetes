vault secrets enable -path=pki-elastic -description='PKI for Elastic stack' -max-lease-ttl=87600h pki
vault write pki-elastic/root/generate/internal common_name='Elastic stack root' ttl=87600h key_type=ec key_bits=521 organization='Open Computing Facility' permitted_dns_domains=ocf.berkeley.edu
vault secrets tune -max-lease-ttl=768h pki-elastic/
vault write pki-elastic/roles/client max_ttl=768h ttl=168h allow_localhost=false allowed_domains='ocf.berkeley.edu' allow_subdomains=true server_flag=false client_flag=true key_type=ec key_bits=521
