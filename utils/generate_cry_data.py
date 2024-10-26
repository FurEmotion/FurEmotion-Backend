import os
import json
import random
from datetime import datetime, timedelta
import sqlite3

# Define the cry states for cats and dogs
cat_cry_states = ['happy', 'hunger', 'lonely']
dog_cry_states = ['anger', 'play', 'happy', 'sad']

# Define intensities
intensities = ['low', 'medium', 'high']

# Function to generate a random predictMap based on the pet's cry states


def generate_predict_map(cry_states):
    # Ensure at least two states have non-zero probabilities
    num_non_zero = random.randint(2, len(cry_states))
    non_zero_states = random.sample(cry_states, num_non_zero)
    zero_states = [
        state for state in cry_states if state not in non_zero_states]

    # Generate random probabilities for the non-zero states
    probabilities = [random.random() for _ in non_zero_states]
    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]

    # Combine into a single dictionary
    predict_map = {state: 0.0 for state in zero_states}
    for state, prob in zip(non_zero_states, probabilities):
        predict_map[state] = round(prob, 3)
    return predict_map

# Function to generate dummy data for a pet (cat or dog)


def save_pet_cry_sample_data_to_file(start_date, end_date, pet_id, pet_type, total_entries, file_path):
    audio_id_counter = 1

    # Select cry states based on pet type
    if pet_type.lower() == 'cat':
        cry_states = cat_cry_states
    elif pet_type.lower() == 'dog':
        cry_states = dog_cry_states
    else:
        raise ValueError("Invalid pet type. Please use 'cat' or 'dog'.")

    # Calculate the total time delta
    total_seconds = (end_date - start_date).total_seconds()
    # Calculate average interval between cries
    avg_interval = total_seconds / total_entries

    # Generate cry times spread over the date range
    cry_times = []
    for i in range(total_entries):
        # Calculate the time offset from the start date
        time_offset = avg_interval * i
        # Add some randomness to the time offset
        random_offset = random.uniform(-avg_interval / 2, avg_interval / 2)
        actual_offset = time_offset + random_offset
        # Ensure the actual offset is within the date range
        actual_offset = max(0, min(total_seconds, actual_offset))
        # Calculate the actual cry time
        cry_time = start_date + timedelta(seconds=actual_offset)
        cry_times.append(cry_time)

    # Sort the cry times
    cry_times.sort()

    # Writing data to the file
    with open(file_path, 'a') as file:
        for cry_time in cry_times:
            # Randomly select intensity and duration
            intensity = random.choice(intensities)
            duration = round(random.uniform(2.0, 17.0), 2)
            # Generate predictMap and select state with the largest probability
            predict_map = generate_predict_map(cry_states)
            selected_state = max(predict_map, key=predict_map.get)
            # Ensure that no probability is 1.0 and at least two probabilities are non-zero
            if predict_map[selected_state] == 1.0 or sum(1 for p in predict_map.values() if p > 0) < 2:
                continue  # Skip this iteration if condition is not met
            # Create the SQL INSERT statement
            insert_statement = f"INSERT INTO cry (pet_id, time, state, audioId, predictMap, intensity, duration) VALUES ({pet_id}, '{cry_time.strftime('%Y-%m-%d %H:%M:%S')}', '{selected_state}', 'audioId{audio_id_counter}', '{json.dumps(predict_map)}', '{intensity}', {duration});\n"
            file.write(insert_statement)
            audio_id_counter += 1

    return file_path


# Main function to get user input and generate data
if __name__ == '__main__':
    PROJECT_DIR = os.getcwd().split(
        'FurEmotion-Backend')[0] + 'FurEmotion-Backend'
    file_path = os.path.join(PROJECT_DIR, 'dataset', 'pet_cry_sample_data.sql')
    database_path = os.path.join(PROJECT_DIR, 'Database.db')

    start_date = datetime(2024, 10, 3)
    end_date = datetime(2024, 11, 6)

    user = {
        "uid": "yTKx5CWGvLbjKVCRgve6K5Ne8cv2",
        "email": "importjaewone@gmail.com",
        "nickname": "재원E import",
        "photoId": "https://lh3.googleusercontent.com/a/ACg8ocImJ4n_F7nNCoqxlFA3SN2odkufbJFPRCOowJzLBmT3=s96-c",
    }

    # Pet IDs and types
    pets = [
        {'pet_id': 1,
         'pet_type': 'cat',
         'total_entries': 300,
         'name': "뽀삐",
         "gender": "male",
         "age": 1,
         "species": "dog",
         "photo_id": "1.jpeg",
         "sub_species": "푸들"},
        # {'pet_id': 2,
        #  'pet_type': 'dog',
        #  'total_entries': 300,
        #  'name': "루리",
        #  "gender": "female",
        #  "age": 2,
        #  "species": "cat",
        #  "photo_id": "2.jpeg",
        #  "sub_species": "스코티쉬폴드"},
    ]

    # Clear the file before writing
    open(file_path, 'w').close()

    # Generate User data
    if True:
        with open(file_path, 'a') as file:
            uid = user['uid']
            email = user['email']
            nickname = user['nickname']
            photo_id = user['photoId']
            file.write(
                f"INSERT INTO user (uid, email, nickname, photoId) VALUES ('{uid}', '{email}', '{nickname}', '{photo_id}');\n")

    # Generate Pet data
    with open(file_path, 'a') as file:
        for pet in pets:
            name = pet['name']
            gender = pet['gender']
            age = pet['age']
            species = pet['species']
            photo_id = pet['photo_id']
            sub_species = pet['sub_species']
            user_id = user['uid']
            file.write(
                f"INSERT INTO pet (name, gender, age, species, photo_id, sub_species, user_id) VALUES ('{name}', '{gender}', {age}, '{species}', '{photo_id}', '{sub_species}', '{user_id}');\n")

    # Generate data for each pet
    for pet in pets:
        save_pet_cry_sample_data_to_file(
            start_date=start_date,
            end_date=end_date,
            pet_id=pet['pet_id'],
            pet_type=pet['pet_type'],
            total_entries=pet['total_entries'],
            file_path=file_path
        )

    # insert into Database.db
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    with open(file_path, 'r', encoding='utf-8') as sql_file:
        sql_script = sql_file.read()

    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
