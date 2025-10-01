#!/usr/bin/env python3
"""
Resume Generator Script

This script reads resume data from a YAML file and generates a LaTeX resume.
Automatically generates PDF and creates timestamped backups.
"""

import yaml
import argparse
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from jinja2 import Template

def load_resume_data(yaml_file: str) -> dict:
    """Load resume data from YAML file."""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_latex_resume(data: dict, template_file: str, output_file: str):
    """Generate LaTeX resume from data and template."""
    from jinja2 import Environment, FileSystemLoader

    # Get template directory and filename
    template_dir = str(Path(template_file).parent)
    template_name = Path(template_file).name

    # Create Jinja2 environment with LaTeX-safe delimiters
    env = Environment(
        loader=FileSystemLoader(template_dir),
        variable_start_string='<<',
        variable_end_string='>>',
        block_start_string='<BLOCK>',
        block_end_string='</BLOCK>',
        comment_start_string='<#',
        comment_end_string='#>'
    )

    # Add LaTeX escape filter
    def latex_escape(text):
        """Escape LaTeX special characters."""
        if not isinstance(text, str):
            text = str(text)

        # Basic LaTeX character escaping - order matters!
        # Do backslash first, then others
        text = text.replace('\\', r'\textbackslash{}')
        text = text.replace('&', r'\&')
        text = text.replace('%', r'\%')
        text = text.replace('$', r'\$')
        text = text.replace('#', r'\#')
        text = text.replace('^', r'\textasciicircum{}')
        text = text.replace('_', r'\_')
        text = text.replace('{', r'\{')
        text = text.replace('}', r'\}')
        text = text.replace('~', r'\textasciitilde{}')

        return text

    env.filters['latex_escape'] = latex_escape

    template = env.get_template(template_name)
    rendered = template.render(**data)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rendered)

def compile_pdf(tex_file: str, output_name: str = "Resume") -> bool:
    """Compile LaTeX file to PDF using pdflatex."""
    try:
        # Run pdflatex twice for proper reference resolution
        for _ in range(2):
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_file],
                capture_output=True,
                text=True,
                cwd=Path(tex_file).parent
            )
            if result.returncode != 0:
                print(f"LaTeX compilation error: {result.stderr}")
                return False

        # Rename the output PDF to our desired name
        tex_path = Path(tex_file)
        generated_pdf = tex_path.with_suffix('.pdf')
        target_pdf = tex_path.parent / f"{output_name}.pdf"

        if generated_pdf.exists():
            shutil.move(str(generated_pdf), str(target_pdf))

        # Clean up auxiliary files
        aux_extensions = ['.aux', '.out', '.fls', '.fdb_latexmk']
        for ext in aux_extensions:
            aux_file = tex_path.with_suffix(ext)
            if aux_file.exists():
                aux_file.unlink()

        return True
    except Exception as e:
        print(f"Error compiling PDF: {e}")
        return False

def create_backup(pdf_file: str, backup_dir: str = "backups"):
    """Create timestamped backup of the PDF."""
    pdf_path = Path(pdf_file)
    if not pdf_path.exists():
        print(f"Warning: PDF file {pdf_file} not found for backup")
        return

    backup_path = Path(backup_dir)
    backup_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{pdf_path.stem}_{timestamp}.pdf"
    backup_file = backup_path / backup_name

    shutil.copy2(str(pdf_path), str(backup_file))
    print(f"Backup created: {backup_file}")

def main():
    parser = argparse.ArgumentParser(description='Generate LaTeX resume from YAML data')
    parser.add_argument('--data', '-d', default='resume_data.yaml',
                       help='YAML file containing resume data')
    parser.add_argument('--template', '-t', default='resume_template.tex',
                       help='LaTeX template file')
    parser.add_argument('--output', '-o', default='resume.tex',
                       help='Output LaTeX file')
    parser.add_argument('--pdf-name', default='Resume',
                       help='Name for the generated PDF (without .pdf extension)')
    parser.add_argument('--backup-dir', default='backups',
                       help='Directory for timestamped backups')
    parser.add_argument('--no-pdf', action='store_true',
                       help='Skip PDF generation')
    parser.add_argument('--no-backup', action='store_true',
                       help='Skip creating backup')

    args = parser.parse_args()

    # Check if files exist
    data_path = Path(args.data)
    template_path = Path(args.template)

    if not data_path.exists():
        print(f"Error: Data file {args.data} not found")
        return 1

    if not template_path.exists():
        print(f"Error: Template file {args.template} not found")
        return 1

    try:
        # Load data and generate resume
        data = load_resume_data(args.data)
        generate_latex_resume(data, args.template, args.output)
        print(f"LaTeX resume generated: {args.output}")

        # Generate PDF unless disabled
        if not args.no_pdf:
            if compile_pdf(args.output, args.pdf_name):
                pdf_file = f"{args.pdf_name}.pdf"
                print(f"PDF generated: {pdf_file}")

                # Create backup unless disabled
                if not args.no_backup:
                    create_backup(pdf_file, args.backup_dir)
            else:
                print("PDF generation failed")
                return 1

        return 0
    except Exception as e:
        print(f"Error generating resume: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
