import asyncio
from app.workflow import create_code_review_workflow

async def main():
    print("Initializing Code Review Workflow...")
    engine = create_code_review_workflow()
    
    # Needs to be complex enough to trigger the loop once or twice
    # complexity = len, triggers loop. 
    # check_complexity node: loop if < 80 score.
    # score = 100 - (complexity * 0.5) - (issues * 10)
    # to fail: complexity * 0.5 + issues * 10 > 20
    # e.g. complexity 42 -> 21 deduction -> score 79 -> loop
    
    # We want a function name length 42 approx.
    # "def " + 38 chars
    long_name = "x" * 38
    
    code_input = f"""
def {long_name}():
    print("Hello")
    """
    
    initial_state = {"code": code_input}
    
    print("\n--- Starting Execution ---")
    result = await engine.run(initial_state)
    
    print("\n--- Execution Finished ---")
    print("Final State Keys:", result["final_state"].keys())
    print("Quality Score:", result["final_state"].get("quality_score"))
    
    print("\n--- History ---")
    for step in result["history"]:
        print(step)

if __name__ == "__main__":
    asyncio.run(main())
