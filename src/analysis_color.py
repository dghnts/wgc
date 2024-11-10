from colorthief import ColorThief
import os


def extract_pallete(image_path, color_count=8):
    # 背景画像から主要な色のパレットを抽出
    color_thief = ColorThief(image_path)
    palette = color_thief.get_palette(color_count=color_count)
    while len(palette) < color_count:
        palette.append((255, 255, 255))
    return palette


def display_pallete(pallete):
    # 抽出したカラーパレットの表示
    print("Extracted Color Pallete")
    for i, color in enumerate(pallete):
        print(f"Color{i+1}: RGB{color}")


if __name__ == "__main__":
    # サンプル画像のパス
    image_path = "/usr/share/backgrounds/Black_hole_by_Marek_Koteluk.jpg"
    if os.path.exists(image_path):
        pallete = extract_pallete(image_path)
        display_pallete(pallete)
    else:
        print(f"画像が見つかりません: {image_path}")
