#!/usr/bin/env python3
"""
Script to start the MiniRAG server with the correct configuration.
"""

import os
import subprocess
import argparse
from dotenv import load_dotenv

def main():
    """Main function to start the MiniRAG server."""
    # Load environment variables
    load_dotenv()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Start the MiniRAG server")
    parser.add_argument("--working-dir", default=os.getenv("MINIRAG_WORKING_DIR", "./data/storage"), help="Working directory for MiniRAG")
    parser.add_argument("--cosine-threshold", default=os.getenv("MINIRAG_COSINE_THRESHOLD", "0.4"), help="Cosine threshold for MiniRAG")
    parser.add_argument("--top-k", default=os.getenv("MINIRAG_TOP_K", "10"), help="Top K for MiniRAG")
    parser.add_argument("--embedding-binding", default=os.getenv("MINIRAG_EMBEDDING_BINDING", "openai"), help="Embedding binding for MiniRAG")
    parser.add_argument("--embedding-model", default=os.getenv("MINIRAG_EMBEDDING_MODEL", "text-embedding-3-large"), help="Embedding model for MiniRAG")
    parser.add_argument("--llm-binding", default=os.getenv("MINIRAG_LLM_BINDING", "openai"), help="LLM binding for MiniRAG")
    parser.add_argument("--llm-model", default=os.getenv("MINIRAG_LLM_MODEL", "gpt-4-turbo"), help="LLM model for MiniRAG")
    parser.add_argument("--openai-api-key", default=os.getenv("OPENAI_API_KEY", ""), help="OpenAI API key")
    parser.add_argument("--input-dir", default=os.getenv("MINIRAG_INPUT_DIR", "./data/inputs"), help="Directory containing input documents")
    parser.add_argument("--port", default=os.getenv("MINIRAG_PORT", "9621"), help="Server port")
    parser.add_argument("--host", default=os.getenv("MINIRAG_HOST", "0.0.0.0"), help="Server host")
    parser.add_argument("--embedding-batch-num", default=os.getenv("EMBEDDING_BATCH_NUM", "32"), help="Batch size for embedding computations")
    parser.add_argument("--embedding-func-max-async", default=os.getenv("EMBEDDING_FUNC_MAX_ASYNC", "16"), help="Maximum number of concurrent embedding function calls")

    args = parser.parse_args()

    # Set OpenAI API key as environment variable if provided
    if (args.embedding_binding == "openai" or args.llm_binding == "openai") and args.openai_api_key:
        os.environ["OPENAI_API_KEY"] = args.openai_api_key

    # Build the command
    command = [
        "lightrag-server",
        "--working-dir", args.working_dir,
        "--input-dir", args.input_dir,
        "--cosine-threshold", args.cosine_threshold,
        "--top-k", args.top_k,
        "--embedding-binding", args.embedding_binding,
        "--llm-binding", args.llm_binding,
        "--host", args.host,
        "--port", args.port,
        "--max-tokens", "128000",  # Use a large token limit for GPT-4 Turbo
        "--embedding-batch-num", args.embedding_batch_num,
        "--embedding-func-max-async", args.embedding_func_max_async
    ]

    # Set environment variables for models
    os.environ["EMBEDDING_MODEL"] = args.embedding_model
    os.environ["LLM_MODEL"] = args.llm_model

    # Set embedding dimension to match the model
    # text-embedding-3-large has 3072 dimensions, text-embedding-3-small has 1536 dimensions
    if args.embedding_model == "text-embedding-3-large":
        os.environ["EMBEDDING_DIM"] = "3072"
    elif args.embedding_model == "text-embedding-3-small":
        os.environ["EMBEDDING_DIM"] = "1536"
    else:
        # Default for other models
        os.environ["EMBEDDING_DIM"] = "1536"

    # Print the command
    print("Starting MiniRAG server with command:")
    print(" ".join(command))
    print(f"Using LLM model: {args.llm_model}")
    print(f"Using embedding model: {args.embedding_model}")
    print(f"Using embedding dimension: {os.environ['EMBEDDING_DIM']}")

    # Start the server
    try:
        subprocess.run(command, env=os.environ)
    except KeyboardInterrupt:
        print("\nMiniRAG server stopped")
    except Exception as e:
        print(f"Error starting MiniRAG server: {str(e)}")
        print("\nMake sure you have installed MiniRAG with:")
        print("pip install lightrag-hku[api]")

if __name__ == "__main__":
    main()
