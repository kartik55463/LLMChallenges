from openai import OpenAI
import pandas as pd
import time
client = OpenAI(
    api_key="sk-CULBqccVTxv5NYA-s75xvSyaf_XMGWUuZInCUsHyLWT3BlbkFJhgGh6uL1SMJLfN5fGB5v3hsTOtEYHugxpO4kWfffoA"
)
def classify_text(text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a researcher doing research about challenges in developing LLM and you will be answering this research question: What types of questions are Large Language Model developers are asking?"},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please carefully read the following text entry and classify it into one of the specific categories below. Each entry should be assigned only one category:\n\n"
                                "1. Model Development and Deployment: If the text discusses tasks such as fine-tuning, model deployment, or data preprocessing.\n"
                                "2. Evaluation and Optimization: If the text is about evaluating performance, benchmarking, or long-term optimization.\n"
                                "3. Ethical and Best Practices: If the text includes ethical considerations, standards, or best practices in development.\n"
                                "4. Troubleshooting: If the text describes a real-time problem or issue that requires troubleshooting.\n"
                                "5. Feature Requests and Improvements: If the text suggests new features or improvements.\n"
                                "6. Guidance and Validation: If the text involves seeking advice or validation on a topic.\n"
                                "7. Maintenance and Ongoing Support: If the text discusses project maintenance or support tasks.\n\n" 
                                "Please only output the category name"
                                f"Text to classify: '{text}'"
                    }
                ]
            }
        ],
        max_tokens=50,
    )
    classification = response.choices[0].message.content
    return classification

def main(input_file_path, output_file_path):
    # Load the CSV file
    try:
        df = pd.read_csv(input_file_path)
    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
        return
    except pd.errors.EmptyDataError:
        print(f"No data: {input_file_path}")
        return
    except pd.errors.ParserError:
        print(f"Parsing error: {input_file_path}")
        return

    # Ensure the 'combined_text' column exists
    if 'Title' not in df.columns:
        print("The input CSV must contain a 'Title' column.")
        return

    # Apply the classification function to each row
    classifications = []
    for text in df['Title']: 
        classification = classify_text(text)
        classifications.append(classification)
        time.sleep(5)  # To respect API rate limits

    df['classification'] = classifications

    # Save the results to a new CSV file
    try:
        df.to_csv(output_file_path, index=False)
        print(f"Classification completed. Results saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    input_file_path ="5.selected.csv"  # Replace with your input file path
    output_file_path = '5.classified.csv'  # Replace with your desired output file path
    main(input_file_path, output_file_path)