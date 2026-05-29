<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen.svg" alt="Status">
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> |
  <a href="#繁體中文">繁體中文</a> |
  <a href="#english">English</a>
</p>

---

# 简体中文

<div align="center">
  <h1>🔍 RegexMaster</h1>
  <p><strong>终端正则表达式测试与调试利器</strong></p>
  <p>AI智能解释 · 可视化分析 · 性能优化 · 代码生成</p>
</div>

## 🎉 项目介绍

**RegexMaster** 是一款专为开发者打造的终端正则表达式工具，让你无需离开终端即可高效测试、调试和优化正则表达式。

### ✨ 核心特性

- 🔍 **实时匹配测试** - 输入即匹配，实时高亮显示结果
- 🤖 **AI智能解释** - 将复杂正则转换为自然语言说明
- 📊 **可视化分析** - AST树状图展示，直观理解模式结构
- ⚡ **性能优化** - 检测灾难性回溯，提供优化建议
- 🛠️ **代码生成** - 一键生成 Python/JS/Go/Java 代码
- 📚 **学习模式** - 交互式教程，从入门到精通
- 🎨 **精美TUI** - 基于 Textual 的现代化终端界面

### 🚀 快速开始

#### 环境要求
- Python 3.10 或更高版本
- pip 包管理器

#### 安装

```bash
# 使用 pip 安装
pip install regexmaster

# 或使用简短命令
pip install rxm
```

#### 运行

```bash
# 启动交互式TUI
regexmaster

# 或使用简写
rxm

# 快速测试
regexmaster test '\d+' -t 'abc123def'

# 解释模式
regexmaster explain '\d{3}-\d{3}-\d{4}'

# 生成代码
regexmaster generate '\w+@[\w.]+' -l python
```

### 📖 详细使用指南

#### 交互式模式

启动TUI后，你可以：
1. 在 **Pattern** 输入框输入正则表达式
2. 在 **Test Text** 区域输入测试文本
3. 实时查看匹配结果

#### 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+E` | 解释当前模式 |
| `Ctrl+G` | 生成代码 |
| `Ctrl+O` | 性能优化分析 |
| `Ctrl+L` | 清空输入 |
| `Ctrl+Q` | 退出程序 |
| `F1` | 帮助 |

#### 命令行模式

```bash
# 测试匹配
regexmaster test 'pattern' -t 'test text'

# 解释模式
regexmaster explain 'pattern'

# 性能分析
regexmaster optimize 'pattern' -t 'test text'

# 代码生成
regexmaster generate 'pattern' -l python
```

### 💡 设计思路

RegexMaster 的设计理念是 **简单、高效、智能**：

1. **简单** - 一条命令即可安装，无需复杂配置
2. **高效** - 实时匹配，零延迟反馈
3. **智能** - AI辅助解释，降低学习曲线

### 📦 打包与部署

```bash
# 克隆仓库
git clone https://github.com/gitstq/regexmaster.git
cd regexmaster

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 构建分发包
pip install build
python -m build
```

### 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

# 繁體中文

<div align="center">
  <h1>🔍 RegexMaster</h1>
  <p><strong>終端正則表達式測試與調試利器</strong></p>
  <p>AI智能解釋 · 可視化分析 · 性能優化 · 代碼生成</p>
</div>

## 🎉 項目介紹

**RegexMaster** 是一款專為開發者打造的終端正則表達式工具，讓你無需離開終端即可高效測試、調試和優化正則表達式。

### ✨ 核心特性

- 🔍 **實時匹配測試** - 輸入即匹配，實時高亮顯示結果
- 🤖 **AI智能解釋** - 將複雜正則轉換為自然語言說明
- 📊 **可視化分析** - AST樹狀圖展示，直觀理解模式結構
- ⚡ **性能優化** - 檢測災難性回溯，提供優化建議
- 🛠️ **代碼生成** - 一鍵生成 Python/JS/Go/Java 代碼
- 📚 **學習模式** - 交互式教程，從入門到精通
- 🎨 **精美TUI** - 基於 Textual 的現代化終端界面

### 🚀 快速開始

#### 環境要求
- Python 3.10 或更高版本
- pip 包管理器

#### 安裝

