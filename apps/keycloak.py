import json

from transpire import helm
from transpire.resources import ConfigMap
from transpire.utils import get_versions

name = "keycloak"


def oidc_client(
    client_id: str,
    *,
    name: str,
    description: str,
    home_url: str,
    redirect_uris: list[str],
):
    return {
        "clientId": client_id,
        "name": name,
        "description": description,
        "baseUrl": home_url,
        "clientAuthenticatorType": "client-secret",
        "redirectUris": redirect_uris,
        "webOrigins": ["+"],
        "publicClient": False,
        "protocol": "openid-connect",
        "enabled": True,
    }


clients = [
    oidc_client(
        "argocd",
        name="ArgoCD",
        description="Declarative GitOps CD for Kubernetes",
        home_url="https://argo.ocf.berkeley.edu/",
        redirect_uris=["https://argo.ocf.berkeley.edu/auth/callback"],
    ),
    oidc_client(
        "hedgedoc",
        name="HedgeDoc",
        description="Collaborative markdown notes",
        home_url="https://notes.ocf.berkeley.edu/",
        redirect_uris=["https://notes.ocf.berkeley.edu/auth/oauth2/callback"],
    ),
    oidc_client(
        "outline",
        name="Outline",
        description="Team knowledge base & wiki",
        home_url="https://docs.ocf.berkeley.edu/",
        redirect_uris=["https://docs.ocf.berkeley.edu/auth/oidc.callback"],
    ),
    oidc_client(
        "id6",
        name="id6",
        description="Identification linking engine",
        home_url="https://github.com/ocf/id6",
        redirect_uris=["https://discord.ocf.berkeley.edu/*"],
    ),
]

