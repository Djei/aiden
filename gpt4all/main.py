from huggingface_hub import hf_hub_download
from pyllamacpp.model import Model

#Download the model
model_path = hf_hub_download(repo_id="LLukas22/gpt4all-lora-quantized-ggjt", filename="ggjt-model.bin")

#Load the model
model = Model(ggml_model=model_path, n_ctx=512)

#Generate
prompt="Write a poem about a large language model"

def new_text_callback(text: str):
  print(text, end="", flush=True)

model.generate(prompt, n_predict=1500, new_text_callback=new_text_callback, n_threads=8)