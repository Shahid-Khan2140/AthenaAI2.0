# --- A Self-Made Career Advisor ---
def start_career_advisor():
    """
    This function runs the main logic for the career advisor.
    It asks the user questions and provides a suggestion based on pre-defined rules.
    """
    
    print("-----------------------------------------")
    print(" Welcome to the Self-Made Career Advisor ")
    print("-----------------------------------------")
    print("Please answer the following questions with 'yes' or 'no'.\n")

    # --- Gather Facts from the User ---
    try:
        # Get user input and clean it up (convert to lowercase, remove whitespace)
        likes_tech = input("Do you enjoy working with computers and technology? > ").lower().strip()
        likes_art = input("Are you a creative person who enjoys design and art? > ").lower().strip()
        likes_people = input("Do you like helping and interacting with other people? > ").lower().strip()
        likes_numbers = input("Are you good with numbers and enjoy analysis? > ").lower().strip()
    except KeyboardInterrupt:
        print("\n\nProgram cancelled by user. Goodbye!")
        return

    print("\n-----------------------------------------")
    print("Analyzing your answers...")
    print("-----------------------------------------")

    # --- The "Inference Engine" - This is your self-made logic ---    
    suggestion = "" # A variable to hold the final suggestion

    if likes_tech == 'yes' and likes_numbers == 'yes':
        suggestion = "Based on your interest in tech and numbers, you might enjoy being a Data Scientist or a Software Developer. 💻"
    elif likes_art == 'yes' and likes_tech == 'yes':
        suggestion = "Combining art and technology is perfect for a career as a UI/UX Designer. 🎨"
    elif likes_people == 'yes' and likes_art == 'yes':
        suggestion = "Your creativity and people skills would be great for a career as a Teacher or in Marketing. 👩‍🏫"
    elif likes_people == 'yes':
        suggestion = "Your interest in helping others could lead to a rewarding career in Human Resources or Counselling. 🤝"
    elif likes_numbers == 'yes':
        suggestion = "Your skill with numbers would be a great fit for an Accountant or a Financial Analyst. 💰"
    elif likes_art == 'yes':
        suggestion = "Your creativity could shine in a career as a Graphic Designer or a Writer. 🖼️"
    else:
        suggestion = "Your interests are diverse! It's a great time to explore different fields to find what you're passionate about. ✨"
        
    print(suggestion)
    print("-----------------------------------------\n")


# --- Main entry point of the program ---
if __name__ == "__main__":
    start_career_advisor()