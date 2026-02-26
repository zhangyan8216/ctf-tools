# VulnHunter Enterprise - API 文档

**版本**: 1.0.0
**Base URL**: http://localhost:5001/api

---

## 📋 基本信息

### 认证
大多数API端点需要API密钥认证。

```bash
# 设置API密钥
export VULNHUNTER_API_KEY="your-api-key"
```

在请求头中包含：
```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

### 响应格式
所有API响应遵循统一格式：

```json
{
  "success": true,
  "message": "操作成功",
  "data": {},
  "error": null
}
```

---

## 🔌 API 端点

### 1. 健康检查

检查服务是否正常运行。

#### 请求
```http
GET /api/health
```

#### 响应
```json
{
  "success": true,
  "message": "Service is healthy",
  "data": {
    "status": "running",
    "version": "1.0.0",
    "uptime": 3600
  }
}
```

---

### 2. 扫描任务

#### 2.1 创建扫描任务

创建新的漏洞扫描任务。

#### 请求
```http
POST /api/v1/scan
Content-Type: application/json

{
  "target": "https://example.com",
  "scan_type": "web",
  "depth": 3,
  "threads": 10,
  "enable_detection": {
    "sqli": true,
    "xss": true,
    "ssrf": true,
    "xxe": false
  },
  "format": "json"
}
```

**参数说明**:
- `target` (必需): 目标URL或IP
- `scan_type` (可选): 扫描类型 `web|network|port|all` (默认: `web`)
- `depth` (可选): 扫描深度 1-10 (默认: 3)
- `threads` (可选): 并发线程数 1-50 (默认: 10)
- `enable_detection` (可选): 启用哪些检测模块
- `format` (可选): 报告格式 `json|html|ascii` (默认: `json`)

#### 响应
```json
{
  "success": true,
  "message": "扫描任务已创建",
  "data": {
    "task_id": "scan_1234567890",
    "target": "https://example.com",
    "status": "pending",
    "created_at": "2026-02-26T10:00:00Z",
    "estimated_time": 300
  }
}
```

---

#### 2.2 查询扫描状态

查询扫描任务的当前状态。

#### 请求
```http
GET /api/v1/scan/{task_id}/status
```

#### 响应
```json
{
  "success": true,
  "message": "扫描任务状态",
  "data": {
    "task_id": "scan_1234567890",
    "target": "https://example.com",
    "status": "running",
    "progress": 65,
    "vulnerabilities_found": {
      "critical": 1,
      "high": 2,
      "medium": 3,
      "low": 5
    },
    "current_phase": "XSS检测",
    "started_at": "2026-02-26T10:00:00Z",
    "estimated_completion": "2026-02-26T10:05:00Z"
  }
}
```

**状态值**:
- `pending`: 等待中
- `running`: 运行中
- `completed`: 已完成
- `failed`: 失败
- `cancelled`: 已取消

---

#### 2.3 获取扫描结果

获取扫描任务的详细结果。

#### 请求
```http
GET /api/v1/scan/{task_id}/results
```

#### 响应
```json
{
  "success": true,
  "message": "扫描结果",
  "data": {
    "task_id": "scan_1234567890",
    "target": "https://example.com",
    "status": "completed",
    "scan_time": 245.5,
    "vulnerabilities": [
      {
        "id": "vuln_001",
        "type": "SQL Injection",
        "severity": "critical",
        "url": "https://example.com/page?id=1",
        "technique": "Union-Based",
        "payload": "' UNION SELECT * FROM users--",
        "evidence": "MySQL syntax error in response",
        "cve": null,
        "cvss_score": 9.8,
        "description": "检测到SQL注入漏洞",
        "remediation": "使用参数化查询",
        "references": [
          "https://owasp.org/www-community/attacks/SQL_Injection"
        ]
      },
      {
        "id": "vuln_002",
        "type": "XSS (Cross-Site Scripting)",
        "severity": "high",
        "url": "https://example.com/search?q=test",
        "technique": "Reflected",
        "payload": "<script>alert(document.cookie)</script>",
        "evidence": "Reflection found in response",
        "cve": null,
        "cvss_score": 7.5,
        "description": "检测到反射型XSS漏洞",
        "remediation": "对所有用户输入进行HTML实体编码",
        "references": [
          "https://owasp.org/www-community/attacks/xss/"
        ]
      }
    ],
    "summary": {
      "total": 2,
      "by_severity": {
        "critical": 1,
        "high": 1,
        "medium": 0,
        "low": 0,
        "info": 0
      },
      "by_type": {
        "SQL Injection": 1,
        "XSS": 1
      }
    }
  }
}
```

---

#### 2.4 下载扫描报告

下载扫描任务的报告文件。

#### 请求
```http
GET /api/v1/scan/{task_id}/report?format=html
```

**查询参数**:
- `format`: 报告格式 `html|pdf|ascii|json` (默认: `json`)

#### 响应
- 格式为 `json`: 使用标准JSON响应
- 格式为其他: 直接下载文件

---

#### 2.5 取消扫描任务

取消正在运行的扫描任务。

#### 请求
```http
DELETE /api/v1/scan/{task_id}
```

#### 响应
```json
{
  "success": true,
  "message": "扫描任务已取消",
  "data": {
    "task_id": "scan_1234567890",
    "status": "cancelled"
  }
}
```

---

### 3. 批量扫描

#### 3.1 创建批量扫描任务

为多个目标创建批量扫描。

#### 请求
```http
POST /api/v1/batch-scan
Content-Type: application/json

