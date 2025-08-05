import gradio as gr
from kittentts import KittenTTS
import soundfile as sf

# It's recommended to install the required libraries in your environment:
# pip install gradio soundfile
# pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl

# Load the model
try:
    m = KittenTTS("KittenML/kitten-tts-nano-0.1")
except Exception as e:
    print(f"Error loading model: {e}")
    # Handle model loading failure, maybe by displaying an error in the Gradio app

# Define the list of available voices
available_voices = [
    'expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f',
    'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f'
]

def generate_audio(text, voice):
    """
    Generates audio from text using the selected voice.
    """
    try:
        audio_data = m.generate(text, voice=voice)
        sample_rate = 24000
        file_path = "output.wav"
        sf.write(file_path, audio_data, sample_rate)
        return file_path
    except Exception as e:
        return str(e)


# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# KittenTTS Gradio App")
    gr.Markdown("A simple Gradio app to play with the KittenTTS model.")
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(label="Input Text", placeholder="Enter text to synthesize...")
            voice_input = gr.Dropdown(
                choices=available_voices, label="Select Voice", value=available_voices[0]
            )
            generate_button = gr.Button("Generate Audio")
        with gr.Column():
            audio_output = gr.Audio(label="Generated Audio", type="filepath")

    generate_button.click(
        fn=generate_audio,
        inputs=[text_input, voice_input],
        outputs=audio_output,
    )

    gr.Markdown("## About KittenTTS")
    gr.Markdown(
        "KittenTTS is an open-source, lightweight, and high-quality "
        "text-to-speech model. For more information, visit the "
        "[KittenTTS GitHub repository](https://github.com/KittenML/KittenTTS)."
    )

# Launch the app
if __name__ == "__main__":
    demo.launch(share=True)
