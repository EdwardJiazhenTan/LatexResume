# Resume Generator

A Python-based resume generation system using YAML data and LaTeX templates.

## Setup

1. **Clone and navigate**
   ```bash
   git clone <repository-url>
   cd Resume
   ```

2. **Install LaTeX**
   - macOS: `brew install --cask mactex`
   - Ubuntu: `sudo apt-get install texlive-full`
   - Windows: Install MiKTeX or TeX Live

3. **Setup Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Generate resume**
   ```bash
   python3 generate_resume.py
   ```

## Customization

6. **Edit content**: Modify `resume_data.yaml` with your information

7. **Personalize output**: 
   - Change PDF filename in `generate_resume.py` (line 69, default: "Resume")
   - Adjust link display text in `resume_template.tex` header section

## Branch Structure

- `master` - Public template with placeholder data
- `personal` - Your personal information (keep local)
- `experiment-*` - Experimental layout branches

## File Structure

- `resume_data.yaml` - Resume content in YAML
- `resume_template.tex` - LaTeX template with Jinja2 variables
- `generate_resume.py` - Generation script
- `requirements.txt` - Python dependencies