{
  "targets": [
    "https://example1.com",
    "https://example2.com",
    "192.168.1.100"
  ],
  "scan_type": "web",
  "depth": 2,
  "threads": 5,
  "format": "json"
}
```

#### 响应
```json
{
  "success": true,
  "message": "批量扫描任务已创建",
  "data": {
    "batch_id": "batch_1234567890",
    "total_targets": 3,
    "status": "pending",
    "tasks": [
      {
        "task_id": "scan_001",
        "target": "https://example1.com",
        "status": "pending"
      },
      {
        "task_id": "scan_002",
        "target": "https://example2.com",
        "status": "pending"
      },
      {
        "task_id": "scan_003",
        "target": "192.168.1.100",
        "status": "pending"
      }
    ]
  }
}
```

---

#### 3.2 查询批量扫描状态

#### 请求
```http
GET /api/v1/batch-scan/{batch_id}/status
```

#### 响应
```json
{
  "success": true,
  "message": "批量扫描状态",
  "data": {
    "batch_id": "batch_1234567890",
    "total_targets": 3,
    "completed": 1,
    "running": 1,
    "pending": 1,
    "failed": 0,
    "progress": 33.3,
    "vulnerabilities_found": {
      "critical": 1,
      "high": 2,
      "medium": 0,
      "low": 0
    }
  }
}
```

---

### 4. 漏洞利用

#### 4.1 生成利用Payload

为检测到的漏洞生成利用Payload。

#### 请求
```http
POST /api/v1/exploit/generate
Content-Type: application/json

{
  "vulnerability_id": "vuln_001",
  "vulnerability_type": "SQL Injection",
  "target_url": "https://example.com/page?id=1",
  "technique": "Union-Based"
}
```

#### 响应
```json
{
  "success": true,
  "message": "Payload生成成功",
  "data": {
    "payload_id": "payload_001",
    "payload": "' UNION SELECT 1,username,password FROM users--",
    "cves": ["CVE-2023-1234"],
    "exploitability": "high",
    "risk_level": "critical",
    "mitigation": "使用参数化查询或ORM框架"
  }
}
```

---

#### 4.2 执行利用测试

执行利用测试（仅在授权环境中使用）。

#### 请求
```http
POST /api/v1/exploit/execute
Content-Type: application/json

