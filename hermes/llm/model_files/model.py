import os
from llama_cpp import Llama

# Carpeta donde está este script
BASE_DIR = os.path.dirname(__file__)

model_id = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"

# Ruta correcta al modelo
model_path = os.path.join(BASE_DIR, "bin", model_id)

# Cargar el modelo
llm = Llama(model_path=model_path)






# import torch
# from huggingface_hub import login
# from decouple import config
# from transformers import pipeline, logging

# # Login on Hugging Face
# token = config("HF_TOKEN_READ", default=False)
# login(token)

# # Removes all the logs and warnings from transformers (logging)
# logging.set_verbosity_error()

# model_id = "meta-llama/Llama-3.2-1B-Instruct"


# pipe = pipeline(
#     "text-generation",
#     model=model_id,
#     dtype=torch.float32, # downgrade for old hardware
#     device_map="cpu", # forces CPU - downgrade for old hardware
# )