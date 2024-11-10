import json
import wall_images
import analysis_color
from convert_path import convert_path


def rgb_to_hex(rgb):
    # 色を16進数に変換
    # return "#{:02x}:{02x}{:02x}".format(rgb)
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def normalize_color(c):
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def calculate_relative_luminance(rgb):
    '''
    RGB値から相対輝度を計算
    '''
    r, g, b = [x / 255.0 for x in rgb]
    r = normalize_color(r)
    g = normalize_color(g)
    b = normalize_color(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def calculate_contrast_ratio(color1, color2):
    """
    2つの色のコントラスト比を計算
    """
    lum1 = calculate_relative_luminance(color1)
    lum2 = calculate_relative_luminance(color2)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.5) / (darker + 0.5)


def choose_contrasting_color(background_rgb, palette, threshold=4.5):
    """
    WACGに基づき，背景色に対してコントラスト比が閾値以上の色を選択
    """
    for color in palette:
        if calculate_contrast_ratio(background_rgb, color) >= threshold:
            return color
    # デフォルトで最初の色を返す（全て閾値未満の場合）
    return palette[1]


def generate_color_scheme(palette, schemename):
    """
    カラーパレットからカラースキームを生成
    """
    background = palette[0]  # 最も暗い色を背景色
    foreground = choose_contrasting_color(background, palette)

    return {
        "name": schemename,
        "background": rgb_to_hex(background),
        "foreground": rgb_to_hex(foreground),
        "black": rgb_to_hex(palette[0]),
        "red": rgb_to_hex(palette[2]),
        "green": rgb_to_hex(palette[3]),
        "yellow": rgb_to_hex(palette[4]),
        "blue": rgb_to_hex(palette[5]),
        "purple": rgb_to_hex(palette[6]),
        "cyan": rgb_to_hex(palette[7]),
        "white": rgb_to_hex(foreground),
        "brightBlack": rgb_to_hex(palette[0]),
        "brightRed": rgb_to_hex(palette[2]),
        "brightGreen": rgb_to_hex(palette[3]),
        "brightYellow": rgb_to_hex(palette[4]),
        "brightBlue": rgb_to_hex(palette[5]),
        "brightPurple": rgb_to_hex(palette[6]),
        "brightCyan": rgb_to_hex(palette[7]),
        "brightWhite": rgb_to_hex(foreground),
    }


def update_settings_f(settings_path, scheme, schemename):
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
            f.close()
        if "schemes" not in settings:
            settings["schemes"] = []
        # 既に登録済みのカラースキームを追加
        settings["schemes"] = [s for s in settings["schemes"]
                               if s["name"] != schemename]
        # 新しいカラースキームを追加
        settings["schemes"].append(scheme)

        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

        print("カラースキームが更新されました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    settings_path = wall_images.get_settings_path()
    image_paths = wall_images.get_background_images(settings_path)

    for profile_name, image_path in image_paths.items():
        image_path = convert_path(image_path)
        palette = analysis_color.extract_pallete(image_path)
        schemename = profile_name + "scheme"
        scheme = generate_color_scheme(palette, schemename)
        update_settings_f(settings_path, scheme, schemename)
    else:
        print(f"画像が見つかりません: {image_path}")
