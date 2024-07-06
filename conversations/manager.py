import sqlite3
import numpy as np
import os
import uuid
import anthropic
from openai import OpenAI  # OpenRouter uses OpenAI's client library
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

# init clients and models
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
use_service = os.getenv("USE_SERVICE", "anthropic")  # default anthropic if not specified

anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
openrouter_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")

tokenizer = AutoTokenizer.from_pretrained("gpt2")
sentence_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

class ConversationManager:
    def __init__(self, db_name="conversations.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        self.conversations = {}
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Load the sentence transformer model
        self.api_choice = use_service
        if self.api_choice == "anthropic":
            self.api_client = anthropic_client
        elif self.api_choice == "openrouter":
            self.api_client = openrouter_client
        else:
            raise ValueError("Invalid API choice. Choose either 'anthropic' or 'openrouter'.")

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                session_id TEXT,
                user_id TEXT,
                chunk TEXT,
                summary TEXT,
                vector BLOB
            )
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT,
                name TEXT
            )
            """)

    def create_new_session(self):
        session_id = str(uuid.uuid4())
        with self.conn:
            self.conn.execute("INSERT INTO sessions (session_id, name) VALUES (?, ?)", (session_id, "New Session"))
        self.conversations[session_id] = {'chunks': [], 'current': [], 'current_token_count': 0}
        return session_id

    def start_conversation(self, user_id, session_id):
        self.conversations[session_id] = {'chunks': [], 'current': [], 'current_token_count': 0, 'user_id': user_id}

    def add_turn(self, session_id, user_input, ai_response):
        if session_id not in self.conversations:
            raise ValueError(f"No active conversation for session_id {session_id}")

        turn_text = f"User: {user_input}\nAI: {ai_response}"
        tokens = tokenizer(turn_text)["input_ids"]
        token_count = len(tokens)

        self.conversations[session_id]['current'].append({'user': user_input, 'ai': ai_response})
        self.conversations[session_id]['current_token_count'] += token_count

        if self.conversations[session_id]['current_token_count'] > 5000:  # Adjust chunk size as needed
            self.summarize_and_store(session_id)

    def get_context(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT chunk, summary FROM conversations WHERE session_id=?", (session_id,))
        rows = cursor.fetchall()
        chunks = [{'summary': row[1], 'details': eval(row[0])} for row in rows]
        context = self.conversations.get(session_id, {'chunks': chunks, 'current': [], 'current_token_count': 0})
        return context['chunks'] + context['current']

    def summarize_and_store(self, session_id):
        current_chunk = self.conversations[session_id]['current']
        context_text = "\n".join([f"User: {turn['user']}\nAI: {turn['ai']}" for turn in current_chunk])
    
        try:
            if self.api_choice == "anthropic":
                summary_response = self.api_client.completions.create(
                    model="claude-3-sonnet-20240229",
                    prompt=f"Summarize the following conversation:\n\n{context_text}\n",
                    max_tokens_to_sample=500  # Increased summary size
                )
                summary = summary_response.completion
            elif self.api_choice == "openrouter":
                summary_response = self.api_client.chat.completions.create(
                    model="anthropic/claude-3-sonnet-20240229",  # Use Claude model via OpenRouter
                    messages=[
                        {"role": "system", "content": "Summarize the following conversation:"},
                        {"role": "user", "content": context_text}
                    ],
                    max_tokens=500
                )
                summary = summary_response.choices[0].message.content
        except Exception as e:
            print(f"Error generating summary: {e}")
            summary = "Error generating summary"        
        
        # Generate vector representation for vector search
        vector = self.generate_vector(summary)

        with self.conn:
            self.conn.execute("INSERT INTO conversations (session_id, user_id, chunk, summary, vector) VALUES (?, ?, ?, ?, ?)",
                              (session_id, self.conversations[session_id]['user_id'], str(current_chunk), summary, vector.tobytes()))
        self.conversations[session_id]['chunks'].append({'summary': summary, 'details': current_chunk})
        self.conversations[session_id]['current'] = []
        self.conversations[session_id]['current_token_count'] = 0

    def generate_vector(self, text):
        return self.model.encode([text])[0]

    def vector_search(self, query, top_k=5):
        query_vector = self.generate_vector(query)
        cursor = self.conn.cursor()
        cursor.execute("SELECT session_id, summary, vector FROM conversations")
        results = []
        for row in cursor.fetchall():
            session_id, summary, vector_bytes = row
            vector = np.frombuffer(vector_bytes, dtype=np.float32)
            similarity = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))
            results.append((session_id, summary, similarity))
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:top_k]

    def search_past_context(self, query):
        results = self.vector_search(query)
        return [{'session_id': r[0], 'summary': r[1], 'similarity': r[2]} for r in results]

    def rename_session(self, session_id, new_name):
        with self.conn:
            self.conn.execute("UPDATE sessions SET name = ? WHERE session_id = ?", (new_name, session_id))

    def get_all_sessions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT session_id, name FROM sessions")
        return cursor.fetchall()

    def close(self):
        self.conn.close()
