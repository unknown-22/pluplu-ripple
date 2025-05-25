import cv2
import numpy as np
from PIL import Image
import tempfile
import os


def jitter_line(img_rgba, amplitude_percent, sigma, frames, fps, seed, bg_color="#FFFFFF"):
    """
    Line Boil Effectを適用してアニメーションGIFを生成する
    
    Args:
        img_rgba: PIL Image (RGBA形式)
        amplitude_percent: 変位の振幅（画像幅に対する%）
        sigma: ガウシアンブラーのσ値
        frames: フレーム数
        fps: フレームレート
        seed: 乱数シード (0の場合はランダム)
        bg_color: 背景色 (透過PNG用)
    
    Returns:
        生成されたGIFファイルのパス
    """
    # PIL ImageをOpenCV形式に変換
    img_array = np.array(img_rgba)
    
    # RGBAでない場合はRGBAに変換
    if img_array.shape[2] == 3:
        # RGBの場合、アルファチャンネルを追加
        alpha = np.ones((img_array.shape[0], img_array.shape[1], 1), dtype=img_array.dtype) * 255
        img_array = np.concatenate([img_array, alpha], axis=2)
    
    h, w = img_array.shape[:2]
    
    # 割合からピクセル値に変換
    amplitude = w * amplitude_percent / 100.0
    
    base_x, base_y = np.meshgrid(np.arange(w), np.arange(h))
    
    # 乱数生成器の初期化
    rng = np.random.default_rng(seed if seed != 0 else None)
    
    outputs = []
    
    for _ in range(frames):
        # ノイズ生成 (-1 から 1 の範囲)
        noise_x = (rng.random((h, w)) * 2 - 1).astype(np.float32)
        noise_y = (rng.random((h, w)) * 2 - 1).astype(np.float32)
        
        # ガウシアンブラーで滑らかに
        dx = cv2.GaussianBlur(noise_x, (0, 0), sigma) * amplitude
        dy = cv2.GaussianBlur(noise_y, (0, 0), sigma) * amplitude
        
        # 変位マップを作成
        map_x = (base_x + dx).astype(np.float32)
        map_y = (base_y + dy).astype(np.float32)
        
        # リマッピング実行
        warped = cv2.remap(img_array, map_x, map_y, cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
        
        # OpenCV形式からPIL Imageに変換
        warped_pil = Image.fromarray(warped, 'RGBA')
        
        # 背景色の合成（透過部分がある場合）
        if bg_color != "#FFFFFF" or True:  # 常に背景合成を行う
            bg = Image.new('RGB', warped_pil.size, bg_color)
            composite = Image.alpha_composite(
                Image.new('RGBA', warped_pil.size, bg_color + 'FF'),
                warped_pil
            ).convert('RGB')
            outputs.append(composite)
        else:
            outputs.append(warped_pil.convert('RGB'))
    
    # 一時ファイルに保存
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, f"pluplu_ripple_{hash(str(seed))}.gif")
    
    # フレーム継続時間を計算
    duration_ms = int(1000 / fps)
    
    # GIFとして保存
    outputs[0].save(
        output_path,
        save_all=True,
        append_images=outputs[1:],
        duration=duration_ms,
        loop=0,
        disposal=2,
        optimize=False
    )
    
    return output_path


def process_image(image, seed, amplitude_percent, sigma, frames, fps, bg_color):
    """
    Gradio用の画像処理ラッパー関数
    """
    if image is None:
        return None
    
    # PIL Imageに変換
    if isinstance(image, np.ndarray):
        pil_image = Image.fromarray(image)
    else:
        pil_image = image
    
    # RGBAに変換
    if pil_image.mode != 'RGBA':
        pil_image = pil_image.convert('RGBA')
    
    # Line Boil Effectを適用
    result_path = jitter_line(
        pil_image, 
        amplitude_percent, 
        sigma, 
        frames, 
        fps, 
        seed, 
        bg_color
    )
    
    return result_path