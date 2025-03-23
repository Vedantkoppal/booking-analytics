
# 📊 Booking Analytics & Q&A System

![FastAPI](https://img.shields.io/badge/FastAPI-0.115.1-green?style=for-the-badge)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.39-orange?style=for-the-badge)
![Plotly](https://img.shields.io/badge/Plotly-6.0.1-blue?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-0.4.7-red?style=for-the-badge)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-0.12.25-purple?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-2.2.3-yellow?style=for-the-badge)

---

An FastAPI-based analytics dashboard and Q&A system that analyzes booking data, generates insightful graphs, and answers natural language questions using a fine-tuned `phi4-mini` model. It supports visualizing trends, tracking cancellations, and answering booking-related queries.

---

## 🚀 Setup / Installation

### Prerequisites
- Python 3.11 or higher
- Ollama installed on your system ([Download Ollama](https://ollama.com/download))
> Note: If using other models like `gpt-3.5-turbo` or OpenAI models, skip this step.
---

### Step 1: Pull the LLM Model
```bash
ollama pull phi4-mini:latest
```

---

### Step 2: Clone the Repository
```bash
git clone https://github.com/Vedantkoppal/booking-analytics.git
cd booking-analytics
```

---

### Step 3: Create and Activate Virtual Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# For Windows:
venv\Scripts\activate

# For Linux/Mac:
source venv/bin/activate
```

---

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

---

### Step 5: Run the Application
```bash
uvicorn app.main:app --reload
```
---
## 🚀 **APIs Implemented**

- `/analytics` - Returns various analytics reports.
- `/ask` - Answers booking-related questions using LLM.
- `/health` - Checks the status of system dependencies.
- `/history` - Displays chat/query history.
---
## Approach to Problem

## 📊 1. About Data
- The data preprocessed using standard data preprocessing techniques.
- **Duplicated Values:**
    - The data does not have unique identity rows. It does not contain specific user related information. Hence, it is sensible to treat data in that way. This means that data has much more information in group by analogy.
    - Almost 30% data is duplicated; All these duplicated rows contain same col values. Now for hotel booking system its possible that many users have booked in same conditions which is not uncommon for such a setting. On top of that, anonymous nature of data backs this statement. So I have considered all rows without dropping any rows.
- I have calculated certain additional cols required for analytics such as revenue, total_stays etc.
- Analytics was done using pandas dataframe queries.

---

## ⚡️ 2. Development
- I have used FastAPI for this project as simple and fast.
- I have used jinja2 template engine for building and parsing graphs into html.
- To create graphs, I have used plotly and used iframes to embed them into website.

---

## 🤖 3. RAG Vs QandA
- Instead of full RAG, I have used Question-Answering Approach in this project.
- **First thing to look at for this is - anonymous nature of data.** Our data is not row specific.
- **Fundamental thing about RAG-based systems** is that each row is unique which allows us to fetch information from it.  
    - For example: _"For user 'Krishna Yadav', tell me about his all room bookings."_  
      This statement is converted into vector representation and then, most similar records are fetched from vector databases.
    - The similar records are themselves vector representation of each row from database. This makes it able to fetch closest records and return calculations.
- **But the data we are using is not row specific, so RAG is not that much efficient in this case.**
- **Question and answering technique differs from RAG.**
    - Instead of converting all rows into vector representation, we save them as it is in database.
    - Next we take natural human query like _"Tell me number of hotel bookings done in July 2016 which were cancelled."_  
    - This query is converted into vector representation.
    - It is then passed to any Large Language Model like I have used phi4:mini.
    - Along with this query, all information about structure of database and tables is passed to the LLM.
    - It includes schema of database, detailed info about each field(column) with its datatype, database being used (sqlite, mysql).
    - Now any decent LLM is smart enough to convert user query into a proper syntax accurate SQL query.
    - Now this query is run against the table. Fetched records are returned.
- **This makes the most sense to retrieve the data in such a way:**
    - Using all power of LLM to understand a query and convert it into best possible, error-free query.
    - Such a query will give us most accurate results.
- This approach is known as **text-to-sql LLM system**.