keycloak_config_cli = {
    "id": "ocf",
    "realm": "ocf",
    "displayName": "OCF",
    "sslRequired": "all",
    "enabled": True,
    "registrationAllowed": False,
    "loginWithEmailAllowed": False,
    "loginTheme": "keywind",
    "accountTheme": "keycloak.v2",
    "adminTheme": "keycloak.v2",
    "emailTheme": "keycloak",
    "roles": {
        "realm": [
            {"name": "ocfstaff", "composite": False, "clientRole": False},
            {"name": "ocfroot", "composite": False, "clientRole": False},
            {"name": "opstaff", "composite": False, "clientRole": False},
        ]
    },
    "groups": [
        {"name": "ocf"},
        {"name": "ocfalumni"},
        {"name": "ocfapphost"},
        {"name": "ocfhpc"},
        {"name": "ocfofficers"},
        {
            "name": "ocfroot",
            "realmRoles": ["ocfroot"],
            "clientRoles": {
                "realm-management": [
                    "manage-clients",
                    "manage-events",
                    "manage-identity-providers",
                    "manage-realm",
                    "manage-users",
                    "manage-authorization",
                    "realm-admin",
                ]
            },
        },
        {"name": "ocfstaff", "realmRoles": ["ocfstaff"]},
        {"name": "opstaff", "realmRoles": ["opstaff"]},
        {"name": "sorry"},
    ],
    "clients": clients,
    "clientScopes": [
        {
            "name": "groups",
            "protocol": "openid-connect",
            "attributes": {
                "include.in.token.scope": "true",
                "display.on.consent.screen": "true",
            },
            "protocolMappers": [
                {
                    "name": "groups",
                    "protocol": "openid-connect",
                    "protocolMapper": "oidc-group-membership-mapper",
                    "consentRequired": False,
                    "config": {
                        "full.path": "false",
                        "id.token.claim": "true",
                        "access.token.claim": "true",
                        "claim.name": "groups",
                        "userinfo.token.claim": "true",
                    },
                }
            ],
        }
    ],
    "defaultDefaultClientScopes": [
        "acr",
        "email",
        "profile",
        "roles",
        "web-origins",
        "groups",
    ],
    "components": {
        "org.keycloak.storage.UserStorageProvider": [
            {
                "name": "ldap",
                "providerId": "ldap",
                "config": {
                    "enabled": ["true"],
                    "vendor": ["other"],
                    "connectionUrl": ["ldaps://ldap.ocf.berkeley.edu"],
                    "useTruststoreSpi": ["ldapsOnly"],
                    "connectionPooling": ["true"],
                    "authType": ["none"],
                    "editMode": ["READ_ONLY"],
                    "usersDn": ["ou=People,dc=OCF,dc=Berkeley,dc=EDU"],
                    "usernameLDAPAttribute": ["uid"],
                    "rdnLDAPAttribute": ["uid"],
                    "uuidLDAPAttribute": ["uid"],
                    "userObjectClasses": ["ocfAccount,account,posixAccount"],
                    "customUserSearchFilter": [
                        "(!(loginShell=/opt/share/utils/bin/sorried))"
                    ],
                    "searchScope": ["1"],
                    "pagination": ["true"],
                    "importEnabled": ["true"],
                    "batchSizeForSync": ["1000"],
                    "fullSyncPeriod": ["604800"],
                    "changedSyncPeriod": ["86400"],
                    "allowKerberosAuthentication": ["true"],
                    "kerberosRealm": ["OCF.BERKELEY.EDU"],
                    "serverPrincipal": ["HTTP/idm.ocf.berkeley.edu@OCF.BERKELEY.EDU"],
                    "keyTab": ["/vault/secrets/keytab"],
                    "debug": ["true"],
                    "useKerberosForPasswordAuthentication": ["true"],
                    "cachePolicy": ["DEFAULT"],
                    "syncRegistrations": ["false"],
                    "validatePasswordPolicy": ["false"],
                    "trustEmail": ["true"],
                    "priority": ["0"],
                },
                "subComponents": {
                    "org.keycloak.storage.ldap.mappers.LDAPStorageMapper": [
                        {
                            "name": "username",
                            "providerId": "user-attribute-ldap-mapper",
                            "subComponents": {},
                            "config": {
                                "ldap.attribute": ["uid"],
                                "is.mandatory.in.ldap": ["true"],
                                "always.read.value.from.ldap": ["false"],
                                "read.only": ["true"],
                                "user.model.attribute": ["username"],
                            },
                        },
                        {
                            "name": "email",
                            "providerId": "user-attribute-ldap-mapper",
                            "subComponents": {},
                            "config": {
                                "ldap.attribute": ["ocfEmail"],
                                "is.mandatory.in.ldap": ["true"],
                                "is.binary.attribute": ["false"],
                                "always.read.value.from.ldap": ["false"],
                                "read.only": ["true"],
                                "user.model.attribute": ["email"],
                            },
                        },
                        {
                            "name": "first name",
                            "providerId": "user-attribute-ldap-mapper",
                            "subComponents": {},
                            "config": {
                                "ldap.attribute": ["cn"],
                                "is.mandatory.in.ldap": ["true"],
                                "read.only": ["true"],
                                "always.read.value.from.ldap": ["true"],
                                "user.model.attribute": ["firstName"],
                            },
                        },
                        {
                            "name": "creation date",
                            "providerId": "user-attribute-ldap-mapper",
                            "subComponents": {},
                            "config": {
                                "ldap.attribute": ["createTimestamp"],
                                "is.mandatory.in.ldap": ["false"],
                                "read.only": ["true"],
                                "always.read.value.from.ldap": ["true"],
                                "user.model.attribute": ["createTimestamp"],
                            },
                        },
                        {
                            "name": "modify date",
                            "providerId": "user-attribute-ldap-mapper",
                            "subComponents": {},
                            "config": {
                                "ldap.attribute": ["modifyTimestamp"],
                                "is.mandatory.in.ldap": ["false"],
                                "read.only": ["true"],
                                "always.read.value.from.ldap": ["true"],
                                "user.model.attribute": ["modifyTimestamp"],
                            },
                        },
                        {
                            "name": "group",
                            "providerId": "group-ldap-mapper",
                            "subComponents": {},
                            "config": {
                                "mode": ["READ_ONLY"],
                                "membership.attribute.type": ["UID"],
                                "user.roles.retrieve.strategy": [
                                    "LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"
                                ],
                                "group.name.ldap.attribute": ["cn"],
                                "preserve.group.inheritance": ["false"],
                                "ignore.missing.groups": ["false"],
                                "membership.user.ldap.attribute": ["uid"],
                                "membership.ldap.attribute": ["memberUid"],
                                "group.object.classes": ["posixGroup"],
                                "groups.dn": ["ou=Group,dc=ocf,dc=Berkeley,dc=EDU"],
                                "memberof.ldap.attribute": ["memberOf"],
                                "drop.non.existing.groups.during.sync": ["false"],
                            },
                        },
                    ]
                },
            }
        ],
    },
}


