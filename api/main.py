import os
from dotenv import load_dotenv
import gradio as gr
from cnn.road_detection_model import RoadDetectionModel

load_dotenv()
IS_DEV = int(os.getenv("IS_DEV"))
rdm = RoadDetectionModel()

def classify_road_condition(image_path):
    result = rdm.predict(image_path)
    map_result = {
        "clean": "The road is clean and well-maintained.",
        "dirty": "The road is dirty and may need cleaning.",
        "potholes": "The road contains potholes and needs repair.",
    }

    return f"Result: {result}\nMessage: {map_result[result]}"

def train_model(btn):
    rdm.train()

with gr.Blocks() as iface:
    with gr.Row():
        inp = gr.Image(type="filepath", label="Select an image")
        out = gr.Textbox()
    predict_btn = gr.Button("Run")
    predict_btn.click(fn=classify_road_condition, inputs=inp, outputs=out)
    if IS_DEV:
        with gr.Row():
            train_btn = gr.Button()
            train_btn.value = "Train model"
            train_btn.click(fn=train_model, inputs=train_btn, outputs=train_btn)

iface.launch(server_name="0.0.0.0", server_port=8000)
