# Python Scripts Collection

This repository contains a collection of utility Python scripts for various tasks including file processing, machine learning, Git management, FTP uploads, and more.

## Scripts Overview

### 1. **copy_translations.py**
**Purpose:** Language translation file management utility

Recursively copies all property and JSON translation files from a specified folder to a temporary location, compresses them into a ZIP archive, and sends the file to a configured FTP server.

**Key Features:**
- Filters property files by language code (e.g., en, es, cn)
- Supports both `.properties` and `.json` file formats
- Automatic ZIP compression with organized directory structure
- FTP upload capability
- Configurable via `copy_translations.properties`

**Usage:** `python copy_translations.py <path> [<languages>]`

---

### 2. **gitcopybranches.py**
**Purpose:** Git repository branch management automation

Automates complex Git branch operations including copying branches, renaming branches, and reorganizing repository structure.

**Key Features:**
- Creates develop branch from master
- Replaces master from a specified branch while retaining history
- Renames release branches with `release/` prefix
- Renames feature branches with `feature/` prefix and JIRA IDs
- Automated push operations

**Use Case:** Reorganizing Git repository structure and branch naming conventions

---

### 3. **html2txt.py**
**Purpose:** HTML to text file converter

Converts HTML files to plain text by extracting and writing text content, removing all HTML tags and formatting.

**Key Features:**
- Uses BeautifulSoup for parsing HTML
- Outputs UTF-8 encoded text file with same basename as input
- Preserves text structure without HTML markup

**Usage:** `python html2txt.py <html_filename>`

---

### 4. **perf.py**
**Purpose:** Process performance log analyzer

Analyzes Boomi process logs to identify time-consuming operations by measuring time intervals between log entries.

**Key Features:**
- Parses timestamped log entries
- Calculates time duration between consecutive log lines
- Filters entries exceeding 2-second threshold
- Sorts results by duration in descending order
- Formats output for easy performance analysis

**Usage:** `python perf.py [<log_file_path>]`

**Default:** Reads from `c:\temp\process.log`

---

### 5. **ren.py**
**Purpose:** Batch file rename utility

Renames files in a directory structure by removing leading spaces and consolidating multiple spaces into single spaces.

**Key Features:**
- Recursively processes all files in directory tree
- Removes leading whitespace from filenames
- Collapses multiple consecutive spaces into single spaces
- Useful for cleaning up poorly named file collections

**Configuration:** Update the `path` variable to target directory before running

---

### 6. **SVM_vs_RF.py**
**Purpose:** Machine learning model comparison and optimization

Compares performance of multiple regression models: SVM, Random Forest, and XGBoost using GridSearchCV for hyperparameter tuning.

**Key Features:**
- Support for Random Forest Regressor, XGBoost Regressor, and SVM
- GridSearchCV for parameter optimization
- Uses diabetes dataset from scikit-learn
- RobustScaler for data preprocessing
- Performance metrics printing

**Models Compared:**
- Random Forest Regressor
- XGBoost Regressor
- Support Vector Machine (SVM) Regressor

---

### 7. **test_jira_integration.py**
**Purpose:** JIRA and PSS system integration testing

Integrates with JIRA and PSS (PowerSteering) systems to retrieve and compare sprint and issue data across platforms.

**Key Features:**
- Fetches JIRA issues from specified sprints using JQL queries
- Retrieves PSS sprint data via REST API
- Supports filtering by issue type (Bug, Story)
- Handles authentication for both systems
- Configurable via constants at script top

**Requirements:** Valid JIRA and PSS credentials and URLs

---

### 8. **upload2artifactory.py**
**Purpose:** Maven artifact deployment to Artifactory

Uploads JAR files from local Maven repository to remote Artifactory or AWS CodeArtifact repositories.

**Key Features:**
- Scans local Maven repository structure
- Supports bulk upload of entire repository
- Integration with AWS CodeArtifact authentication tokens
- Uses curl for file transfer
- Configurable upload enable/disable for testing

**Configuration Variables:**
- `SUB_FOLDERS_TO_UPLOAD`: List of folders to upload
- `ARTIFACTORY_URL`: Target repository URL
- `ENABLE_UPLOAD`: Toggle actual uploads

---

### 9. **upload2codeartifact.py**
**Purpose:** Maven artifact deployment to AWS CodeArtifact

Automates JAR file deployment to AWS CodeArtifact by extracting POM metadata and using Maven deployment commands.

**Key Features:**
- Extracts metadata from POM files (groupId, artifactId, version)
- Recursively traverses local Maven repository
- Matches POM files with corresponding JAR files
- Executes Maven deploy commands via `mvn.cmd`
- Namespace-aware XML parsing

**Usage:** Run without arguments; configures repository path internally

---

### 10. **usage_report.py**
**Purpose:** Customer environment usage reporting

Generates usage reports by querying SQL Server databases and distributes them via email with CSV attachments.

**Key Features:**
- Executes SQL queries across multiple databases
- Maps databases to customer names
- Generates CSV report files
- Email delivery with attachment support
- Configurable via `usage_report.properties`
- Logging to file
- Supports multiple mail recipients

**Requirements:** SQL Server access and SMTP server configuration

---

### 11. **xgbreg.py**
**Purpose:** Generic XGBoost regression model with hyperparameter tuning

Implements a flexible XGBoost regression template for predicting continuous values with GridSearchCV optimization capabilities.

**Key Features:**
- Configurable XGBoost parameters
- GridSearchCV for hyperparameter optimization
- Supports multiple datasets (California housing, diabetes)
- Calculates MSE and R² score metrics
- Train-test split validation
- Parameter discovery workflow for optimal performance

**Workflow:**
1. Update `get_data()` method for your dataset
2. Run `grid_search()` to find best parameters
3. Update parameters in `train_xgbr()` method
4. Use `train_predict()` for training and validation

---

### 12. **zipextract.py**
**Purpose:** Selective ZIP file extraction and 7z compression

Extracts files from ZIP archives based on modification date and recompresses them using 7z compression.

**Key Features:**
- Extracts ZIP files modified after specified date
- Supports date filtering in format (dd-mmm-yyyy)
- Clears target extraction folder before extraction
- Compresses extracted files using 7z with AES encryption
- Automatic cleanup of extracted files post-compression

**Usage:** `python zipextract.py <date>`

**Example:** `python zipextract.py 1-oct-2017`

---

## Dependencies

Common dependencies across scripts:
- `requests` - HTTP library (test_jira_integration.py)
- `lxml` - XML parsing (test_jira_integration.py)
- `beautifulsoup4` - HTML parsing (html2txt.py)
- `scikit-learn` - Machine learning (SVM_vs_RF.py, xgbreg.py)
- `xgboost` - Gradient boosting (SVM_vs_RF.py, xgbreg.py)
- `pandas` - Data manipulation (xgbreg.py)
- `python-dateutil` - Date parsing (perf.py)

Standard library modules used: `os`, `sys`, `subprocess`, `ftplib`, `tempfile`, `shutil`, `logging`, `re`, `email`, `smtplib`, `zipfile`, `xml.etree`, `datetime`, `pathlib`, `configparser`

## Installation

Install required dependencies:
```bash
pip install requests lxml beautifulsoup4 scikit-learn xgboost pandas python-dateutil
```

## Notes

- Several scripts require external configuration files (e.g., `.properties` files)
- Some scripts contain hardcoded paths that may need adjustment for your environment
- FTP and email-based scripts require valid credentials and server configurations
- Database scripts require SQL Server and appropriate access permissions

## Author

Original Author: Ranjith Karunakaran

---

*Last Updated: February 2026*" 
