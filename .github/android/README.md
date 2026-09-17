# Android APK 打包

`install.yml` 的 `android` / `android_mirrorchyan` 两个 job 用
[Aliothmoon/MaaFwApp](https://github.com/Aliothmoon/MaaFwApp)（固定 ref）把本仓库的 PI
打成 APK，并在正式发版时把 APK 传到 MirrorChyan。

## 包名

```
applicationId = BASE_APPLICATION_ID + "." + pi-profile.yaml 的 app.id
              = com.maafw.mq                + vero
              = com.maafw.mq.vero
```

- `patch_maafwapp.py` 改 MaaFwApp 里的 `BASE_APPLICATION_ID`（上游是 `com.aliothmoon.maafw`）；
- `pi-profile.yaml` 的 `app.id` 是后缀，只收小写包段（`[a-z][a-z0-9_]*`），大写和连字符会被拒绝。

**包名一旦发过版就不能再改**，改了老用户只能卸载重装。另外 debug 与 release 的
`applicationId` 相同、只有签名不同，所以先装了 debug 包之后 release 包装不上，
必须卸载重装 —— 定好包名后就一直用 release 包测。

## Repository secrets

`android` job 读这 4 个，**必须四个一起配**（只配 1~3 个会直接 `exit 1`；一个都不配则出
debug 签名包，产物名带 `-debug`）：

| Secret | 内容 |
|:---|:---|
| `ANDROID_KEYSTORE_BASE64` | keystore 文件的 base64，**必须单行** |
| `ANDROID_KEYSTORE_PASSWORD` | store password |
| `ANDROID_KEY_ALIAS` | 别名 |
| `ANDROID_KEY_PASSWORD` | key password（PKCS12 下必须与 store 相同） |

`android_mirrorchyan` job 另外读 `ANDROID_MIRRORCHYANUPLOADTOKEN` —— 注意这是**另一个**
secret，和桌面端 `mirrorchyan_release.yml` 用的 `MirrorChyanUploadToken` 不是同一个。

### 当前密钥库（离线备份：`D:\keys\Maa_KES\`）

| 项 | 值 |
|:---|:---|
| 文件 | `maakes-release.jks`（4328 bytes，PKCS12） |
| base64 | `maakes-release.jks.b64`（5772 chars，单行）；即 `ANDROID_KEYSTORE_BASE64` |
| 别名 | `maakes`；即 `ANDROID_KEY_ALIAS` |
| sha256 | `bf1e99cf902bcf7a9016cfaf75e67c0197880d1f9682001643aca91657a8d90a` |

CI 日志里那行 `keystore: ... sha256: ...` 就是拿这个值对：对不上说明 secret 里的字节
和本地文件不一致（多半是抄写截断）。

**这个 keystore 一旦发过版就永远不能换**，换了老用户必须卸载重装。密码存在密码管理器里，
`.jks` / `.b64` 不进仓库（已在 `.gitignore` 里挡掉 `*.jks` / `*.jks.b64` / `*.keystore`）。

## MirrorChyan

| 位置 | 值 |
|:---|:---|
| workflow env `ANDROID_MIRRORCHYAN_RID`（`install.yml` 顶部，全流程只有这一处） | `Maa_Kes_exec` |
| 桌面端 `assets/interface.json` 的 `mirrorchyan_rid` | `MaaKes`（不动） |

rid 写错（大小写不匹配、或后台没有这个 rid）上传必失败。

MaaFwApp 的更新检查不是从 workflow 读 rid，而是从 APK 内 `interface.json` 的
`mirrorchyan_rid` 读，并且固定带 `os=android` + 设备 ABI，要求返回 APK 链接。
所以 Android 用独立 rid 时，打包时要用 `stage_pi_assets.py --rid` 把 APK 里那份
`interface.json` 一起改掉，否则 app 会去查桌面那个 rid、拿不到 android 资源
（会回退 GitHub 源，但吃不到 CDN）。桌面端不受影响。

## 本地验证（不用等 CI）

```bash
# 1. 铺 OCR 模型（assets/resource/model/ocr 没进 git）
python tools/configure.py

# 2. 组装扁平 PI 目录，并改掉里面那份 interface.json 的版本和 rid
python tools/ci/stage_pi_assets.py --tag v1.2.3 --rid Maa_Kes_exec

# 3. 算 resource.hash（幂等，跑两次结果一致）
python tools/ci/gen_resource_hash.py build-android/pi-assets/interface.json \
  --root build-android/pi-assets
```

要真出包就在 MaaFwApp 仓库里：

```bash
export PI_PROFILE=<本仓库>/build-android/pi-assets/../../.github/android/pi-profile.yaml
python scripts/setup_maa_framework.py --tag v5.12.3
./gradlew :app:assembleRelease      # 或 assembleDebug
```

签名走环境变量 `KEYSTORE_PATH` / `KEYSTORE_PASSWORD` / `KEY_ALIAS` / `KEY_PASSWORD`
（`KEYSTORE_PATH` 为空时 release 是 unsigned，不报错）；`local.properties` 写
`pi.profile=` 也能指配方。

## 排错对照表

| 报错 | 原因 |
|:---|:---|
| `KeytoolException: Failed to read key ... : null` + `Caused by: java.io.EOFException` | 文件不是密钥库 / 被截断（base64 传错、二次编码、误传文本文件）。keystore 应该 4KB 上下，别把密码文本存成 `.jks` |
| `keystore password was incorrect` / `Cannot recover key` | 密码错 |
| `Alias <x> does not exist` | 别名错（预检会打印 keystore 里实际的别名列表） |
| `app.id must be lowercase package segments` | `pi-profile.yaml` 的 `app.id` 有大写或连字符 |
| `basename: missing operand` / `Input required and not supplied: path` | `MirrorChyan/uploading-action` 的 `Check upload token` 先失败了，后面两步是连带的，根因是 upload token |

## 其他打包路径

`tools/install.py` 结尾会调 `gen_resource_hash.py` 算 `resource.hash`，这一步依赖 `MaaFw`
（见 `tools/requirements.txt`）。它是**可选 + 容错**的：import 不到 `maa`（例如容器里没有
native 运行库）就打一行警告跳过，不会让打包整体失败。新增打包路径时如果要装 `MaaFw`，
记得补齐它的 native 依赖（`libatomic1` / `libstdc++6` / `libgomp1` 之类）。

另外 `print` 中文/emoji 之前一定要先 `sys.stdout.reconfigure(encoding="utf-8")`：
Windows 控制台默认 cp1252/GBK，否则「优雅降级」的分支自己会抛 `UnicodeEncodeError`
把 exit code 变成 1。
