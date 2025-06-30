# FreeIPA Password Reset Tool

[![Build Status](https://github.com/your-username/MCP-Tools/workflows/Multi-Platform%20Build/badge.svg)](https://github.com/your-username/MCP-Tools/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform Support](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](#平台支持)

一个强大的 FreeIPA 用户密码过期时间管理工具，支持批量操作、交互式界面和 Linux 平台部署。

## ✨ 特性亮点

- 🚀 **零依赖部署** - 独立可执行文件，无需 Python 环境
- 🐧 **Linux 专用** - 针对 Linux 平台优化，高兼容性设计
- 🎯 **批量操作** - 支持批量修改用户密码过期时间
- 🖥️ **交互式界面** - 用户友好的命令行交互体验
- 🧪 **演示模式** - 无需真实 FreeIPA 环境即可测试功能
- 📦 **简易安装** - 标准 Linux 安装方式，支持系统路径部署
- 🔧 **灵活配置** - 支持多种日期格式和用户选择方式

## 📋 目录

- [快速开始](#快速开始)
- [功能特性](#功能特性)
- [平台支持](#平台支持)
- [安装方法](#安装方法)
- [使用指南](#使用指南)
- [构建说明](#构建说明)
- [开发指南](#开发指南)
- [故障排除](#故障排除)
- [贡献指南](#贡献指南)

## 🚀 快速开始

### 下载预构建版本

从 [Releases](https://github.com/your-username/MCP-Tools/releases) 页面下载 Linux 版本：

```bash
# Linux x86_64
wget https://github.com/your-username/MCP-Tools/releases/latest/download/freeipa-password-reset-linux-x86_64.tar.gz
tar -xzf freeipa-password-reset-linux-x86_64.tar.gz

# Linux ARM64
wget https://github.com/your-username/MCP-Tools/releases/latest/download/freeipa-password-reset-linux-arm64.tar.gz
tar -xzf freeipa-password-reset-linux-arm64.tar.gz
```

### 立即体验

```bash
# 演示模式 - 无需 FreeIPA 环境
./freeipa-password-reset --demo

# 查看帮助信息
./freeipa-password-reset --help

# 列出演示用户
./freeipa-password-reset --demo --list-only
```

## 🎯 功能特性

### 核心功能

| 功能 | 描述 | 支持状态 |
|------|------|----------|
| **用户管理** | 列出 FreeIPA 用户及详细信息 | ✅ |
| **批量操作** | 批量修改多个用户密码过期时间 | ✅ |
| **交互式界面** | 友好的命令行交互体验 | ✅ |
| **演示模式** | 离线功能测试和培训 | ✅ |
| **多种日期格式** | 支持 ISO 8601 等多种日期格式 | ✅ |
| **用户选择** | 支持编号、用户名、"all" 等选择方式 | ✅ |
| **系统安装** | 标准 Linux 系统路径安装 | ✅ |

### 高级特性

- **智能日期解析** - 自动识别和验证日期格式
- **操作确认** - 重要操作前的安全确认机制
- **详细日志** - 完整的操作日志和错误信息
- **权限检查** - 自动验证 FreeIPA 管理权限
- **网络检测** - 智能检测 FreeIPA 服务器连接状态

## 🌍 平台支持

### 支持的平台

| 平台 | 架构 | 状态 | 最低版本要求 |
|------|------|------|-------------|
| **Linux** | x86_64 | ✅ 完全支持 | GLIBC 2.3.4+ (2003+) |
| **Linux** | ARM64 | ✅ 完全支持 | GLIBC 2.17+ |

### 兼容的 Linux 发行版

- **Ubuntu**: 12.04+ (Precise Pangolin)
- **CentOS/RHEL**: 6+ 
- **Debian**: 7+ (Wheezy)
- **SUSE**: 11+
- **Fedora**: 所有现代版本
- **Alpine**: 3.0+

## 📦 安装方法

### 方法一：系统安装（推荐）

```bash
# 下载并解压
wget https://github.com/your-username/MCP-Tools/releases/latest/download/freeipa-password-reset-linux-x86_64.tar.gz
tar --no-xattrs -xzf freeipa-password-reset-linux-x86_64.tar.gz

# 系统安装
sudo cp freeipa-password-reset /usr/local/bin/
sudo chmod +x /usr/local/bin/freeipa-password-reset

# 验证安装
freeipa-password-reset --help
```

### 方法二：直接运行

```bash
# 下载并解压
wget https://github.com/your-username/MCP-Tools/releases/latest/download/freeipa-password-reset-linux-x86_64.tar.gz
tar --no-xattrs -xzf freeipa-password-reset-linux-x86_64.tar.gz

# 添加执行权限
chmod +x freeipa-password-reset

# 直接运行
./freeipa-password-reset --help
```

## 📖 使用指南

### 基本用法

```bash
# 查看帮助信息
freeipa-password-reset --help

# 演示模式（推荐首次使用）
freeipa-password-reset --demo

# 连接到 FreeIPA 服务器
freeipa-password-reset --server ipa.example.com --username admin
```

### 演示模式

演示模式使用模拟数据，无需真实的 FreeIPA 环境：

```bash
# 列出模拟用户
freeipa-password-reset --demo --list-only

# 交互式演示
freeipa-password-reset --demo

# 批量操作演示
freeipa-password-reset --demo --users test.user1,admin --expiration 2030-12-31T12:00:00Z
```

### 生产环境使用

```bash
# 交互式模式
freeipa-password-reset --server ipa.company.com --username admin

# 批量模式
freeipa-password-reset --server ipa.company.com --username admin \
  --users john.doe,jane.smith --expiration 2030-12-31T12:00:00Z

# 仅列出用户信息
freeipa-password-reset --server ipa.company.com --username admin --list-only
```

### 高级用法

```bash
# 使用不同的日期格式
freeipa-password-reset --demo --users user1 --expiration "2030-12-31 12:00:00"
freeipa-password-reset --demo --users user1 --expiration "2030-12-31T12:00:00Z"

# 选择所有用户
freeipa-password-reset --demo --users all --expiration 2030-12-31T12:00:00Z

# 通过用户编号选择
freeipa-password-reset --demo --users 1,3,5 --expiration 2030-12-31T12:00:00Z
```

## 🔨 构建说明

### 前置要求

- Python 3.9+
- PyInstaller: `pip install pyinstaller`
- Docker（用于跨平台构建）

### 本地构建

```bash
# 克隆仓库
git clone https://github.com/your-username/MCP-Tools.git
cd MCP-Tools

# 为当前平台构建
./build-multiplatform.sh -c

# 构建特定平台（需要 Docker）
./build-multiplatform.sh -p linux-x86_64
./build-multiplatform.sh -p linux-arm64

# 构建所有 Linux 平台
./build-multiplatform.sh -a
```

### 使用 GitHub Actions

项目包含完整的 CI/CD 配置，支持自动构建：

```bash
# 创建发布标签触发构建
git tag v2.3.0
git push origin v2.3.0
```

### 手动构建

```bash
# 进入源码目录
cd L0

# 安装依赖
pip install pyinstaller

# 构建可执行文件
pyinstaller --onefile --name freeipa-password-reset freeipa_password_reset.py

# 可执行文件位于 dist/ 目录
```

## 👨‍💻 开发指南

### 项目结构

```
MCP-Tools/
├── L0/                          # 源代码目录
│   ├── freeipa_password_reset.py # 主程序
│   ├── test_password_reset.py    # 测试文件
│   └── *.spec                    # PyInstaller 配置
├── .github/workflows/           # GitHub Actions 配置
├── build-*.sh                   # 构建脚本
├── Dockerfile.*                 # Docker 构建配置
├── *-build/                     # 构建输出目录
└── README*.md                   # 文档文件
```

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/your-username/MCP-Tools.git
cd MCP-Tools

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
cd L0
python -m pytest test_password_reset.py -v
```

### 代码规范

- 使用 Python 3.9+ 语法
- 遵循 PEP 8 代码风格
- 添加类型注解
- 编写单元测试
- 更新文档

## 🔧 故障排除

### 常见问题

**GLIBC 版本错误**
```bash
# 检查系统 GLIBC 版本
ldd --version

# 本工具需要 GLIBC 2.3.4+（2003年发布）
# 如果版本过低，请升级系统或使用源码安装
```

**权限问题**
```bash
# 添加执行权限
chmod +x freeipa-password-reset

# 系统安装需要 sudo 权限
sudo cp freeipa-password-reset /usr/local/bin/
```

**架构兼容性**
```bash
# 检查系统架构
uname -m

# x86_64 系统使用 linux-x86_64 版本
# aarch64/arm64 系统使用 linux-arm64 版本
```

**PATH 环境变量**
```bash
# 检查 PATH 设置
echo $PATH

# 如果系统安装后仍无法找到命令，检查 /usr/local/bin 是否在 PATH 中
# 或使用完整路径运行
/usr/local/bin/freeipa-password-reset --help
```

### 网络问题

```bash
# 测试 FreeIPA 服务器连接
ping ipa.example.com

# 检查防火墙设置
# 确保可以访问 FreeIPA 服务器的 443 端口

# 使用演示模式进行离线测试
freeipa-password-reset --demo
```

### 获取帮助

如果遇到问题，请：

1. 查看 [Issues](https://github.com/your-username/MCP-Tools/issues) 页面
2. 搜索已知问题和解决方案
3. 提交新的 Issue，包含：
   - 操作系统和版本
   - 错误信息的完整输出
   - 复现步骤

## 🤝 贡献指南

我们欢迎各种形式的贡献！

### 如何贡献

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 提交 **Pull Request**

### 贡献类型

- 🐛 Bug 修复
- ✨ 新功能开发
- 📚 文档改进
- 🧪 测试用例
- 🌍 多语言支持
- 🚀 性能优化

### 开发指南

- 遵循现有代码风格
- 添加适当的测试
- 更新相关文档
- 确保所有测试通过

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [FreeIPA](https://www.freeipa.org/) 项目团队
- [PyInstaller](https://www.pyinstaller.org/) 开发者
- 所有贡献者和用户
</div>