{
  "payload_id": "payload_001",
  "target_url": "https://example.com/page?id=1",
  "safe_mode": true
}
```

**参数说明**:
- `safe_mode`: 安全模式，只检测不进行实际利用 (默认: `true`)

#### 响应
```json
{
  "success": true,
  "message": "利用测试已完成",
  "data": {
    "test_result": "vulnerable",
    "confidence": 0.95,
    "evidence": "注入成功，返回了用户表数据",
    "warnings": [
      "此漏洞具有高风险",
      "建议立即修复"
    ]
  }
}
```

---

### 5. AI分析

#### 5.1 智能漏洞评估

使用AI评估漏洞的可利用性和风险。

#### 请求
```http
POST /api/v1/ai/analyze
Content-Type: application/json

{
  "scan_results": {
    "vulnerabilities": [
      {
        "type": "SQL Injection",
        "severity": "critical",
        "url": "https://example.com/page"
      }
    ]
  }
}
```

#### 响应
```json
{
  "success": true,
  "message": "AI分析完成",
  "data": {
    "overall_risk": "critical",
    "exploitability_score": 0.95,
    "risk_assessment": {
      "primary_risks": [
        "数据库完全暴露",
        "可能的数据泄露",
        "权限提升风险"
      ],
      "attack_vectors": [
        "SQL注入攻击",
        "盲注攻击",
        "时间盲注"
      ],
      "business_impact": "high"
    },
    "recommendations": [
      "立即修复SQL注入漏洞",
      "实施输入验证和参数化查询",
      "升级数据库驱动到最新版本"
    ],
    "priority_order": [
      "vuln_001 - SQL Injection (critical)",
      "vuln_002 - XSS (high)"
    ]
  }
}
```

---

### 6. 工具集成

#### 6.1 执行SQLMap

集成SQLMap进行SQL注入测试。

#### 请求
```http
POST /api/v1/tools/sqlmap
Content-Type: application/json

{
  "target_url": "https://example.com/page?id=1",
  "options": {
    "batch": true,
    "level": 3,
    "risk": 2,
    "dbs": true
  }
}
```

#### 响应
```json
{
  "success": true,
  "message": "SQLMap执行完成",
  "data": {
    "target": "https://example.com/page?id=1",
    "vulnerable": true,
    "dbms": "MySQL 8.0",
    "databases": ["information_schema", "ctfd"],
    "tables": {
      "ctfd": ["users", "challenges", "flags"]
    }
  }
}
```

---

#### 6.2 执行Nmap端口扫描

集成Nmap进行端口扫描。

#### 请求
```http
POST /api/v1/tools/nmap
Content-Type: application/json

{
  "target": "192.168.1.100",
  "ports": "1-1000",
  "options": {
    "-sV": true,
    "-sC": true,
    "-O": false
  }
}
```

#### 响应
```json
{
  "success": true,
  "message": "Nmap扫描完成",
  "data": {
    "target": "192.168.1.100",
    "open_ports": [
      {
        "port": 22,
        "protocol": "tcp",
        "service": "ssh",
        "version": "OpenSSH 8.2p1"
      },
      {
        "port": 80,
        "protocol": "tcp",
        "service": "http",
        "version": "nginx 1.18.0"
      }
    ],
    "os_guess": "Linux"
  }
}
```

---

### 7. 历史记录

#### 7.1 查询扫描历史

查询历史扫描记录。

#### 请求
```http
GET /api/v1/history?page=1&limit=20&status=completed
```

**查询参数**:
- `page`: 页码 (默认: 1)
- `limit`: 每页数量 (默认: 20)
- `status`: 状态过滤 `all|pending|running|completed|failed` (默认: `all`)

#### 响应
```json
{
  "success": true,
  "message": "扫描历史记录",
  "data": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "records": [
      {
        "task_id": "scan_1234567890",
        "target": "https://example.com",
        "scan_type": "web",
        "status": "completed",
        "vulnerabilities": 5,
        "created_at": "2026-02-26T10:00:00Z",
        "completed_at": "2026-02-26T10:05:00Z"
      }
    ]
  }
}
```

---

### 8. 配置管理

#### 8.1 获取当前配置

获取当前扫描器配置。

#### 请求
```http
GET /api/v1/config
```

#### 响应
```json
{
  "success": true,
  "message": "当前配置",
  "data": {
    "scanner": {
      "timeout": 10,
      "max_depth": 3,
      "threads": 10,
      "user_agent": "VulnHunter/1.0"
    },
    "detector": {
      "check_sqli": true,
      "check_xss": true,
      "check_ssrf": true,
      "check_xxe": true
    },
    "ai": {
      "enabled": true,
      "model": "gpt-3.5-turbo"
    }
  }
}
```

---

#### 8.2 更新配置

更新扫描器配置。

#### 请求
```http
PUT /api/v1/config
Content-Type: application/json

