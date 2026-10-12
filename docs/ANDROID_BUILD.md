# Android APK build
1. Open Actions -> Android APK -> Run workflow, or push a change to lib/.
2. Wait for build to finish, then download the artifact named SquashFrame-AI-V0.1-debug-apk.
3. Unzip the artifact and install app-debug.apk on the Huawei Mate X2.
4. This is a DEBUG build for testing, not a production-signed release.
5. Pose inference currently runs on a separate Python server; set its LAN address in the app.
6. The build workflow generates platform folders via flutter create and enables cleartext HTTP for local development only.
7. If Actions is disabled by repository policy, enable Actions under repository settings.
