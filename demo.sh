#仅使用CPU
#python -m llama_cpp.server --host 0.0.0.0 --model .\\model\\Meta-Llama-3-8B-Instruct.Q2_K.gguf --n_ctx 2048
# 如果你有NVidia GPU
#python -m ../llama.cpp/server --host 0.0.0.0 --model ../model/Meta-Llama-3-8B-Instruct.Q2_K.gguf --n_ctx 2048 --n_gpu_layers 28
../llama.cpp/server --host 0.0.0.0 --model ../model/Meta-Llama-3-8B-Instruct.Q2_K.gguf
