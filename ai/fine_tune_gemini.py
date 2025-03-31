import google.generativeai as genai
import pandas as pd
import numpy as np
import faiss
import json

# Load Google API key
genai.configure(api_key="GOOGLE_GEMINI_API_KEY")

# Load dataset
df = pd.read_csv("sha_dataset.csv")

# Create Embeddings for Each Question
def generate_embedding(text):
    response = genai.embed_content(model="models/embedding-001", content=text)
    return np.array(response["embedding"])

# Generate Vectors for Dataset
df["vector"] = df["Question"].apply(generate_embedding)

# Convert Vectors to FAISS Format
dimension = len(df["vector"].iloc[0])
index = faiss.IndexFlatL2(dimension)
vectors = np.vstack(df["vector"].values).astype("float32")
index.add(vectors)

# Save Index
faiss.write_index(index, "sha_index.faiss")

# Save Data Mapping
df[["ID", "Question", "Answer"]].to_json("sha_mapping.json", orient="records")

print("Fine-tuning completed. SHA model is ready!")


# Fine-Tune Gemini AI Using Vertex AI

