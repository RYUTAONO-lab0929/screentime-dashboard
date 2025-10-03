## Screentime Dashboard (Research)

このリポジトリは、iPadのスクリーンタイムを研究目的で集計・可視化・レポート化するWebベースのダッシュボードの雛形です。

### 主要スタック
- Backend: FastAPI + SQLModel + Alembic
- DB: PostgreSQL (本番) / SQLite (開発)
- Frontend: React + Vite + Plotly
- Worker: APScheduler (ETL/日次集計)
- Infra: Docker Compose (db, api, worker, web, nginx)

### クイックスタート（ローカル）
```bash
cp .env.sample .env
make up
make migrate
make seed
# Nginx経由（推奨）
open http://localhost:3000
# 直アクセス（デバッグ用）
# Web: http://localhost:5173 / API: http://localhost:18000
```

ポート/エンドポイント
- Web(Nginx): http://localhost:3000
- API(直): http://localhost:18000
- DB(直): localhost:15432 (postgres/screentime)

### Ingest API（サンプル: iPadヘルパーからの日次JSON）
- `POST /ingest/v1/screentime`
  - Header: `Authorization: Bearer <token>`, `X-Timestamp: <ISO8601>`, `X-Signature: <hmac>`
  - Body: `{"source":"ipad","events":[{"device_id":"...","captured_at":"2025-10-01T12:00:00Z","payload":{}}]}`
  - 署名の作り方: `hex(hmac_sha256(HMAC_SECRET, X-Timestamp + '.' + body))`
  - 例（curl）
    ```bash
    TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    BODY='{"source":"ipad","events":[{"device_id":"D1","captured_at":"2025-09-30T12:00:00Z","payload":{}}]}'
    SIG=$(python - <<'PY'
import hmac, hashlib, os
secret=os.getenv('HMAC_SECRET','change-me').encode()
import sys
ts=sys.argv[1]
body=sys.argv[2].encode()
msg=(ts+'.'+body.decode()).encode()
print(hmac.new(secret,msg,hashlib.sha256).hexdigest())
PY
"$TS" "$BODY")
    curl -X POST http://localhost:3000/api/ingest/v1/screentime \
      -H "Authorization: Bearer role:participant:devtoken" \
      -H "Content-Type: application/json" \
      -H "X-Timestamp: $TS" -H "X-Signature: $SIG" \
      -d "$BODY"
    ```

### 分析API（主なもの）
- `GET /analytics/v1/kpi?from&to` 総分/カテゴリ比率/上位アプリ/通知/ピックアップ
- `GET /analytics/v1/timeseries?from&to&window=7` 日次合計と移動平均
- `GET /analytics/v1/dow-pattern?from&to` 曜日パターンと学校日/休日の平均
- `GET /analytics/v1/alerts?from&to&z=2.5` z-scoreによる急増検知
- `GET /analytics/v1/compliance?from&to` ルール遵守（limits対比/超過率/連続遵守）
- `GET /analytics/v1/cohort-timeseries?from&to` コホート別の時系列（`participants.cohort_id`）
- `GET /analytics/v1/summary?from&to&cohort=...`
- `GET /analytics/v1/participant/{id}/daily?from&to`

### エクスポート
- `GET /exports/v1/csv`（研究者ロール）
- `GET /exports/v1/pdf`（研究者ロール）
  - 研究者ロールはBearerトークンで代替: `Authorization: Bearer role:researcher:devtoken`

### ディレクトリ
- `backend/` FastAPIアプリ、モデル、マイグレーション
- `frontend/` Vite+Reactアプリ
- `infra/` Nginx設定
- `tools/` MDM取込スクリプト、シード生成

### フロントの使い方
- 画面上部のフィルタ（開始/終了日・移動平均）を変更するとグラフが更新
- KPIカード（総分/ピックアップ/通知/上位アプリ）
- カテゴリ比率ドーナツ、上位アプリ表、時系列（移動平均）を表示
- ダークモード切替: 右上の月アイコン（設定はローカルに保存）

### Makefile コマンド
```bash
make up         # コンテナ起動（db/api/web/worker/nginx）
make migrate    # Alembicマイグレーション適用
make seed       # シンセティックデータ投入（100名×30日＋limits）
make logs       # ログ追従
make openapi    # backend/openapi.json を生成
```

### 研究倫理/プライバシー
- 仮名化ID、最小収集、保持期間、削除API（`/privacy/v1/participant/{id}`）
- 署名検証（HMAC）、RBACスタブ

### 今後
- OIDC実装、RBAC強化、エクスポートPDF
- Celery化、OpenTelemetry計測
- IaC雛形（Terraform/Ansible）
