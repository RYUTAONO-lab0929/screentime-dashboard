### アーキテクチャ概要

```mermaid
flowchart LR
  subgraph Device[iPad 端末]
    A[DeviceActivity/FamilyControls] -->|JSON (日次)| B[HTTPS Upload]
  end

  B -->|Bearer + HMAC| API[(FastAPI)]
  API --> DB[(PostgreSQL / SQLite)]
  API --> Worker[APScheduler ETL]
  API --> Export[CSV/PDF]
  API --> Frontend
  Frontend[React + Vite + Plotly] --> User[研究者/参加者]

  subgraph Optional[ASM/MDM]
    MDM[CSV/JSON メタデータ] --> Import[tools/import_mdm.py]
    Import --> API
  end
```

- 日本時間(Asia/Tokyo)を標準に集計
- RBAC（admin/researcher/participant）
- 忘れられる権利の削除API
- 監査ログ、最小収集、仮名化ID
