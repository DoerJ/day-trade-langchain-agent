from huggingface_hub import hf_hub_download

path = hf_hub_download(
    repo_id="foduucom/stockmarket-future-prediction",
    filename="best.pt",
    local_dir="./model"
)

print(path)