krb5_conf = """
[libdefaults]
  default_realm = OCF.BERKELEY.EDU

# The following krb5.conf variables are only for MIT Kerberos.
  krb4_config = /etc/krb.conf
  krb4_realms = /etc/krb.realms
  kdc_timesync = 1
  ccache_type = 4
  forwardable = true
  proxiable = true

# The following libdefaults parameters are only for Heimdal Kerberos.
  v4_instance_resolve = false
  v4_name_convert = {
    host = {
      rcmd = host
      ftp = ftp
    }
    plain = {
      something = something-else
    }
  }
  fcc-mit-ticketflags = true

[realms]
  OCF.BERKELEY.EDU = {
    kdc = kerberos.ocf.berkeley.edu
    admin_server = kerberos.ocf.berkeley.edu
  }

[domain_realm]
  .ocf.berkeley.edu = OCF.BERKELEY.EDU
  ocf.berkeley.edu = OCF.BERKELEY.EDU

[login]
  krb4_convert = true
  krb4_get_tickets = false
"""

helm_values = {
    "auth": {"existingSecret": "keycloak", "existingSecretKey": "admin-password"},
    "production": True,
    "proxy": "edge",
    "httpRelativePath": "/",
    "replicaCount": 1,
    "podAnnotations": {
        "vault.hashicorp.com/agent-inject": "true",
        "vault.hashicorp.com/role": "keycloak",
        "vault.hashicorp.com/service": "https://vault.ocf.berkeley.edu/",
        "vault.hashicorp.com/agent-inject-secret-keytab": "kvv2/data/keycloak/keycloak",
        "vault.hashicorp.com/agent-inject-template-keytab": (
            "{{`"
            '{{- with secret "kvv2/data/keycloak/keycloak" -}}'
            "{{ base64Decode .Data.data.keytab }}"
            "{{- end}}"
            "`}}"
        ),
    },
    "initContainers": [
        {
            "name": "download-resources",
            "image": "alpine/git",
            "command": ["/bin/sh", "-c"],
            "args": [
                "mkdir -p /keycloak/themes/keywind && (git -C /keycloak/themes/keywind pull || git clone https://github.com/lukin/keywind /keycloak/themes/keywind)"
            ],
            "volumeMounts": [{"name": "keycloak", "mountPath": "/keycloak"}],
        }
    ],
    "ingress": {
        "enabled": True,
        "ingressClassName": "contour",
        "annotations": {
            "cert-manager.io/cluster-issuer": "letsencrypt",
            "ingress.kubernetes.io/force-ssl-redirect": "true",
            "kubernetes.io/tls-acme": "true",
        },
        "hostname": "idm.ocf.berkeley.edu",
        "tls": True,
    },
    "metrics": {"enabled": True},
    "keycloakConfigCli": {
        "enabled": True,
        "existingConfigmap": "keycloak-config-cli",
        "cleanupAfterFinished": {
            "enabled": True,
            "seconds": 0,
        },
    },
    "postgresql": {"enabled": False},
    "externalDatabase": {
        "host": "ocf-keycloak",
        "port": 5432,
        "user": "keycloak",
        "database": "keycloak",
        "existingSecret": "keycloak.ocf-keycloak.credentials.postgresql.acid.zalan.do",
        "existingSecretPasswordKey": "password",
    },
    "extraVolumes": [
        {"name": "krb5-conf", "configMap": {"name": "krb5-conf"}},
        {"name": "keycloak", "persistentVolumeClaim": {"claimName": "keycloak"}},
    ],
    "extraVolumeMounts": [
        {
            "name": "krb5-conf",
            "mountPath": "/etc/krb5.conf",
            "subPath": "krb5.conf",
        },
        {
            "mountPath": "/opt/bitnami/keycloak/themes/keywind",
            "name": "keycloak",
            "subPath": "themes/keywind/theme/keywind",
        },
    ],
}


def objects():
    yield ConfigMap("krb5-conf", data={"krb5.conf": krb5_conf}).build()
    yield ConfigMap(
        "keycloak-config-cli",
        data={"configuration": json.dumps(keycloak_config_cli)},
    ).build()

    yield {
        "apiVersion": "v1",
        "kind": "PersistentVolumeClaim",
        "metadata": {"name": "keycloak"},
        "spec": {
            "storageClassName": "rbd-nvme",
            "accessModes": ["ReadWriteOnce"],
            "resources": {"requests": {"storage": "2Gi"}},
        },
    }

    yield {
        "apiVersion": "acid.zalan.do/v1",
        "kind": "postgresql",
        "metadata": {"name": "ocf-keycloak"},
        "spec": {
            "teamId": "ocf",
            "volume": {
                "size": "32Gi",
                "storageClass": "rbd-nvme",
            },
            "numberOfInstances": 1,
            "users": {"keycloak": ["superuser", "createdb"]},
            "databases": {"keycloak": "keycloak"},
            "postgresql": {"version": "15"},
        },
    }

    yield from helm.build_chart_from_versions(
        name=name,
        versions=get_versions(__file__),
        values=helm_values,
    )
