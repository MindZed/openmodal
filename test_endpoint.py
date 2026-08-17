import modal
import sys
import time

def ask_gemma(prompt):
    print(f"\n[You]: {prompt}")
    print("[Gemma]: Thinking...", end="", flush=True)
    
    start_time = time.time()
    try:
        # Lookup our deployed Modal class natively
        Server = modal.Cls.from_name("gemma-4-e4b-server", "Server")
        
        # Instantiate and call the generate method
        # This will securely connect over gRPC and handle all authentication
        server = Server()
        answer = server.generate.remote(prompt)
        
        elapsed = time.time() - start_time
        
        # Clear the "Thinking..." line and print the answer
        sys.stdout.write("\r\033[K")
        print(f"[Gemma]: {answer.strip()}")
        print(f"\n(Response time: {elapsed:.2f} seconds)")
        
    except Exception as e:
        sys.stdout.write("\r\033[K")
        print(f"[Error]: {e}")

if __name__ == "__main__":
    print("=== Modal Gemma-4-E4B Native Test Script ===")
    print("Type 'exit' or 'quit' to stop.")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                break
                
            ask_gemma(user_input)
            
        except KeyboardInterrupt:
            break
            
    print("\nGoodbye!")
