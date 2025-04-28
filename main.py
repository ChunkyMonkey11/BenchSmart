import math

# --- User Inputs (to be populated via CLI or UI) ---
CW_X_R = None           # Tuple: (weight lifted, number of reps)
GOAL = None             # Target 1RM (float)
TIMEFRAME = None        # Timeframe in weeks (int or float)
FREQUENCY = None        # Training frequency per week (int)

# --- Functions ---

def estimate_1rm(CW_X_R):
    """
    Estimate the user's current 1-rep max using the Epley formula.
    """
    weight, reps = CW_X_R
    if reps <= 0 or weight <= 0:
        raise ValueError("Weight and reps must be greater than 0")
    return weight * (1 + reps / 30)

def calculate_weekly_rate(current_1rm, goal_1rm, weeks):
    """
    Calculate the weekly strength progression rate required to reach the goal 1RM.
    """
    return (goal_1rm / current_1rm) ** (1 / weeks) - 1

def calculate_reps_for_weight(proj_1rm, weight):
    """
    Given a target 1RM and working weight, estimate the number of reps using reverse Epley.
    """
    reps = 30 * ((proj_1rm / weight) - 1)
    return max(1, round(reps))  # Ensure at least 1 rep

def get_user_inputs():
    """
    Collects and returns user inputs.
    """
    print("Welcome to the Bench Press Progression Planner!\n")

    try:
        weight = float(input("Enter the weight you lifted (lbs): "))
        reps = int(input("Enter the number of reps you completed with that weight: "))
        if weight <= 0 or reps <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input. Weight must be a number > 0, and reps must be an integer > 0.")
        exit()
    CW_X_R = (weight, reps)

    try:
        GOAL = float(input("Enter your goal 1-rep max (lbs): "))
        if GOAL <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input. Goal must be a number greater than 0.")
        exit()

    try:
        TIMEFRAME = float(input("Enter your timeframe to reach your goal (in weeks): "))
        if TIMEFRAME <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input. Timeframe must be a number greater than 0.")
        exit()

    try:
        FREQUENCY = int(input("How many times per week do you bench press (1–4)? "))
        if FREQUENCY not in [1, 2, 3, 4]:
            raise ValueError
    except ValueError:
        print("Invalid input. Frequency should be 1, 2, 3, or 4.")
        exit()

    return CW_X_R, GOAL, TIMEFRAME, FREQUENCY

def generate_weekly_plan(current_1rm, rate, weeks, frequency):
    """
    Generate and print a detailed week-by-week session plan with calculated weight × reps.
    """
    print("\n--- Weekly Bench Press Progression Plan ---\n")
    weeks = int(weeks)
    intensities = [0.80, 0.85, 0.90, 0.875]  # Extended for up to 4 sessions

    for week in range(1, weeks + 1):
        projected_1rm = current_1rm * (1 + rate) ** week
        projected_1rm = round(projected_1rm, 2)

        print(f"Week {week} - Projected 1RM: {projected_1rm} lbs")
        for session in range(1, frequency + 1):
            intensity = intensities[(session - 1) % len(intensities)]
            working_weight = projected_1rm * intensity
            working_weight = round_to_nearest(projected_1rm * intensity, base=2.5)
            reps = calculate_reps_for_weight(projected_1rm, working_weight)
            print(f"  Session {session}: Bench {working_weight} lbs × {reps} reps")
        print()

    print("Note: Reps are estimated based on intensity using reverse Epley.")
    print("These targets are starting points. Adjust based on real-world performance and recovery.")

def round_to_nearest(weight, base):
    return round(weight / base) * base

# --- Main Execution Flow ---
if __name__ == "__main__":
    CW_X_R, GOAL, TIMEFRAME, FREQUENCY = get_user_inputs()

    current_1rm = estimate_1rm(CW_X_R)

    if current_1rm >= GOAL:
        print("\n⚠️ Your current estimated 1RM is already above your goal.")
        print("Consider increasing your goal or reassessing your input.\n")
        exit()

    weekly_rate = calculate_weekly_rate(current_1rm, GOAL, TIMEFRAME)

    print("\n--- Calculation Results ---")
    print(f"Estimated current 1RM: {round(current_1rm, 2)} lbs")
    print(f"Required weekly progression rate: {round(weekly_rate * 100, 2)}%\n")

    generate_weekly_plan(current_1rm, weekly_rate, TIMEFRAME, FREQUENCY)
