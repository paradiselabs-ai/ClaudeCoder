# ClaudeCoder for coding help (FOR LOCAL USE - READ WARNING BELOW BEFORE DEPLOYING ONLINE!!)

/*WARNING - FRONTEND uses react app modules that have vulnerabilites right now, some very serious. I could not update the npm dependencies without either causing more or not making any difference and i spent hours trying. DEPLOY ONLINE AT YOUR OWN RISK. Safest bet is to use this code assistant locally only.*/

Model used: anthropic/claude-3-5-sonnet-20240620

Endpoints can be directly from anthropic or openrouter (must have an openrouter api key to use openrouter endpoint, in which case feel free to edit the project files to use whatever model you want through openrouter. however claude 3.5 sonnet is a very very good model for code and has a 100,000 context limit)

On top of this 100,000 conext limit I have added the following features:

1. Session Management: Tracks and manages different conversation sessions.
2. Conversation Storage: Stores and retrieves conversation chunks with summaries.
3. Vector Generation and Search: Uses sentence-transformers for vector representation and cosine similarity for search.

This advanced chunking, conversation summerization, and vector retrieval makes the interface similar to that of chatGPT's as far as claude being able to keep a very large memory of not only very long conversations but also the conversations are session based and you can see your list of them on the side, and claude should be able to retrieve context even from different conversations, giving it an almost virtually "unlimited" contextual memory.

## to use: git clone this repo

```bash
cd ClaudeCoder

python -m venv claude-env
source claude-env/bin/source

pip install -r requirements.txt

touch .env

sudo nano .env
```

## Add to .env

```bash
ANTHROPIC_API_KEY=<insert_api_key>

```

**to setup frontend:**

```bash
    cd frontend

    npm install
```

## start project

**Start backend server:**

```bash
    cd ../
```

* to get to main directory

```bash
    uvicorn api.main:app --reload
```

**start frontend dev server:**

```bash
    cd frontend
    npm start
```

## Usage

1. Open your browser and navigate to localhost:3000 to access the ClaudeCoder interface.
2. Interact with the AI assistant by typing your queries and receiving contextual coding help.

## Contributing - would love to have contributors

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -m 'Add some feature').
5. Push to the branch (git push origin feature-branch).
6. Open a pull request.

## Things I am looking to implement

1. Code Interpretation
2. Ways to upload datasets
3. Creating multi-agentic instances of claude for better code help/mimic an actual developer team.
