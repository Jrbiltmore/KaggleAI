"""
Enhanced code_metrics Module
----------------------------
Extensively analyzes Python projects for quality, complexity, and potential issues. 
It integrates Radon for in-depth metrics and complexity analysis, and leverages flake8
for code quality checks, providing a comprehensive quality report.
"""

import os
import json
import subprocess
from glob import iglob
from radon.raw import analyze as radon_analyze
from radon.complexity import cc_visit, cc_rank
from radon.metrics import mi_visit
from typing import List, Dict

def analyze_file_with_radon(file_path: str) -> Dict:
    """
    Analyzes a single file with Radon, extracting metrics, cyclomatic complexity,
    and maintainability index.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    analysis_results = radon_analyze(content)
    complexity_results = cc_visit(content)
    maintainability_index = mi_visit(content, analysis_results.multi)

    complexity_scores = [
        (fn.name, fn.complexity, cc_rank(fn.complexity))
        for fn in complexity_results
    ]

    return {
        'file_path': file_path,
        'total_lines': analysis_results.loc,
        'code_lines': analysis_results.lloc,
        'comment_lines': analysis_results.comments,
        'comment_density': analysis_results.comments / analysis_results.lloc if analysis_results.lloc else 0,
        'complexity_scores': complexity_scores,
        'maintainability_index': maintainability_index
    }

def analyze_directory_with_radon(directory_path: str, file_pattern: str = "*.py") -> List[Dict]:
    """
    Aggregates Radon metrics and analysis across all Python files in a directory.
    """
    files = iglob(os.path.join(directory_path, "**", file_pattern), recursive=True)
    return [analyze_file_with_radon(file_path) for file_path in files]

def run_flake8_analysis(directory_path: str) -> Dict:
    """
    Runs flake8 analysis on a directory, capturing output for report inclusion.
    """
    try:
        result = subprocess.run(['flake8', directory_path, '--format=json'], capture_output=True, text=True)
        if result.stdout.strip():
            return json.loads(result.stdout)
        else:
            print("flake8 did not return any output.")
            return {}
    except subprocess.CalledProcessError as e:
        print(f"Error running flake8: {e}")
    except json.JSONDecodeError as e:
        print(f"Failed to decode flake8 output as JSON: {e}")
    return {}

def generate_summary_report(directory_path: str) -> Dict:
    """
    Generates a comprehensive summary report based on Radon metrics and flake8 analysis.
    """
    metrics_list = analyze_directory_with_radon(directory_path)
    flake8_violations = run_flake8_analysis(directory_path)

    report = {
        'total_files_analyzed': len(metrics_list),
        'total_code_lines': sum(m['code_lines'] for m in metrics_list),
        'average_comment_density': sum(m['comment_density'] for m in metrics_list) / len(metrics_list) if metrics_list else 0,
        'functions_with_high_complexity': [
            (m['file_path'], fn[0], fn[1], fn[2]) for m in metrics_list for fn in m['complexity_scores'] if fn[1] > 10
        ],
        'maintainability_index_average': sum(m['maintainability_index'] for m in metrics_list) / len(metrics_list) if metrics_list else 0,
        'flake8_violations': flake8_violations
    }

    return report

# Example usage
if __name__ == "__main__":
    directory_path = './path/to/your/code_directory'
    summary_report = generate_summary_report(directory_path)
    print(json.dumps(summary_report, indent=4))
