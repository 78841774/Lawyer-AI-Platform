#!/bin/bash

# 路径设置
REPO_PATH="$HOME/Lawyer-AI-Platform"
cd "$REPO_PATH" || { echo "Repo not found!"; exit 1; }

# 1️⃣ 创建 Case Service 目录和文件
mkdir -p 07-Case-Service/backend/app/models
mkdir -p 07-Case-Service/backend/app/api
mkdir -p 07-Case-Service/docs

# 2️⃣ 数据库模型：Case
cat > 07-Case-Service/backend/app/models/case_model.py << 'EOF'
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
EOF

# 3️⃣ API 路由：Case
cat > 07-Case-Service/backend/app/api/case.py << 'EOF'
from fastapi import APIRouter, HTTPException
from app.models.case_model import Case
from app.database import SessionLocal

router = APIRouter()

@router.post("/cases")
def create_case(title: str, description: str = ""):
    db = SessionLocal()
    new_case = Case(title=title, description=description)
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    db.close()
    return new_case

@router.get("/cases/{case_id}")
def get_case(case_id: int):
    db = SessionLocal()
    case = db.query(Case).filter(Case.id == case_id).first()
    db.close()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
EOF

# 4️⃣ 文档
cat > 07-Case-Service/docs/API-Case-Service.md << 'EOF'
# Case Service API

## Endpoints

- POST /cases
- GET /cases/{case_id}
EOF

# 5️⃣ 更新仓库 README
echo -e "\n## v0.6 Case Service\n新增 Case Service API，包括案件创建与查询接口。" >> README.md

# 6️⃣ Git 提交
git add .
git commit -m "feat: add Case Service v0.6"
git push origin main

echo "✅ v0.6 Case Service 文件生成并提交完成"
