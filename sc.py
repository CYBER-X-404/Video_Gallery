import os
import textwrap
import urllib.request

# --- App Configuration (Updated with your new path) ---
APP_NAME = "Video Gallery"
PACKAGE_NAME = "com.video.gallery"
PROJECT_DIR = "/sdcard/App/Video_Gallery/"
GRADLE_WRAPPER_JAR_URL = "https://services.gradle.org/distributions/gradle-6.7.1-wrapper.jar"

# --- Helper Function to Create Files ---
def create_file(path, content, is_executable=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(textwrap.dedent(content) if not is_executable else content)
    if is_executable:
        os.chmod(path, 0o755)
    print(f"Created: {path}")

# --- Codemagic YAML Content ---
codemagic_yaml_content = """
workflows:
  android-app-build:
    name: Android App Build
    environment:
      java: 1.8
    scripts:
      - name: Set up local properties
        script: |
          echo "sdk.dir=$ANDROID_SDK_ROOT" > "$FCI_BUILD_DIR/local.properties"
      - name: Build debug APK with Gradle
        script: |
          cd $FCI_BUILD_DIR
          chmod +x ./gradlew
          ./gradlew assembleDebug
    artifacts:
      - app/build/outputs/apk/debug/*.apk
    publishing:
      email:
        recipients:
          - your-email@example.com
        notify:
          success: true
          failure: true
"""
# --- All other file contents (Same as before) ---
settings_gradle_content = 'rootProject.name = "{app_name}"\ninclude \':app\''
build_gradle_content = 'buildscript {{ repositories {{ google(); mavenCentral() }}; dependencies {{ classpath \'com.android.tools.build:gradle:4.2.2\' }} }}; allprojects {{ repositories {{ google(); mavenCentral() }} }}; task clean(type: Delete) {{ delete rootProject.buildDir }}'
gradle_properties_content = 'org.gradle.jvmargs=-Xmx2048m\nandroid.useAndroidX=true\nandroid.enableJetifier=true'
app_build_gradle_content = 'apply plugin: \'com.android.application\'\n\nandroid {{\n    compileSdkVersion 30\n    buildToolsVersion "30.0.3"\n\n    defaultConfig {{\n        applicationId "{package_name}"\n        minSdkVersion 21\n        targetSdkVersion 30\n        versionCode 1\n        versionName "1.0"\n    }}\n\n    buildTypes {{\n        release {{\n            minifyEnabled false\n            proguardFiles getDefaultProguardFile(\'proguard-android-optimize.txt\'), \'proguard-rules.pro\'\n        }}\n    }}\n    \n    sourceSets {{\n        main {{\n            java.srcDirs = [\'src/main/java\']\n            res.srcDirs = [\'src/main/res\']\n            assets.srcDirs = [\'src/main/assets\']\n        }}\n    }}\n    \n    compileOptions {{\n        sourceCompatibility 1.8\n        targetCompatibility 1.8\n    }}\n}}\n\ndependencies {{\n    implementation \'androidx.appcompat:appcompat:1.3.1\'\n    implementation \'com.google.android.material:material:1.4.0\'\n}}'
manifest_content = '<?xml version="1.0" encoding="utf-8"?>\n<manifest xmlns:android="http://schemas.android.com/apk/res/android"\n    package="{package_name}">\n    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />\n    <application\n        android:allowBackup="true"\n        android:icon="@mipmap/ic_launcher"\n        android:label="@string/app_name"\n        android:roundIcon="@mipmap/ic_launcher_round"\n        android:supportsRtl="true"\n        android:theme="@style/AppTheme">\n        <activity\n            android:name=".MainActivity"\n            android:exported="true">\n            <intent-filter>\n                <action android:name="android.intent.action.MAIN" />\n                <category android:name="android.intent.category.LAUNCHER" />\n            </intent-filter>\n        </activity>\n    </application>\n</manifest>'
main_activity_java_content = 'package {package_name};\n\nimport androidx.appcompat.app.AppCompatActivity;\nimport android.os.Bundle;\n\npublic class MainActivity extends AppCompatActivity {{\n    @Override\n    protected void onCreate(Bundle savedInstanceState) {{\n        super.onCreate(savedInstanceState);\n        setContentView(R.layout.main);\n    }}\n}}'
main_xml_content = '<?xml version="1.0" encoding="utf-8"?>\n<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"\n    android:layout_width="match_parent"\n    android:layout_height="match_parent"\n    android:orientation="vertical"\n    android:gravity="center">\n    <TextView\n        android:layout_width="wrap_content"\n        android:layout_height="wrap_content"\n        android:text="Hello, {app_name}!"\n        android:textSize="24sp"/>\n</LinearLayout>'
strings_xml_content = '<resources>\n    <string name="app_name">{app_name}</string>\n</resources>'
colors_xml_content = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="colorPrimary">#6200EE</color>\n    <color name="colorPrimaryDark">#3700B3</color>\n    <color name="colorAccent">#03DAC6</color>\n</resources>'
styles_xml_content = '<resources>\n    <style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">\n        <item name="colorPrimary">@color/colorPrimary</item>\n        <item name="colorPrimaryDark">@color/colorPrimaryDark</item>\n        <item name="colorAccent">@color/colorAccent</item>\n    </style>\n</resources>'
gradle_wrapper_properties_content = 'distributionBase=GRADLE_USER_HOME\ndistributionPath=wrapper/dists\nzipStoreBase=GRADLE_USER_HOME\nzipStorePath=wrapper/dists\ndistributionUrl=https\\://services.gradle.org/distributions/gradle-6.7.1-bin.zip'
gradlew_script_content = r'''#!/usr/bin/env sh
PRG="$0"; while [ -h "$PRG" ] ; do ls=`ls -ld "$PRG"`; link=`expr "$ls" : '.*-> \(.*\)$'`; if expr "$link" : '/.*' > /dev/null; then PRG="$link"; else PRG=`dirname "$PRG"`"/$link"; fi; done
SAVED="`pwd`"; cd "`dirname \"$PRG\"`/" >/dev/null; APP_HOME="`pwd -P`"; cd "$SAVED" >/dev/null
APP_NAME="Gradle"; APP_BASE_NAME=`basename "$0"`; DEFAULT_JVM_OPTS=""; MAX_FD="maximum"
warn () { echo "$*"; }; die () { echo; echo "$*"; echo; exit 1; }
cygwin=false; msys=false; darwin=false; nonstop=false; case "`uname`" in CYGWIN* ) cygwin=true;; Darwin* ) darwin=true;; MINGW* ) msys=true;; NONSTOP* ) nonstop=true;; esac
if [ -z "$JAVA_HOME" ] ; then if ${darwin} ; then [ -x '/usr/libexec/java_home' ] && export JAVA_HOME=`/usr/libexec/java_home`; elif [ -d "/usr/lib/jvm/java-11-openjdk-amd64" ] ; then export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"; elif [ -d "/usr/lib/jvm/java-8-openjdk-amd64" ] ; then export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"; fi; fi
if [ -n "$JAVA_HOME" ] ; then if [ -x "$JAVA_HOME/jre/sh/java" ] ; then JAVACMD="$JAVA_HOME/jre/sh/java"; else JAVACMD="$JAVA_HOME/bin/java"; fi; if [ ! -x "$JAVACMD" ] ; then die "ERROR: JAVA_HOME is set to an invalid directory: $JAVA_HOME"; fi; else JAVACMD="java"; which java >/dev/null 2>&1 || die "ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH."; fi
if ! ${cygwin} && ! ${darwin} && ! ${nonstop} ; then MAX_FD_LIMIT=`ulimit -H -n`; if [ $? -eq 0 ] ; then if [ "$MAX_FD" = "maximum" -o "$MAX_FD" = "max" ] ; then MAX_FD="$MAX_FD_LIMIT"; fi; ulimit -n $MAX_FD; if [ $? -ne 0 ] ; then warn "Could not set maximum file descriptor limit: $MAX_FD"; fi; else warn "Could not query maximum file descriptor limit: $MAX_FD_LIMIT"; fi; fi
CLASSPATH="$APP_HOME/gradle/wrapper/gradle-wrapper.jar"; exec "$JAVACMD" ${JAVA_OPTS} -classpath "$CLASSPATH" org.gradle.wrapper.GradleWrapperMain "$@"'''
gradlew_bat_script_content = r'@if "%DEBUG%"=="" @echo off; @if "%OS%"=="Windows_NT" setlocal; set DIRNAME=%~dp0; if "%DIRNAME%"=="" set DIRNAME=.; set APP_BASE_NAME=%~n0; set APP_HOME=%DIRNAME%; set DEFAULT_JVM_OPTS=; if defined JAVA_HOME goto findJavaFromJavaHome; set JAVA_EXE=java.exe; %JAVA_EXE% -version >NUL 2>&1; if "%ERRORLEVEL%"=="0" goto execute; echo ERROR: JAVA_HOME is not set and no ^'java^' command could be found in your PATH.; goto fail; :findJavaFromJavaHome; set JAVA_HOME=%JAVA_HOME:"=%; set JAVA_EXE=%JAVA_HOME%/bin/java.exe; if exist "%JAVA_EXE%" goto execute; echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%; goto fail; :execute; set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar; "%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% "-Dorg.gradle.appname=%APP_BASE_NAME%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*; :end; if "%ERRORLEVEL%"=="0" goto mainEnd; :fail; exit /b 1; :mainEnd; if "%OS%"=="Windows_NT" endlocal'

# --- Main Project Creation Logic ---
def create_project():
    print("--- Starting Android Project Generation ---")
    package_path = PACKAGE_NAME.replace('.', '/')
    java_dir = os.path.join(PROJECT_DIR, 'app/src/main/java', package_path)
    
    # Create all project text files
    create_file(os.path.join(PROJECT_DIR, 'settings.gradle'), settings_gradle_content.format(app_name=APP_NAME))
    create_file(os.path.join(PROJECT_DIR, 'build.gradle'), build_gradle_content)
    create_file(os.path.join(PROJECT_DIR, 'gradle.properties'), gradle_properties_content)
    create_file(os.path.join(PROJECT_DIR, 'app/build.gradle'), app_build_gradle_content.format(package_name=PACKAGE_NAME))
    create_file(os.path.join(PROJECT_DIR, 'app/proguard-rules.pro'), "# Proguard rules")
    create_file(os.path.join(PROJECT_DIR, 'app/src/main/AndroidManifest.xml'), manifest_content.format(package_name=PACKAGE_NAME))
    create_file(os.path.join(java_dir, 'MainActivity.java'), main_activity_java_content.format(package_name=PACKAGE_NAME))
    create_file(os.path.join(PROJECT_DIR, 'app/src/main/res/layout/main.xml'), main_xml_content.format(app_name=APP_NAME))
    create_file(os.path.join(PROJECT_DIR, 'app/src/main/res/values/strings.xml'), strings_xml_content.format(app_name=APP_NAME))
    create_file(os.path.join(PROJECT_DIR, 'app/src/main/res/values/colors.xml'), colors_xml_content)
    create_file(os.path.join(PROJECT_DIR, 'app/src/main/res/values/styles.xml'), styles_xml_content)
    create_file(os.path.join(PROJECT_DIR, 'gradlew'), gradlew_script_content, is_executable=True)
    create_file(os.path.join(PROJECT_DIR, 'gradlew.bat'), gradlew_bat_script_content)
    create_file(os.path.join(PROJECT_DIR, 'gradle/wrapper/gradle-wrapper.properties'), gradle_wrapper_properties_content)
    create_file(os.path.join(PROJECT_DIR, 'codemagic.yaml'), codemagic_yaml_content)
    os.makedirs(os.path.join(PROJECT_DIR, 'app/src/main/assets'), exist_ok=True)
    
    # --- Download the JAR file directly into the project ---
    jar_path = os.path.join(PROJECT_DIR, 'gradle/wrapper/gradle-wrapper.jar')
    print(f"\nDownloading gradle-wrapper.jar to {jar_path}...")
    try:
        urllib.request.urlretrieve(GRADLE_WRAPPER_JAR_URL, jar_path)
        print("Download complete.")
    except Exception as e:
        print(f"\n!!! FAILED TO DOWNLOAD JAR FILE: {e} !!!")
        print("!!! Please check your internet connection and run the script again. !!!")
        return

    print("\n--- Project Generation Complete! All files are ready. ---")
    print(f"Project created at: {PROJECT_DIR}")

if __name__ == "__main__":
    create_project()