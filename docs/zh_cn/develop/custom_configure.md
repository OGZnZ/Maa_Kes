# Custom Configuration

## Table of Contents

- [Issue Templates](#issue-templates)
- [VSCode Extensions](#vscode-extensions)
- [Code Formatting Tools](#code-formatting-tools)

## Issue Templates

Good issue templates save communication time between maintainers and users, helping identify bugs and root causes faster.

Adapted from the [MAA](https://github.com/MaaAssistantArknights/MaaAssistantArknights) project template and tailored for `MaaFramework` workflows, a practical configuration is provided.

You can customize `.github/ISSUE_TEMPLATE/cn-bug-report.yaml` and `en-bug-report.yaml` by replacing `MXX` with your project name.

## VSCode Extensions <a id="vscode-extensions"></a>

Helpful extensions improve development efficiency significantly:

- [Maa Pipeline Support](https://marketplace.visualstudio.com/items?itemName=nekosu.maa-support) | MaaFramework extension providing pipeline debugging, screencaps, ROI selection, and color picking
- [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) | Markdown syntax and linting extension

## Code Formatting Tools

Code formatters enforce a unified style, improve readability, and lower long-term maintenance costs.

Currently enabled formatting tools:

| File Type | Formatter |
| --- | --- |
| JSON/YAML | [Prettier](https://prettier.io/) |
| Markdown | [MarkdownLint](https://github.com/DavidAnson/markdownlint-cli2) |

Additionally, `oxipng` is used for lossless PNG compression.

### Automated Formatting via Pre-commit Hooks

1. Ensure both Python and Node environments are installed on your machine.

2. Run the following commands in the project root directory:

    ```bash
    pip install pre-commit
    pre-commit install
    ```

If pre-commit fails to run after pip installation, verify that the pip binary directory is included in your system `PATH`.

Once configured, formatters will run automatically before each git commit to ensure code quality standards.

### Formatter Configurations

#### Oxipng

Configured in `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/shssoichiro/oxipng
  rev: v9.1.2
  hooks:
    - id: oxipng
      args: ["-q", "-o", "2", "-s", "--ng"]
```

[Parameter Documentation](https://github.com/shssoichiro/oxipng)

#### MarkdownLint

Configured in `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/DavidAnson/markdownlint-cli2
  rev: v0.13.0
  hooks:
    - id: markdownlint-cli2
      files: ^docs/.*|^README\.md$
      types:
        - markdown
      args: ["--fix", "--config", "docs/.markdownlint.yaml", "#**/node_modules"]
```

Configuration file: `docs/.markdownlint.yaml`, [Rule Details](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)

#### Prettier

Configured in `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/pre-commit/mirrors-prettier
  rev: v4.0.0-alpha.8
  hooks:
    - id: prettier
      types_or:
        - yaml
        - json
```

Configuration file: `.prettierrc.yaml`, [Options Documentation](https://prettier.io/docs/en/options.html)

The plugin "prettier-plugin-multiline-arrays" is used here to maintain multiline array formatting (removable if not needed), referenced in `package.json` and `package-lock.json`.
