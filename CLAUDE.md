# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python-based network monitoring detection tool that identifies potential surveillance on a system by detecting:
- Proxy configurations (environment variables, Windows registry)
- Monitoring/packet capture processes (Wireshark, Fiddler, etc.)
- Virtual network adapters and VPN connections
- Suspicious listening ports and network connections
- TLS/SSL certificate anomalies indicating MITM attacks

## Running the Tool

```bash
# Basic usage (Chinese output, default)
python main.py

# English output
python main.py --lang en

# Quick mode (skips slow certificate checks)
python main.py --quick

# Export results to JSON
python main.py --json report.json

# All options combined
python main.py --lang en --quick --json results.json

# View help
python main.py -h
```

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Or with conda
conda activate stock_api
pip install -r requirements.txt
```

## Architecture

### Detector Pattern

All detection modules follow a consistent pattern:

1. **Location**: `detectors/` directory
2. **Constructor**: Each detector accepts a `translator` parameter for i18n support
3. **detect() Method**: Returns a standardized dictionary:
   ```python
   {
       "name": str,           # Translated module name
       "risk_level": str,     # "HIGH", "MEDIUM", or "LOW"
       "findings": [          # List of finding dictionaries
           {
               "type": str,       # Finding category (kept in English for JSON)
               "detail": str,     # Specific details
               "severity": str    # "HIGH", "MEDIUM", "LOW", or "INFO"
           }
       ]
   }
   ```

**Existing Detectors:**
- `ProxyDetector`: Environment variables + Windows registry proxy settings
- `ProcessDetector`: Scans running processes against known monitoring tools
- `NetworkDetector`: Virtual adapters, VPN detection via port analysis
- `ConnectionDetector`: Suspicious listening ports, established connections
- `CertificateDetector`: TLS/SSL certificate validation to detect MITM

### Translation System (i18n)

**Critical Design Decision**: Translation happens at the display layer only. Internal data structures always use English values.

**Implementation** (`utils/i18n.py`):
- `TranslationManager` class with singleton pattern (`translator` instance)
- Nested dictionaries for `zh` and `en` translations
- `translator.t(key, **kwargs)` - dot notation keys with variable substitution
- `translator.set_language(lang)` - switch language dynamically

**Translation Categories**:
- `cli.*` - Command-line interface text
- `progress.*` - Status messages during execution
- `modules.*` - Detector module names
- `findings.*` - Finding type labels
- `templates.*` - Dynamic messages with placeholders
- `report.*` - Report section labels
- `risk_levels.*` - HIGH/MEDIUM/LOW translations
- `severity_levels.*` - Severity level translations
- `messages.*` - Error messages, notes, disclaimers

**JSON Export**: Always uses English values (e.g., "HIGH", not "高") for API stability.

### Reporter System

**Location**: `utils/reporter.py`

**Responsibilities**:
- Aggregates results from all detectors
- Calculates overall risk level (highest among all modules)
- Prints colored terminal output with translations
- Exports JSON reports with untranslated data

**Key Methods**:
- `add_result(result)` - Add detector result
- `print_report()` - Display formatted, translated report
- `export_json(filename)` - Save JSON with English values
- `_calculate_overall_risk()` - Risk level aggregation logic

### Main Entry Point

**Flow** (`main.py`):
1. Parse CLI arguments (including `--lang`)
2. Set translator language
3. Initialize `Reporter` with translator
4. Instantiate all detectors with translator
5. Run each detector, catch exceptions
6. Print report, export JSON if requested

## Adding a New Detector

1. Create file in `detectors/` directory
2. Implement class with `__init__(self, translator)` constructor
3. Store `self.translator = translator`
4. Implement `detect(self)` method returning the standard dict format
5. Use `self.translator.t('modules.your_module_name')` for module name
6. Add translations to `utils/i18n.py` in both `zh` and `en` sections:
   - Module name in `modules.*`
   - Finding types in `findings.*`
   - Detail templates in `templates.*`
7. Import and instantiate in `main.py` detector list
8. Pass `translator` to constructor

## Adding New Translations

**Location**: `utils/i18n.py` in `TRANSLATIONS` dict

**Process**:
1. Add key-value pairs to both `zh` and `en` dictionaries
2. Maintain identical structure in both language sections
3. For dynamic messages, use `{variable}` placeholders
4. Call with: `translator.t('category.key', variable=value)`

**Example**:
```python
# In TRANSLATIONS
'zh': {
    'templates': {
        'new_finding': '发现 {count} 个 {type}'
    }
}
'en': {
    'templates': {
        'new_finding': 'Found {count} {type}'
    }
}

# In code
translator.t('templates.new_finding', count=5, type='proxies')
```

## Important Implementation Notes

1. **Risk Level vs Severity**:
   - Risk Level: Module-level assessment (detector.risk_level)
   - Severity: Individual finding-level assessment (finding['severity'])
   - Both use: HIGH, MEDIUM, LOW (+ INFO for severity)

2. **Windows-Specific Code**:
   - Registry access in `proxy_detector.py` (uses `winreg` module)
   - Gracefully handles `ImportError` on non-Windows platforms

3. **Permission Handling**:
   - Many detectors require elevated privileges for complete results
   - Use try/except with `psutil.AccessDenied` and `PermissionError`
   - Report permission issues as INFO-level findings, not errors

4. **Error Handling**:
   - Detector exceptions caught in main loop
   - Errors reported as findings with severity "INFO"
   - Tool continues execution even if individual detectors fail

5. **Color Coding** (via colorama):
   - HIGH risk/severity: Red
   - MEDIUM: Yellow
   - LOW: Cyan/Green
   - INFO: White

## Code Style Notes

- Finding types stored in English (e.g., "Environment Proxy", "Suspicious Process")
- Detail strings can be in either language (dynamic/template-based)
- Module names returned as translated strings
- Risk/severity levels stay as English constants in data, translated only for display
