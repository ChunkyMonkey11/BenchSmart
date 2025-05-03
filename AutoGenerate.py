"""                         General Description                           
                The purpose of AutoGenerate is to test a method of testing the 
                weekly plan generated on various json data. The json data is pulled from 
                fitness_profile.json. We should build a function that handles 
                getting the json data and storing it in the assigned variables that
                other functions use. 
                
"""








import json

# --- User Inputs (to be populated via CLI or UI) ---
CW_X_R = None           # Tuple: (weight lifted, number of reps)
GOAL = None             # Target 1RM (float)
TIMEFRAME = None        # Timeframe in weeks (int or float)
FREQUENCY = None        # Training frequency per week (int)
EXPERIENCE_LEVEL = None  # "Beginner", "Intermediate", or "Advanced"

# --- Functions ---

# Function to process the sample fitness data. : Json File -> Processable data for other functions to use.
def process_fitness_data(json_path):
    with open(json_path) as fitness_file:
        profile_contents = json.load(fitness_file)
    CW_X_R = tuple(profile_contents["Current_Weight_X_Reps"])
    GOAL = profile_contents["Goal"]
    TIMEFRAME = profile_contents["Timeframe"]
    EXPERIENCE_LEVEL = profile_contents["Experience_Level"]
    return CW_X_R, GOAL, TIMEFRAME, EXPERIENCE_LEVEL
        
    
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

    # print("Note: Reps are estimated based on intensity using reverse Epley.")
    # print("These targets are starting points. Adjust based on real-world performance and recovery.")

def round_to_nearest(weight, base):
    return round(weight / base) * base


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

def get_safe_rate(experience):
    if experience == 'beginner':
        return 0.02  # 2% per week possible
    elif experience == 'intermediate':
        return 0.01
    elif experience == 'advanced':
        return 0.005
    return 0.01  # fallback default

MAX_SAFE_WEEKLY_RATE = get_safe_rate(EXPERIENCE_LEVEL)
# --- Test Cases ---

# Bottom code should only call functions that pertain the files purpose stated in header.
if __name__ == "__main__":
    "Automatically pull data from json file in path"
    user_sample_data_path = '/Users/revantpatel/BenchSmart/fitness_profile.json'
    CW_X_R, GOAL, TIMEFRAME, EXPERIENCE_LEVEL = process_fitness_data(user_sample_data_path)
    