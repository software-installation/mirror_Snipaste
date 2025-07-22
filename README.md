# Snipaste 安装包自动备份仓库

![GitHub Actions Status](https://img.shields.io/github/actions/workflow/status/software-installation/mirror_Snipaste/backup-snipaste.yml)
![Total Releases](https://img.shields.io/github/downloads/software-installation/mirror_Snipaste/total)

## 🔍 仓库说明

本仓库是 **Snipaste 软件**的安装包自动备份仓库，用于存档各版本的官方安装文件，方便用户在需要时获取历史版本。

👉 **核心定位**：
- 所有文件均为官方原始安装包，未做任何修改或二次打包
- 仅作为自动备份功能，不涉及软件开发、修改或功能更新
- 备份内容同步自 Snipaste 官方下载链接，确保与官方发布一致

## 📁 备份内容

仓库通过 GitHub Actions 自动备份以下平台的安装包：
- Windows (64位)：`Snipaste-<版本号>-x64.zip`
- Windows (32位)：`Snipaste-<版本号>-x86.zip`
- macOS：`Snipaste-<版本号>.dmg`
- Linux：`Snipaste-<版本号>-x86_64.AppImage`

所有文件均保存在对应版本的 Release 中，可通过右侧「Releases」入口查看下载。

## ⏰ 同步机制

- 每日凌晨自动检查官方最新版本，发现更新时自动创建对应版本的 Release 并上传文件
- 通过文件名提取版本号，避免重复备份相同版本
- 保留完整的版本历史，即使官方更新了最新版本，历史版本仍可在仓库中找到

## 📥 如何下载旧版本

1. 点击仓库右侧的「Releases」按钮
2. 在版本列表中选择需要的版本（格式为 `v<版本号>`）
3. 下载对应平台的安装包文件（如 Windows 64位 用户选择 `Snipaste-<版本号>-x64.zip`）

## 🔗 官方链接

- [Snipaste 官网](https://zh.snipaste.com/)
- 官方下载地址：
  - [Windows 64位](https://dl.snipaste.com/win-x64)
  - [Windows 32位](https://dl.snipaste.com/win-x86)
  - [macOS](https://dl.snipaste.com/mac)
  - [Linux](https://dl.snipaste.com/linux)

## 📝 免责声明

- 本仓库仅提供备份服务，软件的所有权利归原作者所有
- 备份文件的安全性与完整性以官方发布为准，建议重要场景下核对官方校验信息
- 若有侵权请联系仓库维护者删除
