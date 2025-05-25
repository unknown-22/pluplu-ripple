import gradio as gr
from core import process_image


def create_interface():
    """Gradio UIを作成する"""
    
    with gr.Blocks(title="PluPlu Ripple - Line Boil Effect", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🌊 PluPlu Ripple
            **線画にLine Boil Effectを適用してアニメーション化**
            
            画像をアップロードし、パラメータを調整してプレビューボタンを押してください。
            """
        )
        
        with gr.Row():
            # 左側：入力画像・パラメータ調整
            with gr.Column(scale=1):
                input_image = gr.Image(
                    label="📥 画像入力",
                    type="pil",
                    height=400
                )
                # パラメータ調整
                with gr.Group():
                    gr.Markdown("### 🎛️ パラメータ調整")
                    
                    seed = gr.Slider(
                        label="🔀 Seed",
                        minimum=0,
                        maximum=9999,
                        value=0,
                        step=1,
                        info="0 = 毎回ランダム"
                    )
                    
                    amplitude = gr.Slider(
                        label="↔ Amplitude (%)",
                        minimum=0,
                        maximum=10,
                        value=3,
                        step=0.1,
                        info="最大変位量（画像幅に対する割合）"
                    )
                    
                    sigma = gr.Slider(
                        label="🌫️ Smooth σ",
                        minimum=1,
                        maximum=15,
                        value=5,
                        step=1,
                        info="ガウシアンブラーのカーネルσ"
                    )
                    
                    frames = gr.Slider(
                        label="🔄 Frames",
                        minimum=2,
                        maximum=24,
                        value=8,
                        step=1,
                        info="ループ枚数"
                    )
                    
                    fps = gr.Slider(
                        label="🎞️ FPS",
                        minimum=6,
                        maximum=30,
                        value=12,
                        step=1,
                        info="再生速度"
                    )
                    
                    bg_color = gr.ColorPicker(
                        label="🎨 背景色",
                        value="#FFFFFF",
                        info="透過PNG用合成色"
                    )

            # 右側：出力
            with gr.Column(scale=1):
                # 出力結果
                output_image = gr.Image(
                    label="📱 アニメーションプレビュー",
                    height=400
                )
                # プレビューボタン
                preview_btn = gr.Button(
                    "👁️‍🗨️ プレビュー生成", 
                    variant="primary",
                    size="lg"
                )

        # イベントハンドラー
        preview_btn.click(
            fn=process_image,
            inputs=[
                input_image,
                seed, 
                amplitude, 
                sigma, 
                frames, 
                fps, 
                bg_color
            ],
            outputs=output_image,
            show_progress=True
        )
        
        # 使用方法の説明
        with gr.Accordion("📖 使用方法", open=False):
            gr.Markdown(
                """
                1. **画像をアップロード**: PNG、JPEG対応（透過PNG推奨）
                2. **パラメータ調整**: 
                   - **Seed**: 0で毎回異なる揺れ、固定値で再現可能
                   - **Amplitude**: 揺れの強さ（画像幅に対する%、3%程度が自然）
                   - **Smooth σ**: 揺れの滑らかさ（5-10が推奨）
                   - **Frames**: フレーム数（8-16が軽量）
                   - **FPS**: 再生速度（16fpsが自然）
                   - **背景色**: 透過部分の背景色
                3. **プレビュー生成**: ボタンを押してアニメーションを確認
                
                **💡 Tips**:
                - 線画やイラストに最適化されています
                - 透過PNGを使用すると背景色の指定が可能
                - パラメータを変更してリアルタイムで効果を確認できます
                """
            )
    
    return demo


def main():
    """アプリケーションのエントリポイント"""
    print("🌊 PluPlu Ripple を起動中...")
    
    demo = create_interface()
    
    # アプリケーションを起動
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
