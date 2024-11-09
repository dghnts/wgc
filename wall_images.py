import json
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# 背景画像のパスを取得する


def get_settings_path():
    windows_terminal_path = os.getenv("WINDOWSTERMINAL")

    if not windows_terminal_path:
        raise EnvironmentError("環境変数 WINDOWSTREMINAL が見つかりません")

    settings_path = os.path.join(windows_terminal_path, "settings.json")

    return settings_path


def get_background_images(settings_path):
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)

        profiles = settings.get("profiles", {}).get("list", [])
        defaults_image = settings.get("profiles", {}).get("defaults", []) \
            .get("backgroundImage", "None")
        background_images = {
                profile.get("name", "Unnamed"):
                profile.get("backgroundImage", defaults_image)
                for profile in profiles
        }
        return background_images
    except FileNotFoundError:
        print(f"設定ファイルが見つかりません: {settings_path}")
        return {}
    except json.JSONDecodeError:
        print("設定ファイルのJSON形式が正しくありません。")
        return {}


if __name__ == "__main__":
    try:
        settings_path = get_settings_path()
        print(settings_path)
        images = get_background_images(settings_path)
        for profile_name, image_path in images.items():
            print(f"Profile: {profile_name}, Background Image: {image_path}")
    except EnvironmentError as e:
        print(f"エラー: {e}")
