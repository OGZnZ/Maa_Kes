# FAQ

## 0. I am new to Git. What is it, and where does that command-line window come from?

The terminal window is Git Bash. Modern software development fundamentally relies on Git. We recommend studying [Git tutorials](https://git-scm.com/book/en/v2) before proceeding with development.

## 1. I am new to Python. Running `python ./configure.py` or `python -m pip install MaaFW` has no response or output?

Windows 10/11 includes a placeholder "Python" alias that directs to the Microsoft Store rather than a functional Python environment.
Disable the app execution alias under Windows Settings > Apps > Advanced App Settings > App Execution Aliases, and install Python directly from [python.org](https://www.python.org/).

## 2. MaaDebugger or MaaPiCli displays an "Application Error: Unable to start correctly" popup

![Missing Runtime](https://github.com/user-attachments/assets/942df84b-f47d-4bb5-98b5-ab5d44bc7c2a)

Your system is likely missing the Microsoft Visual C++ Redistributable. Please install [vc_redist](https://aka.ms/vs/17/release/vc_redist.x64.exe).

## 3. How do I package my project?

Follow the recommended [Development Workflow](./how_to_develop.md) to push a release tag. The [CI workflow](/.github/workflows/install.yml) will automatically package and publish builds. For details, refer to the [GitHub Actions Documentation](https://docs.github.com/en/actions).

## 4. Why hasn't my issue in this template repository been answered?

This repository serves as a starter template, so maintainers monitor it less frequently than active upstream projects.
Please open issues in the appropriate upstream repository:

- MaaFW core and MaaPiCli issues: [MaaFramework/issues](https://github.com/MaaXYZ/MaaFramework/issues)
- MaaDebugger issues: [MaaDebugger/issues](https://github.com/MaaXYZ/MaaDebugger/issues)
- General discussions: [Discussions](https://github.com/MaaXYZ/MaaFramework/discussions)

## 5. OCR returns no results with errors "Failed to load det or rec" or "ocrer_ is null"

**Please read the setup instructions carefully.** You may have skipped downloading the OCR models (`ppocr_v5.zip`) into `assets/resource/model/ocr/`. Run `python tools/configure.py` or manually place the model files in place.

## 6. Where can I find help for other issues?

Join the [MaaFramework Developer Community](https://maafw.com/) to collaborate with other developers.

> [!WARNING]
> Before asking questions, read the [MaaFramework Documentation](https://maafw.com/docs/1.1-QuickStarted) and [How to Develop](./how_to_develop.md). When reporting issues, specify the exact steps, provide full error logs (`debug/maa.log`), and describe your configuration clearly.
