## Terraform 雛形

本番運用を想定したIaCの雛形です（例）。実体のコードは環境固有のため省略。

- VPC, Subnets, Security Groups
- RDS for PostgreSQL (暗号化/自動バックアップ)
- ECS/EKS or VM (API/Worker/Web/Nginx)
- S3 (エクスポート/バックアップ)
- CloudWatch/Prometheus + Grafana
- Secrets Manager / Parameter Store
