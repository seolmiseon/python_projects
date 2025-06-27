# 🚀 LLM Projects with Hugging Face & GPU

Welcome to my LLM projects repository leveraging Hugging Face models and GPU acceleration! 🤖💻

## 🌟 Project Highlights

### 1. Conversational AI Assistant

![Conversational AI](https://github.com/seolmiseon/llm_projects/raw/main/images/conversational_ai.gif)
_Interactive chatbot powered by GPT-3 and fine-tuned with domain-specific data_

### 2. Text Summarization Engine

![Text Summarization](https://github.com/seolmiseon/llm_projects/raw/main/images/text_summarization.png)
_Efficient text summarization using T5 and optimized with GPU_

### 3. Question-Answering System

![QA System](https://github.com/seolmiseon/llm_projects/raw/main/images/qa_system.png)
_Advanced Q&A system using BERT and RAG (Retrieval-Augmented Generation)_

## 🛠️ Projects & Technologies

1. **Conversational AI Assistant** (✅ Completed)

    - Interactive chatbot for customer support
    - Technologies: Python, Hugging Face Transformers, GPT-3, CUDA

2. **Text Summarization Engine** (🚧 In Progress)

    - Automatic summarization of long documents
    - Technologies: Python, Hugging Face Transformers, T5, PyTorch, GPU acceleration

3. **Question-Answering System** (✅ Completed)

    - Context-aware Q&A for large datasets
    - Technologies: Python, Hugging Face Transformers, BERT, FAISS, CUDA

4. **Few-Shot Learning Classifier** (🔜 Planned)
    - Text classification with minimal training data
    - Technologies: Python, Hugging Face Transformers, GPT-3, PyTorch, GPU optimization

## 🔧 Key Libraries & Tools

-   Hugging Face Transformers 🤗 for state-of-the-art LLMs
-   PyTorch 🔥 for deep learning
-   CUDA 🚀 for GPU acceleration
-   FAISS 🔍 for efficient similarity search and clustering
-   Streamlit 🌟 for creating interactive web demos

## 🖥️ GPU Setup

This project utilizes GPU acceleration. Ensure you have:

-   NVIDIA GPU with CUDA support
-   CUDA Toolkit installed
-   Appropriate GPU drivers

Check GPU availability in Python:

```python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```