{
  "scanner": {
    "timeout": 15,
    "threads": 20
  },
  "detector": {
    "check_sqli": true,
    "check_xss": false
  }
}
```

#### 响应
```json
{
  "success": true,
  "message": "配置已更新",
  "data": {
    "updated_at": "2026-02-26T10:00:00Z"
  }
}
```

---

## 🔐 错误代码

| 错误码 | HTTP状态 | 说明 |
|--------|---------|------|
| `INVALID_REQUEST` | 400 | 请求参数无效 |
| `UNAUTHORIZED` | 401 | 未授权（API密钥无效） |
| `FORBIDDEN` | 403 | 权限不足 |
| `NOT_FOUND` | 404 | 资源不存在 |
| `RATE_LIMIT_EXCEEDED` | 429 | 超出速率限制 |
| `SERVER_ERROR` | 500 | 服务器内部错误 |

### 错误响应示例

```json
{
  "success": false,
  "message": "API密钥无效",
  "data": null,
  "error": {
    "code": "UNAUTHORIZED",
    "details": "提供的API密钥无效或已过期"
  }
}
```

---

## 📊 速率限制

- 免费用户: 100次请求/小时
- 付费用户: 1000次请求/小时

超出限制时返回 `429 Too Many Requests`。

---

## 🧪 示例代码

### Python示例

```python
import requests

# 配置
BASE_URL = "http://localhost:5001/api"
API_KEY = "your-api-key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 创建扫描任务
def create_scan():
    url = f"{BASE_URL}/v1/scan"
    data = {
        "target": "https://example.com",
        "scan_type": "web",
        "depth": 3,
        "threads": 10
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# 查询状态
def get_status(task_id):
    url = f"{BASE_URL}/v1/scan/{task_id}/status"
    response = requests.get(url, headers=headers)
    return response.json()

# 获取结果
def get_results(task_id):
    url = f"{BASE_URL}/v1/scan/{task_id}/results"
    response = requests.get(url, headers=headers)
    return response.json()

# 使用示例
result = create_scan()
print(f"任务ID: {result['data']['task_id']}")

task_id = result['data']['task_id']
status = get_status(task_id)
print(f"状态: {status['data']['status']}")
```

### curl示例

```bash
# 创建扫描
curl -X POST http://localhost:5001/api/v1/scan \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://example.com",
    "scan_type": "web"
  }'

# 查询状态
curl -X GET http://localhost:5001/api/v1/scan/scan_1234567890/status \
  -H "Authorization: Bearer YOUR_API_KEY"

# 获取结果
curl -X GET http://localhost:5001/api/v1/scan/scan_1234567890/results \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 📞 支持

如有问题，请联系：
- 📧 Email: support@vulnhunter.com
- 🐛 GitHub Issues: https://github.com/zhangyan8216/ctf-tools/issues
- 📚 文档: https://docs.vulnhunter.com

---

**API版本**: 1.0.0
**最后更新**: 2026-02-26
