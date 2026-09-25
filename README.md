<!-- markdownlint-disable MD033 MD041 MD022 MD032 MD003 MD026 MD009 -->

> **⚠️ Beta Stage — Features are actively under development and continuously improving!**

<p align="center">
  <img alt="LOGO" src="assets/resource/image/logo.png" width="256" height="256" />
</p>

<div align="center">

# NIG-Kes

</div>

<div align="center">

*Chaos Zero Nightmare* automation assistant based on MaaFramework. Computer vision + simulated control to free your hands! Powered by [MaaFramework](https://github.com/MaaXYZ/MaaFramework)!

[Click to join the QQ group (Maa_Kes Community)](https://qm.qq.com/q/QbBRzgyUU2) — Group ID: 437587416

</div>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">
  <img alt="license" src="https://img.shields.io/github/license/miaojiuqing/Maa_KES">
  <img alt="platform" src="https://img.shields.io/badge/platform-Windows%7CAndroid-blueviolet">
  <img alt="commit" src="https://img.shields.io/github/commit-activity/m/miaojiuqing/Maa_KES">
  <img alt="stars" src="https://img.shields.io/github/stars/miaojiuqing/Maa_KES">
   <a href="https://mirrorchyan.com/zh/projects?rid=MaaKes" target="_blank"><img alt="mirrorc" src="https://img.shields.io/badge/Mirror%E9%85%B1-%239af3f6?logo=countingworkspro&logoColor=4f46e5"></a>
</p>

---

## Introduction

**NIG-Kes** is an automation tool developed by miaojiuqing based on the MaaFramework, dedicated to helping players automate daily tasks, stamina clearance, reward claiming, and other repetitive operations in *Chaos Zero Nightmare*.

> **MaaFramework** is a next-generation automated black-box testing framework based on computer vision technologies, incorporating accumulated experience from [MAA](https://github.com/MaaAssistantArknights/MaaAssistantArknights) in a complete rewrite.
> It combines low-code simplicity with high extensibility, providing a rich, practical open-source library that empowers developers to build better black-box testing solutions.

**Note:** MuMu Emulator and LDPlayer are recommended. The PC desktop client is also supported. Please set the display resolution to 16:9.

---

## Key Features

### Game Launch
- ✅ Launch game and enter the main lobby
- ✅ Support auto-launching emulator instances

### Daily Operations

#### ☕ Coffee Break
- ✅ One-click completion of coffee shop daily

#### ⚔️ Stamina Clearance — Super-Spacetime Basin
- ✅ **Growth Materials** — Unit coins / Main combatant upgrade materials / Support combatant upgrade materials
- ✅ **Main Combatants** — Striker / Guardian / Ranger / Hunter / Arcanist / Controller
- ✅ **Support Combatants** — Striker / Guardian / Ranger / Hunter / Arcanist / Controller
- ✅ **Potential Attributes** — Passion / Order / Instinct / Void / Justice
- ✅ **Memory Fragments** — Prelude and Dreams / Desire and Dominance / Flame and Orbs / Status and Tracks / Glory and Authority / Cycle and Destiny / Greed and Obsession / Scarab and Promise / Remains and Tools
- ✅ **Weekly Boss Challenge** — The Wailing Prodigal / Face the Fear
- ✅ Battle efficiency selection (1 to 5 runs)
- ✅ Auto-challenge until stamina is exhausted

#### ❤️‍🩹 Healing Center
- ✅ Automatically handles healing notifications
- ✅ Selectable treatment plans: Memory Erasure / Counseling / Do Not Treat

#### ❤️ Spend Time Together
- ✅ Automatic invitations; terminates automatically when travel tickets are exhausted
- ✅ District selection: Central District / Academy / Resort / Administrative District
- ✅ Custom character priority list (up to 5 priorities)
- ✅ Character filtering by attribute (Passion / Justice / Order / Instinct / Void)
- ✅ Assign specific character as dating target

#### 📋 Policy Review
- ✅ Approval rewards (including Post-disaster Reconstruction, Dreamcatcher, Sincere Handwritten Letter, etc.)
  - ⚠️ Affection item recognition is in progress; currently supported items:
    <details><summary>Expand to view supported item list</summary>
    Recognition templates located at: `assets/resource/image/日常/政策审阅/政策特殊奖励/好感度道具/`
    </details>
- ✅ Post-disaster Reconstruction plans (customizable reward priorities)

#### 🎁 Claim Rewards
- ✅ Daily activity rewards
- ✅ Archianon supply
- ✅ Mailbox items
- ✅ Mayor Chessboard (5 daily dice rolls)

#### ⚔️ Sortie (Under Development)
- 🚧 Star Wanderer / Difficulty selection / Hardcore mode
- 🚧 Character filtering (Attribute / Class / Faction)
- 🚧 Starting character presets / Combat strategies

### Standalone Tools

#### 💬 Read Messages / Clear Notifications
- ✅ Automatically reads messages and clears red dot indicators
- ✅ Automatically advances affection story dialogues
- ✅ Optional dialogue fast-forwarding

#### 📖 Auto Skip Story
- ✅ Automatically skips story dialogues with skip confirmation handling

#### 🗺️ Auto Progression
- ✅ Automatically pushes main story / combat stages
- ✅ Automatically handles story dialogues

#### 🔴 Clear Academy Red Dots
- ✅ Automatically clears tutorial and academy red dot badges

#### ⚔️ Auto Battle
- ✅ Automatically executes combat turns
- ✅ Supports automatic casting of ready EGO skills

#### 🎮 Interactive Helper
- ✅ Automatically detects and taps specified interface buttons
- ✅ Supports Continue Challenge confirmation dialogs

#### 🃏 Chaos Exploration
- ✅ Roguelike mode automatic pathfinding and stage progression

#### ♻️ Chaos Reroll
- ✅ Rerolls for designated starting cards
- ✅ Rerolls for designated starting oracles / speech cards

---

## Instructions for Use

### ADB (Android Emulator)

After starting the software, select "Android" in the top-left resource selector, configure the emulator resolution to 16:9, and run in the background.

### Win32 (Desktop PC)

- Run the application **as Administrator**
- Select "Desktop" in the top-left resource selector
- Set in-game window resolution to 16:9
- Recommended mouse/keyboard input method: `PostMessageWithCursorPos` or `SendMessageWithCursorPos` for background interaction

---

## Frequently Asked Questions (FAQ)

**Q: What should I do if "Resource loading failed" appears on startup?**

A: Open the installation directory, delete all folders except `config`, download the latest release and extract it into the installation directory, then restart.

> [!CAUTION]
> **Q: What should I do if the PC desktop client fails to connect to the game window?**
> 
> A: Run as Administrator. If connection still fails when run as Administrator, try changing the capture method under "Runtime Settings - Screencap Method".

**Q: What if the application throws "Application Error"?**

A: This usually indicates missing runtime libraries. Please install the Microsoft Visual C++ redistributable: [vc_redist](https://aka.ms/vs/17/release/vc_redist.x64.exe).

**Q: How do I export diagnostic logs?**

A: Click "|→" in the application to export logs. If a bug is reliably reproducible, delete the `debug` folder before reproducing the bug and exporting logs.

---

## Disclaimer

This software is free and open-source, intended solely for personal learning and exchange. The authors and maintainers are not responsible for any fees, damages, or consequences arising from unauthorized third-party commercial use.

The development team assumes no liability for account issues resulting from software defects, text misunderstandings, or abnormal operations. Please read instructions carefully and use responsibly!

---

## Utility Tools

1. [MaaDebugger](https://github.com/MaaXYZ/MaaDebugger) — Debug pipeline JSON execution nodes
2. ~~[MFATools](https://github.com/SweetSmellFox/MFATools)~~ — Legacy screenshot and color picker utility
3. [MFAToolsPlus](https://github.com/SweetSmellFox/MFAToolsPlus) — Screenshot, color picker, and ROI selector

## Related Projects

1. [MaaFramework](https://github.com/MaaXYZ/MaaFramework) — Next-generation automated black-box testing framework
2. [MaaPracticeBoilerplate](https://github.com/MaaXYZ/MaaPracticeBoilerplate) — MaaFramework project boilerplate
3. [MFAAvalonia](https://github.com/SweetSmellFox/MFAAvalonia) — Community graphical user interface

## Acknowledgments

This project is proudly powered by **[MaaFramework](https://github.com/MaaXYZ/MaaFramework)**!

Special thanks to all contributors who have helped build this project:

<a href="https://github.com/miaojiuqing/Maa_KES/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=miaojiuqing/Maa_KES&max=1000" alt="Contributors"/>
</a>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=miaojiuqing/Maa_KES&type=date)](https://www.star-history.com/#miaojiuqing/Maa_KES&type=date)
