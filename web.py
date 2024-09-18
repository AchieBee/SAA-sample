import re
import csv

def process_question(question_text):
    match = re.match(r'(\d+)\)\s*(.*)', question_text, re.DOTALL)
    if match:
        return match.group(2).strip()
    return question_text.strip()

def process_answers(answer_text):
    answers = re.findall(r'([A-E])\.\s*([^\n]+)', answer_text)
    return [answer[1].strip() for answer in answers]

def process_file(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Split content into questions and answers
    parts = content.split('Answers', 1)
    if len(parts) != 2:
        print("Error: Could not split content into questions and answers.")
        return

    questions_part, answers_part = parts

    # Process questions
    questions = re.split(r'\n(?=\d+\))', questions_part.strip())
    csv_data = []

    for q in questions:
        question = process_question(q)
        answers = process_answers(q)
        
        if len(answers) < 2:
            print(f"Warning: Not enough answers found for question: {question[:50]}...")
            continue

        csv_data.append([question] + answers + [''] * (4 - len(answers)))

    # Process answers
    correct_answers = re.findall(r'(\d+)\)\s*([A-E](?:,\s*[A-E])*)', answers_part)

    for q_num, correct_ans in correct_answers:
        q_index = int(q_num) - 1
        if q_index < 0 or q_index >= len(csv_data):
            print(f"Warning: Answer {q_num} does not match any question.")
            continue

        correct_ans_list = [ans.strip() for ans in correct_ans.split(',')]
        correct_ans_indices = [ord(ans) - ord('A') + 1 for ans in correct_ans_list]

        question_type = 'radio' if len(correct_ans_indices) == 1 else 'check'
        correct_ans_str = ','.join(map(str, correct_ans_indices))

        csv_data[q_index] += [correct_ans_str, question_type]

    # Write to CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Question', 'Ans1', 'Ans2', 'Ans3', 'Ans4', 'Correct ans', 'check_radio'])
        for row in csv_data:
            if len(row) == 7:  # Only write complete rows
                writer.writerow(row)
            else:
                print(f"Warning: Incomplete data for question: {row[0][:50]}...")

    print(f"Processed {len(csv_data)} questions. Check {output_file} for results.")

# Usage
process_file('sample.txt', 'sample.csv')