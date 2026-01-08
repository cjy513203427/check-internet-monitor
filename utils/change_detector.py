"""
Change Detector Module
Compares detection results to identify new threats and changes
"""
from datetime import datetime


class ChangeDetector:
    """Detects changes between two scan results."""

    def __init__(self, translator):
        self.translator = translator

    def detect_changes(self, previous_results, current_results):
        """
        Detects changes between two sets of results.

        Args:
            previous_results: The previous list of detection results.
            current_results: The current list of detection results.

        Returns:
            dict: A change report, including new findings, risk level changes, etc.
        """
        if previous_results is None:
            return {'has_changes': False}

        changes = {
            'has_changes': False,
            'new_findings': [],
            'removed_findings': [],
            'risk_changes': [],
            'timestamp': datetime.now()
        }

        # Create a lookup dictionary for previous results
        prev_by_name = {r['name']: r for r in previous_results}

        for current_result in current_results:
            name = current_result['name']
            prev_result = prev_by_name.get(name)

            if prev_result is None:
                continue

            # Detect new findings
            new_finds = self._find_new_findings(
                prev_result['findings'],
                current_result['findings']
            )

            if new_finds:
                changes['has_changes'] = True
                changes['new_findings'].append({
                    'module': name,
                    'findings': new_finds,
                    'severity': self._get_highest_severity(new_finds)
                })

            # Detect removed findings
            removed_finds = self._find_removed_findings(
                prev_result['findings'],
                current_result['findings']
            )
            if removed_finds:
                changes['has_changes'] = True
                changes['removed_findings'].append({
                    'module': name,
                    'findings': removed_finds,
                    'severity': self._get_highest_severity(removed_finds)
                })

            # Detect risk level changes
            if prev_result['risk_level'] != current_result['risk_level']:
                changes['has_changes'] = True
                changes['risk_changes'].append({
                    'module': name,
                    'from': prev_result['risk_level'],
                    'to': current_result['risk_level']
                })

        return changes

    def _find_new_findings(self, prev_findings, curr_findings):
        """
        Finds new findings.

        Args:
            prev_findings: The previous list of findings.
            curr_findings: The current list of findings.

        Returns:
            list: A list of new findings.
        """
        # Convert findings to comparable strings
        prev_set = {self._finding_key(f) for f in prev_findings}
        new_findings = []

        for finding in curr_findings:
            key = self._finding_key(finding)
            if key not in prev_set:
                new_findings.append(finding)

        return new_findings

    def _find_removed_findings(self, prev_findings, curr_findings):
        """
        Finds removed findings.

        Args:
            prev_findings: The previous list of findings.
            curr_findings: The current list of findings.

        Returns:
            list: A list of removed findings.
        """
        curr_set = {self._finding_key(f) for f in curr_findings}
        removed_findings = []

        for finding in prev_findings:
            key = self._finding_key(finding)
            if key not in curr_set:
                removed_findings.append(finding)

        return removed_findings

    def _finding_key(self, finding):
        """
        Generates a unique key for a finding.

        Args:
            finding: The finding dictionary.

        Returns:
            str: A unique identifier string.
        """
        return f"{finding['type']}|{finding['detail']}"

    def _get_highest_severity(self, findings):
        """
        Gets the highest severity level from a list of findings.

        Args:
            findings: A list of findings.

        Returns:
            str: The highest severity level (HIGH/MEDIUM/LOW/INFO).
        """
        severity_order = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1, 'INFO': 0}
        max_severity = 'INFO'
        max_value = 0

        for f in findings:
            value = severity_order.get(f['severity'], 0)
            if value > max_value:
                max_value = value
                max_severity = f['severity']

        return max_severity