```bash
# 使用 pip 安裝
pip install regexmaster

# 或使用簡短命令
pip install rxm
```

#### 運行

```bash
# 啟動交互式TUI
regexmaster

# 或使用簡寫
rxm

# 快速測試
regexmaster test '\d+' -t 'abc123def'

# 解釋模式
regexmaster explain '\d{3}-\d{3}-\d{4}'

# 生成代碼
regexmaster generate '\w+@[\w.]+' -l python
```

### 📖 詳細使用指南

#### 交互式模式

啟動TUI後，你可以：
1. 在 **Pattern** 輸入框輸入正則表達式
2. 在 **Test Text** 區域輸入測試文本
3. 實時查看匹配結果

#### 快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl+E` | 解釋當前模式 |
| `Ctrl+G` | 生成代碼 |
| `Ctrl+O` | 性能優化分析 |
| `Ctrl+L` | 清空輸入 |
| `Ctrl+Q` | 退出程序 |
| `F1` | 幫助 |

### 📦 打包與部署

```bash
# 克隆倉庫
git clone https://github.com/gitstq/regexmaster.git
cd regexmaster

# 安裝開發依賴
pip install -e ".[dev]"

# 運行測試
pytest tests/

# 構建分發包
pip install build
python -m build
```

### 🤝 貢獻指南

歡迎貢獻代碼、報告問題或提出建議！

### 📄 開源協議

本項目採用 MIT 協議開源 - 詳見 [LICENSE](LICENSE) 文件。

---

# English

<div align="center">
  <h1>🔍 RegexMaster</h1>
  <p><strong>Terminal Regex Testing & Debugging Powerhouse</strong></p>
  <p>AI-Powered Explanations · Visual Analysis · Performance Optimization · Code Generation</p>
</div>

## 🎉 Introduction

**RegexMaster** is a terminal-based regex tool designed for developers who want to test, debug, and optimize regular expressions without leaving the command line.

### ✨ Key Features

- 🔍 **Real-time Matching** - Instant pattern matching with highlighted results
- 🤖 **AI Explanations** - Convert complex patterns to plain English
- 📊 **Visual Analysis** - AST tree visualization for pattern structure
- ⚡ **Performance Optimization** - Detect catastrophic backtracking, get optimization tips
- 🛠️ **Code Generation** - Generate Python/JS/Go/Java code instantly
- 📚 **Learning Mode** - Interactive tutorials from beginner to expert
- 🎨 **Beautiful TUI** - Modern terminal interface powered by Textual

### 🚀 Quick Start

#### Requirements
- Python 3.10 or higher
- pip package manager

#### Installation

```bash
# Install with pip
pip install regexmaster

# Or use the short name
pip install rxm
```

#### Usage

```bash
# Launch interactive TUI
regexmaster

# Or use the alias
rxm

# Quick test
regexmaster test '\d+' -t 'abc123def'

# Explain mode
regexmaster explain '\d{3}-\d{3}-\d{4}'

# Generate code
regexmaster generate '\w+@[\w.]+' -l python
```

### 📖 Detailed Usage

#### Interactive Mode

After launching the TUI:
1. Enter your regex pattern in the **Pattern** input
2. Type test text in the **Test Text** area
3. View real-time match results

#### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+E` | Explain current pattern |
| `Ctrl+G` | Generate code |
| `Ctrl+O` | Performance analysis |
| `Ctrl+L` | Clear inputs |
| `Ctrl+Q` | Quit |
| `F1` | Help |

#### CLI Mode

```bash
# Test matching
regexmaster test 'pattern' -t 'test text'

# Explain pattern
regexmaster explain 'pattern'

# Performance analysis
regexmaster optimize 'pattern' -t 'test text'

# Generate code
regexmaster generate 'pattern' -l python
```

### 💡 Design Philosophy

RegexMaster is designed to be **Simple, Fast, and Smart**:

1. **Simple** - One command to install, zero configuration
2. **Fast** - Real-time matching with instant feedback
3. **Smart** - AI-assisted explanations to reduce learning curve

### 📦 Building & Deployment

```bash
# Clone the repository
git clone https://github.com/gitstq/regexmaster.git
cd regexmaster

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Build distribution
pip install build
python -m build
```

### 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">SOLO Agent</a>
</p>
