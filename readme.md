明白了，我给你整理一份**完整的文字版架构设计文档**，你可以直接交给团队或用在 Cursor 实现，不包含任何图，只是清晰的文字说明和目录结构。

---

# FastAPI 项目架构设计文档（文字版）

## 1️⃣ 项目目标

* 提供 REST API 接口服务
* 支持复杂业务逻辑拆分
* 可扩展到 100+ API
* 支持内部 Service 层、Repository 层
* 支持多环境（开发/测试/生产）
* 可在 Cursor/IDE 中直接实现和维护

---

## 2️⃣ 总体架构

```
HTTP Request
   │
   ▼
FastAPI 路由层 (Router)
   │
   ▼
Service 层 (业务逻辑)
   │
   ▼
Repository / DB / External API
```

* **Router（API 层）**：只负责 HTTP 请求/响应、参数校验
* **Service（业务层）**：处理核心业务逻辑
* **Repository（数据层）**：数据库或外部服务交互
* **Schema（数据模型）**：统一 Pydantic 模型定义请求/响应

---

## 3️⃣ 项目目录结构

```text
project_name/
├── pyproject.toml            # 打包、依赖、构建配置
├── README.md                 # 项目说明
├── src/                      # 源码目录 (src layout)
│   ├── app/
│   │   ├── main.py           # FastAPI 应用入口
│   │   └── api/
│   │       └── v1/
│   │           ├── api.py    # v1 路由总入口
│   │           ├── users.py  # 用户相关接口
│   │           └── items.py  # 商品相关接口
│   └── domain/
│       ├── __init__.py
│       ├── models.py         # Pydantic 数据模型
│       ├── services/
│       │   └── user_service.py
│       └── repositories/
│           └── user_repo.py
├── tests/                    # 单元测试
│   └── test_users.py
└── scripts/                  # 管理脚本
    └── populate_db.py
```

> 使用 `src layout` 保证安装后的 import 与开发环境一致。

---

## 4️⃣ 各层设计说明

### 4.1 Router 层（API）

* 文件：`src/app/api/v1/*.py`
* 功能：

  * 接收 HTTP 请求
  * 参数校验
  * 调用 Service 层
  * 返回响应
* 规范：

  * 一个文件对应一个资源模块（User、Item）
  * API 版本控制 `/api/v1/...`
  * 路由尽量保持 ≤50 行

---

### 4.2 Service 层（业务逻辑）

* 文件：`src/domain/services/*.py`
* 功能：

  * 核心业务逻辑
  * 调用 Repository
  * 可复用、不依赖 HTTP
* 规范：

  * 每个 Service 类处理一个业务域
  * 独立单元测试

---

### 4.3 Repository 层（数据访问）

* 文件：`src/domain/repositories/*.py`
* 功能：

  * 封装数据库、缓存、外部 API
  * 提供 CRUD 接口给 Service 调用
* 规范：

  * Repository 不处理业务逻辑
  * 封装数据源细节

---

### 4.4 Schema / Models（数据模型）

* 文件：`src/domain/models.py`
* 功能：

  * 统一定义请求、响应数据
  * 校验参数
* 规范：

  * 使用 Pydantic BaseModel
  * 分清请求模型（Create/Update）和响应模型（Read）

---

### 4.5 FastAPI 应用入口

* 文件：`src/app/main.py`
* 功能：

  * 创建 FastAPI 实例
  * 挂载版本化路由
  * 配置中间件（可选）
* 示例：

```python
from fastapi import FastAPI
from src.app.api.v1.api import router as v1_router

app = FastAPI(title="My API")
app.include_router(v1_router, prefix="/api/v1")
```

---

## 5️⃣ API 版本控制

* 使用 `api/v1/api.py` 统一注册路由：

```python
from fastapi import APIRouter
from .users import router as users_router
from .items import router as items_router

router = APIRouter()
router.include_router(users_router)
router.include_router(items_router)
```

* 升级到 v2，只需复制 v1 目录为 v2，修改路由即可

---

## 6️⃣ 测试策略

* **单元测试**：Service 层、Repository 层
* **集成测试**：API 层（使用 `TestClient`）
* 示例：

```python
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/api/v1/users/", json={"name": "Tom"})
    assert response.status_code == 200
    assert response.json()["name"] == "Tom"
```

---

## 7️⃣ 扩展建议

1. **依赖注入**

   * 对 Service/Repository 使用 `Depends`，方便替换实现或 Mock 测试
2. **中间件**

   * 日志、异常处理、请求计时、认证等
3. **异步支持**

   * 数据库或外部 API 支持 async 时，在 Repository / Service 层使用 async
4. **多包项目**

   * `src/domain` → domain 层
   * `src/core` → 核心工具函数
   * `src/libs` → 第三方封装

---

## 8️⃣ 总结

* 高内聚低耦合：路由只管 HTTP，Service 管理业务逻辑，Repository 管理数据
* 可维护性强：接口增加不会影响其他模块
* 可测试性好：Service 层可单独测试
* 可扩展性强：版本升级、异步、缓存都容易加
* `src layout` + 分层设计 = 企业级标准

---

