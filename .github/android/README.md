# Android APK Packaging

The `android` and `android_mirrorchyan` jobs in `install.yml` utilize
[Aliothmoon/MaaFwApp](https://github.com/Aliothmoon/MaaFwApp) (pinned ref) to package this repository's
PI into an Android APK, and upload the APK to MirrorChyan upon official releases.

## Package Name

```
applicationId = BASE_APPLICATION_ID + "." + pi-profile.yaml app.id
              = com.maafw.mq                + vero
              = com.maafw.mq.vero
```

- `patch_maafwapp.py` modifies `BASE_APPLICATION_ID` in MaaFwApp (upstream default is `com.aliothmoon.maafw`).
- In `pi-profile.yaml`, `app.id` is the suffix; only lowercase package segments (`[a-z][a-z0-9_]*`) are accepted. Uppercase characters and hyphens are rejected.

**Once released, the package name cannot be changed**, otherwise existing users must uninstall and reinstall. Additionally, debug and release builds share the same `applicationId` with different signatures, so installing a debug build prevents installing release updates without reinstalling. Always test with release builds after determining the package name.

## Repository Secrets

The `android` job requires all 4 of these secrets configured together (configuring only 1 to 3 will trigger `exit 1`; configuring none produces an unsigned debug build with `-debug` suffix):

| Secret | Description |
|:---|:---|
| `ANDROID_KEYSTORE_BASE64` | Base64-encoded keystore file, **must be a single line** |
| `ANDROID_KEYSTORE_PASSWORD` | Keystore password |
| `ANDROID_KEY_ALIAS` | Key alias |
| `ANDROID_KEY_PASSWORD` | Key password (under PKCS12, must match store password) |

The `android_mirrorchyan` job additionally reads `ANDROID_MIRRORCHYANUPLOADTOKEN` — note that this is a **separate** secret from `MirrorChyanUploadToken` used by the desktop `mirrorchyan_release.yml`.

### Current Keystore (Offline Backup: `D:\keys\Maa_KES\`)

| Property | Value |
|:---|:---|
| File | `maakes-release.jks` (4328 bytes, PKCS12) |
| Base64 | `maakes-release.jks.b64` (5772 chars, single line); mapped to `ANDROID_KEYSTORE_BASE64` |
| Alias | `maakes`; mapped to `ANDROID_KEY_ALIAS` |
| SHA-256 | `bf1e99cf902bcf7a9016cfaf75e67c0197880d1f9682001643aca91657a8d90a` |

In CI logs, the line `keystore: ... sha256: ...` validates against this hash: a mismatch indicates truncated or corrupted secret values (typically copy-paste truncation).

**Never replace this keystore once released**, as changing it forces all users to uninstall and reinstall. Store credentials in a password manager; `.jks` and `.b64` files must never be committed to git (blocked by `.gitignore`).

## MirrorChyan

| Location | Value |
|:---|:---|
| Workflow env `ANDROID_MIRRORCHYAN_RID` (top of `install.yml`) | `Maa_Kes_exec` |
| Desktop `assets/interface.json` `mirrorchyan_rid` | `MaaKes` (do not alter) |

Incorrect rid values (case mismatch or nonexistent backend rid) will cause upload failures.

MaaFwApp update checks read `mirrorchyan_rid` directly from `interface.json` inside the APK (passing `os=android` and device ABI) to retrieve download URLs. When using a separate Android rid, the build script uses `stage_pi_assets.py --rid` to patch `interface.json` inside the staged PI assets without altering the repository's root `interface.json`. Desktop builds remain unaffected.

## Local Verification (No CI Required)

```bash
# 1. Download and configure OCR models (assets/resource/model/ocr is gitignored)
python tools/configure.py

# 2. Assemble flat PI directory and patch interface.json version and rid
python tools/ci/stage_pi_assets.py --tag v1.2.3 --rid Maa_Kes_exec

# 3. Compute resource.hash (idempotent, identical results across runs)
python tools/ci/gen_resource_hash.py build-android/pi-assets/interface.json \
  --root build-android/pi-assets
```

To build the APK locally inside the MaaFwApp repository:

```bash
export PI_PROFILE=<repo_path>/build-android/pi-assets/../../.github/android/pi-profile.yaml
python scripts/setup_maa_framework.py --tag v5.12.3
./gradlew :app:assembleRelease      # or assembleDebug
```

Signing parameters are supplied via environment variables `KEYSTORE_PATH` / `KEYSTORE_PASSWORD` / `KEY_ALIAS` / `KEY_PASSWORD` (when `KEYSTORE_PATH` is empty, release builds remain unsigned without error); `local.properties` can also specify `pi.profile=`.

## Troubleshooting Guide

| Error | Root Cause |
|:---|:---|
| `KeytoolException: Failed to read key ... : null` + `Caused by: java.io.EOFException` | File is not a valid keystore or was truncated (base64 corrupted or text pasted). Keystore should be ~4 KB. |
| `keystore password was incorrect` / `Cannot recover key` | Incorrect keystore or key password. |
| `Alias <x> does not exist` | Incorrect alias name (preflight checks print all available aliases in keystore). |
| `app.id must be lowercase package segments` | `app.id` in `pi-profile.yaml` contains uppercase characters or hyphens. |
| `basename: missing operand` / `Input required and not supplied: path` | `Check upload token` step in `MirrorChyan/uploading-action` failed; verify token validity. |

## Other Packaging Pipelines

`tools/install.py` invokes `gen_resource_hash.py` at the end to compute `resource.hash`, which depends on `MaaFw` (`tools/requirements.txt`). This step is **optional with graceful fallback**: if `maa` cannot be imported (e.g., container lacks native dependencies), a warning is logged and packaging proceeds successfully. When adding new packaging pipelines with `MaaFw`, ensure native dependencies (`libatomic1`, `libstdc++6`, `libgomp1`) are installed.

Always call `sys.stdout.reconfigure(encoding="utf-8")` before printing unicode characters or emoji to prevent `UnicodeEncodeError` crashes on Windows consoles using legacy code pages.
