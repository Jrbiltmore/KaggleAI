"""
analysis_tools Module
---------------------
This module provides various tools for code analysis, including metrics calculation,
file operations, and security checks. Designed to support the development and maintenance
of high-quality, secure code.
"""

# Import submodules to make them accessible via analysis_tools.<module_name>
from . import code_metrics
from . import file_operations
from . import security_checks

# Optionally, define any shared resources or configurations here
# For example, a logger configured specifically for analysis purposes
import logging
logger = logging.getLogger('analysis_tools')
logger.setLevel(logging.INFO)

# Example of a higher-level function that abstracts individual tools for a common task
def perform_security_audit(code_path):
    """
    Performs a comprehensive security audit on the specified code directory.
    This is a high-level function that utilizes individual tools from the module.
    """
    logger.info("Starting security audit...")
    
    # Assuming these functions are defined in the respective submodules
    files = file_operations.list_all_files(code_path)
    for file in files:
        report = security_checks.analyze_security(file)
        logger.info(f"Security analysis for {file}: {report}")

    logger.info("Security audit complete.")

# Making key functionalities directly accessible via the module
__all__ = ['code_metrics', 'file_operations', 'security_checks', 'perform_security_audit']
