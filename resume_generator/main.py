from google import genai
from pdflatex import PDFLaTeX

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key="AIzaSyAUtKr21KnsmYBqEz7ZMQ3X-b3ZuZHNPTc")
original_file = r"D:\automated.tex"
updated_file = r"D:\Tharun_Resume.tex"
def get_points(j_d):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""
        Analyze this job description and generate exactly 6 technical resume bullet points in LaTeX format for ATS optimization.

        Requirements:
        - Use exact keywords/technologies from the job description for ATS matching
        - Keep each bullet point concise (15-25 words maximum)
        - Start each point with a strong action verb (Built, Developed, Implemented, Designed, Architected, etc.)
        - Focus ONLY on technical skills: programming languages, frameworks, databases, cloud platforms, tools
        - Bold important technologies using \\textbf{{}} syntax
        - Include quantifiable metrics when possible (performance improvements, scale, system capacity, etc.)
        - Avoid soft skills like "communication", "teamwork", "agile methodology"

        MANDATORY HEALTHCARE CONTEXT:
        - ALL bullet points must be framed within healthcare/medical technology domain
        - Focus specifically on building scalable Electronic Health Records (EHR) systems
        - Highlight scalability for healthcare systems (patient volume, concurrent users, medical data processing)
        - Use healthcare terminology: patient records, clinical data, medical reports, healthcare providers, EHR modules

        Job Description:
        {j_d}

        Format exactly like this LaTeX structure:
        \\resumeItemListStart
        \\resumeItem{{[Action verb] [EHR/healthcare technical description] using \\textbf{{Technology}} [healthcare scalability/performance metrics]}}
        \\resumeItem{{[Action verb] [EHR/healthcare technical description] using \\textbf{{Technology}} [healthcare scalability/performance metrics]}}
        \\resumeItem{{[Action verb] [EHR/healthcare technical description] using \\textbf{{Technology}} [healthcare scalability/performance metrics]}}
        \\resumeItem{{[Action verb] [EHR/healthcare technical description] using \\textbf{{Technology}} [healthcare scalability/performance metrics]}}
        \\resumeItemListEnd

        Generate 6 bullet points that match the job's technical requirements while ALWAYS emphasizing healthcare EHR system development and scalability.
        """
    )
    print(response.text)
    text = response.text
    print(text[8:-4])
    return text[8:-4]


def replace_job_1(replacement_text):

    # Read original file
    with open(original_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Check if line 128 exists
    if len(lines) < 128:
        raise ValueError("File has fewer than 128 lines.")

    # Replace line 128 (index 127 since list is 0-based) with the new content
    replacement_lines = replacement_text.splitlines(keepends=True)
    lines[127:128] = [line + '\n' if not line.endswith('\n') else line for line in replacement_lines]

    # Write updated file
    with open(updated_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"Updated file saved as: {updated_file}")


def save_pdf():
    pdfl = PDFLaTeX.from_texfile(updated_file)
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)


@app.route('/generate', methods=['POST'])
def process_data():
    jd = request.json.get('JD')
    result = get_points(jd)
    replace_job_1(result)
    save_pdf()
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(debug=True)











