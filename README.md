# Resume Generator

A Python-based resume generation system that uses YAML for data and Jinja2 templates for LaTeX output.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Edit your resume data in `resume_data.yaml`
2. Generate your resume:
```bash
python generate_resume.py
```

Or with custom file paths:
```bash
python generate_resume.py --data resume_data.yaml --template resume_template.tex --output resume.tex

```

3. Compile the LaTeX file to PDF:
```bash
pdflatex resume.tex
```

## File Structure

- `resume_data.yaml` - Your resume data in YAML format
- `resume_template.tex` - LaTeX template with Jinja2 variables
- `generate_resume.py` - Python script to generate LaTeX from YAML
- `requirements.txt` - Python dependencies
- `AndrewResumeWorkshop.tex` - Original resume file (for reference)

## Editing Resume Data

All resume content is stored in `resume_data.yaml`. The structure includes:

- `personal_info` - Name, contact information, links
- `education` - Educational background
- `experience` - Work experience with achievements
- `projects` - Personal/academic projects
- `skills` - Technical skills organized by category

## Benefits

- **Separation of Content and Format**: Edit content in YAML, format stays in LaTeX template
- **Version Control Friendly**: YAML is easier to track changes than LaTeX
- **Reusable**: Can generate different resume formats from same data
- **Maintainable**: Update content without touching LaTeX formatting
