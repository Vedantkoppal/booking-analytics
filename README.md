# Booking Analytics with FastAPI and Ollama

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.11-green?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.39-blue?style=flat&logo=python)](https://www.sqlalchemy.org/)
[![Plotly](https://img.shields.io/badge/Plotly-6.0.1-purple?style=flat&logo=plotly)](https://plotly.com/)
[![LlamaIndex](https://img.shields.io/badge/LlamaIndex-0.12.25-orange?style=flat&logo=python)](https://www.llamaindex.ai/)
[![Ollama](https://img.shields.io/badge/Ollama-0.4.7-black?style=flat)](https://ollama.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2.3-blue?style=flat&logo=pandas)](https://pandas.pydata.org/)

An assignment on booking analytics and Q&A platform built using **FastAPI** with **Plotly** visualizations and **Ollama's Phi-4 mini model** for natural language queries. The system provides insights into various booking trends and allows users to ask questions about the booking data.


## 🚀 Setup / Installation

### Prerequisites
- Python 3.11 or higher
- Ollama installed on your system ([Download Ollama](https://ollama.com/download))

---

### Step 1: Pull the LLM Model
```bash
ollama pull phi4-mini:latest