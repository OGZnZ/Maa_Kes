# How to Develop

Before starting development, please read the [Quick Started](https://maafw.com/docs/1.1-QuickStarted) chapter of the MaaFramework documentation to acquire a foundational understanding of the framework.

## Prerequisites

Developing with this guide assumes familiarity with MaaFramework conventions:

1. **Git version control**: Basic branching, commit, and push operations.
2. **GitHub and CI/CD workflows**: Understanding [GitHub Actions](https://docs.github.com/en/actions) for automated packaging and releases.
3. **MaaFramework Terminology**: Review the [Explanation of Terms](https://maafw.com/docs/1.2-ExplanationOfTerms) guide.

## Development Steps

0. Click `Use this template` > `Create a new repository` on GitHub to initialize your project.

1. Clone your repository:

    ```bash
    git clone https://github.com/MaaXYZ/MaaPracticeBoilerplate.git
    ```

2. Download the OCR recognition model archive [ppocr_v5.zip](https://download.maafw.xyz/MaaCommonAssets/OCR/ppocr_v5/ppocr_v5-zh_cn.zip) and extract it into `assets/resource/model/ocr/`:

    ```tree
    assets/resource/model/ocr/
    ├── det.onnx
    ├── keys.txt
    └── rec.onnx
    ```

    > [!WARNING]
    > Do not commit OCR model files into git. `.gitignore` already ignores `assets/resource/model/ocr/`, and GitHub Actions workflows configure them automatically during release builds.

3. Implement your automation logic. Consult the [MaaFramework Documentation](https://maafw.com/docs/1.1-QuickStarted), update resource files under `assets/` and `interface.json`, and debug using [MaaDebugger](https://maafw.com/docs/1.1-QuickStarted#debugging).

4. Commit and push your changes:

    ```bash
    git config user.name "Your Name"
    git config user.email "your.email@example.com"
    
    git add .
    git commit -m "feat: Add new daily feature"
    git push origin HEAD -u
    ```

5. Publish a release:

    Pushing a git tag triggers the automated build and release workflow in `.github/workflows/install.yml`:

    > [!NOTE]
    > Ensure repository permissions allow write access under `Settings` > `Actions` > `General` > `Workflow permissions` > `Read and write permissions`.

    ```bash
    git tag v1.0.0
    git push origin v1.0.0
    ```

    GitHub Actions will build artifacts and publish release assets automatically under your repository's Releases page.

## Frequently Asked Questions

See [FAQ](./faq.md).

## Advanced Configuration

See [Custom Configuration](./custom_configure.md).
