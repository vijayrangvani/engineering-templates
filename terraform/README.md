# Terraform template (AWS)

```bash
terraform init        # download providers
terraform fmt         # format
terraform validate    # syntax / reference check
terraform plan        # preview changes, READ IT
terraform apply       # create (costs money)
terraform destroy     # delete everything when done practising
```
Files: `versions.tf` (pins + provider), `variables.tf` (inputs), `main.tf` (resources), `outputs.tf` (results).
Never commit `*.tfstate` or `*.tfvars` with secrets.
