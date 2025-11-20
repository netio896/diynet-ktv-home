# 阶段 2 · GitHub 初始化与同步指南

> 目标：把阶段 1 产物放入 Git 版本管理，推送到远程仓库，并规划标准化工作流（分支、忽略策略、CI 入口）。

## 1. 初始化本地 Git 仓库

```powershell
cd G:\Projects\diynet-ktv-home
git init
git checkout -b main   # 若没有 main 分支
```

### 1.1 配置基础信息（如尚未设置）

```powershell
git config user.name  "Your Name"
git config user.email "your@email.com"
```

### 1.2 校验 .gitignore 是否生效

`.gitignore` 已忽略以下关键内容：

- `frontend/node_modules/`、`frontend/dist/`
- 所有 Python 虚拟环境 (`.venv/`, `backend/.venv/`)
- 二进制数据库文件 `database/*.db`
- 歌曲媒体目录 `libraries/`
- 各类 IDE 配置与 `.env`

运行 `git status -sb` 应只包含源代码和配置文件，若仍有大文件出现，可在 `.gitignore` 追加条目。

## 2. 首次提交

```powershell
git add .
git commit -m "chore: bootstrap diynet ktv stage 1"
```

> ⚠️ 确保没有 `database/songs.db`、`libraries/` 等大文件被暂存。必要时使用 `git rm --cached <file>` 取消跟踪。

## 3. GitHub 仓库创建与推送

1. 登陆 GitHub，新建仓库（建议名称：`diynet-ktv-home`）。
2. 通过命令行绑定远程：

   ```powershell
   git remote add origin git@github.com:<YOUR_USER>/diynet-ktv-home.git
   git push -u origin main
   ```

3. 若使用 HTTPS，可改为 `https://github.com/...`。

## 4. 分支与协作策略（建议）

- `main`：稳定可部署版本，仅合并完成测试的功能。
- `develop`（可选）：集成最新特性，再定期合并回 `main`。
- 功能分支：`feature/<scope>`，例如 `feature/player-mapping`。
- 修复分支：`fix/<issue>`。
- 使用 Pull Request 进行代码评审；合并前需通过自动化检查。

## 5. VS Code / IDE 工作流

- 打开仓库后，启用 Git 面板即可管理变更。
- 配置 VS Code Setting：`"git.autofetch": true`、`"git.confirmSync": false`（按需）。
- 建议安装插件：GitLens、GitHub Pull Requests。

## 6. GitHub Actions（可选拓展）

Create `.github/workflows/ci.yml`（后续阶段可实现）：

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci && npm run build
        working-directory: frontend
      - uses: actions/setup-python@v5
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt
        working-directory: backend
      - run: python -m compileall app
        working-directory: backend
```

> 阶段 3 可以在此基础上扩展容器构建、推送私有注册表等任务。

## 7. 常用 Git 命令速查

```powershell
git status -sb           # 精简状态
git log --oneline --graph --decorate
git pull --rebase origin main
git switch feature/xxx
git stash push "work in progress"
```

## 8. 常见问题

| 问题 | 解决方案 |
| --- | --- |
| `.venv` 等仍出现在 Git 中 | `git rm -r --cached .venv`，再提交 |
| `.db` 文件体积大，无法 push | 确认 `.gitignore` 生效，使用 `git lfs` 仅在必要时追踪媒体 |
| 需要清理误添加的 node_modules | `git rm -r --cached frontend/node_modules`，重新提交 |

---

完成以上步骤后，阶段 2 即告完成，可进入阶段 3（远程访问/隧道/多端同步）。
