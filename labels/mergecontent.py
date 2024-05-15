def merge_text_files(output_file, *input_files):
    with open(output_file, 'w') as out_file:
        for file_name in input_files:
            with open(file_name, 'r') as in_file:
                out_file.write(in_file.read())
                out_file.write('\n')  # Add a newline between the content of each file

# Example usage:

categories=['economic_impact','health_emergnecies','mentalhealth','pandemics','personal_experience','preventative_measures']
# C:\Users\30013717\Documents\Personal\GroupByClassModel\labels\health_emergnecies\health_emergnecies_gemini.txt
for cindex,i in  enumerate(categories):
    input_files = [f'labels/{i}/{i}_gpt.txt', f'labels/{i}/{i}_gemini.txt', f'labels/{i}/{i}_mistral.txt']
    output_file = f'labels/merged_{i}.txt'
    merge_text_files(output_file, *input_files)
    print(f"{i} Files merged successfully!")
