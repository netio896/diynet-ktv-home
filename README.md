# Diynet KTV · 阶段 1

面向本地 2TB+ 歌库的 KTV 系统，当前仓库包含完整可运行的「阶段 1」脚手架：
1. `http://localhost:8080` 能打开点歌前端。
2. 搜索调用 FastAPI + SQLite 歌库。
3. 点歌调用宿主机 MPV 播放 AVI/MKV 文件。

---

## 目录结构

```
G:\Projects\diynet-ktv-home
│
├── backend/              # FastAPI + SQLite 搜索/播放 API
│   └── app/
│       ├── main.py
│       ├── db.py
│       ├── models.py
│       └── routers/
│           ├── songs.py
│           └── player.py
│
├── frontend/             # Vue3 + Vite + Tailwind 点歌界面
│   ├── index.html
│   ├── package.json
│   └── src/
│       ├── App.vue
│       ├── main.js
│       ├── components/
│       │   ├── SearchBar.vue
│       │   └── SongList.vue
│       └── api/config.js
│
├── database/             # 歌库 CSV 与 SQLite 数据
│   ├── ktv_songs.csv     # 样例数据，替换为你的实际歌单
│   └── (运行 build_db.py 后生成 songs.db)
│
├── libraries/            # 实际歌曲文件（默认映射 G:/Diynet-KTV/libraries）
│   └── ...
│
├── docker/               # Compose + Dockerfile
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── docker-compose.yml
│
├── build_db.py           # 从 CSV 构建 SQLite 的脚本
└── README.md
```

---

## 运行前准备

1. **Windows 10/11 + PowerShell**
2. **Python 3.11**（用于 FastAPI 与构建数据库）
3. **Node.js 20+ / npm**（用于前端构建）
4. **Docker Desktop**（可选：若想“一键”启动前后端）
5. **MPV 播放器**（必须安装并加入 PATH，PowerShell 下执行 `mpv "G:\\ktv\\demo\\demo.AVI" --fullscreen` 必须成功）
6. 准备好歌曲 CSV（UTF-8 编码，包含 `artist,title,path` 三列）以及实际歌曲文件目录（例如 `G:/ktv/0/0/*.AVI`）。

---

## 1. 后端（FastAPI）

```powershell
cd G:\Projects\diynet-ktv-home\backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

启动：

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

API 调试：
- `http://localhost:5000/` 健康检查
- `http://localhost:5000/songs/search?keyword=朋友`
- `http://localhost:5000/player/play?path=G:/Diynet-KTV/libraries/0/0/pengyou.AVI`

> ⚠️ `player.py` 默认直接 `os.system("mpv ...")`。请确认路径映射正确（容器路径 `/app/libraries/...` 映射宿主 `G:/Diynet-KTV/libraries/...`）。如需更复杂逻辑，可在 `player.py` 中扩展转换函数。

---

## 2. 前端（Vue3 + Vite + Tailwind）

```powershell
cd G:\Projects\diynet-ktv-home\frontend
npm install
npm run dev -- --host 0.0.0.0 --port 8080
```

- 访问 `http://localhost:8080`
- `src/api/config.js` 默认：开发使用 `http://localhost:5000`，生产下走 `'/api'`，可通过 `.env` 设置 `VITE_API_BASE_URL`。

---

## 3. 构建 SQLite 歌库

1. 将你的 `ktv_songs.csv` 覆盖 `database/ktv_songs.csv`
2. 执行：

```powershell
cd G:\Projects\diynet-ktv-home
python build_db.py
```

脚本会：
- 创建（或复用）`database/songs.db`
- 读取 CSV 的 `artist / title / path` 插入 `songs` 表

> CSV 必须是 UTF-8 编码。若含有 GBK/Gb2312，先转换再导入。

---

## 4. Docker 一键启动

```powershell
cd G:\Projects\diynet-ktv-home\docker
docker compose up --build -d
```

- 前端：`http://localhost:8080`
- 后端：`http://localhost:5000`
- Compose 将 `../database` 与 `../libraries` 挂载到容器的 `/app/database`、`/app/libraries`

如需健康检查，可在 `docker-compose.yml` -> `backend` 中加入：

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/"]
  interval: 30s
  timeout: 10s
  retries: 3
```

---

## 5. 快速验证清单

- [ ] `mpv "G:\\ktv\\demo\\demo.AVI" --fullscreen` 在宿主机可正常播放
- [ ] `build_db.py` 运行成功，生成 `songs.db`
- [ ] FastAPI `GET /songs/search` 返回歌曲列表
- [ ] 前端搜索能展示结果，点击“播放”后端成功调用 MPV
- [ ] `docker compose up` 可以一键启动全部服务

---

## 下一阶段

阶段 1 完成后，可继续：
1. **阶段 2：GitHub 初始化 + CI/CD**（仓库推送、GitHub Actions 构建、Container Registry）
2. **阶段 3：远程访问/隧道/多端同步**

准备好继续时告诉我：“继续阶段 2：GitHub 初始化与同步”。

---

## 阶段 2：GitHub 初始化速览

> 详细手册位于 `docs/STAGE2_GITHUB.md`，以下为关键步骤摘要。

1. **初始化仓库**
   ```powershell
   cd G:\Projects\diynet-ktv-home
   git init
   git checkout -b main
   ```
2. **确认 `.gitignore` 生效**  
   - 忽略 `frontend/node_modules/`、`backend/.venv/`、`database/*.db`、`libraries/` 等大文件。
3. **首次提交与推送**
   ```powershell
   git add .
   git commit -m "chore: bootstrap diynet ktv stage 1"
   git remote add origin git@github.com:<USER>/diynet-ktv-home.git
   git push -u origin main
   ```
4. **分支建议**
   - `main` 稳定发布、`develop`（可选）集成功能、`feature/*` / `fix/*` 按需创建并通过 PR 合并。
5. **CI/CD 入口**  
   - 可在 `.github/workflows/ci.yml` 中添加前端构建 + 后端检查的 GitHub Actions（示例见手册）。

完成以上步骤即可把阶段 1 成果安全托管到 GitHub，为阶段 3 做准备。
