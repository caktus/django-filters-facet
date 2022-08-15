#!/bin/sh
# Prints the Ansible vault password retrieved from the AWS Secrets Manager
set -e
export SECRET_ID="django-filters-facet-ansible-vault-password"
aws secretsmanager get-secret-value --secret-id ${SECRET_ID} --query SecretString --output text
