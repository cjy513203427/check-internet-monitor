"""
Monitoring Service Module
Manages continuous monitoring loop and state
"""
import time
import signal
import sys
from datetime import datetime
from detectors.certificate_detector import CertificateDetector


class MonitoringService:
    """Continuous monitoring service"""

    def __init__(self, translator, detectors, reporter, interval=30):
        """
        Initializes the monitoring service.

        Args:
            translator: Translator manager instance.
            detectors: List of detectors [(message, detector), ...].
            reporter: MonitorReporter instance.
            interval: Detection interval in seconds, default is 30 seconds.
        """
        self.translator = translator
        self.detectors = detectors
        self.reporter = reporter
        self.interval = interval
        self.previous_state = None
        self.running = False
        self.start_time = None
        self.cycle_count = 0
        self.last_cert_check = None
        self.cert_check_interval = 300  # 5 minutes

        # Register signal handler (Ctrl+C)
        signal.signal(signal.SIGINT, self._signal_handler)

    def start(self):
        """Starts continuous monitoring."""
        self.running = True
        self.start_time = datetime.now()

        # Print monitoring start information
        self.reporter.print_monitoring_header(self.interval)

        # First full detection cycle
        self.previous_state = self._run_detection_cycle(is_first=True)

        # Enter monitoring loop
        while self.running:
            time.sleep(self.interval)

            if not self.running:
                break

            current_state = self._run_detection_cycle()
            self._handle_changes(current_state)
            self.previous_state = current_state
            self.cycle_count += 1

    def _run_detection_cycle(self, is_first=False):
        """
        Executes one detection cycle.

        Args:
            is_first: Whether it is the first detection.

        Returns:
            list: List of detection results.
        """
        results = []

        for message, detector in self.detectors:
            # Special handling for certificate detection
            if isinstance(detector, CertificateDetector):
                if not self._should_run_certificate_check():
                    continue
                self.last_cert_check = datetime.now()

            try:
                result = detector.detect()
                results.append(result)
            except Exception as e:
                # Silently handle errors to avoid interrupting monitoring
                # Can choose to log to a file
                pass

        return results

    def _should_run_certificate_check(self):
        """
        Determines if the certificate check should be run.

        Returns:
            bool: True if it should run.
        """
        if self.last_cert_check is None:
            return True

        elapsed = (datetime.now() - self.last_cert_check).total_seconds()
        return elapsed >= self.cert_check_interval

    def _handle_changes(self, current_state):
        """
        Handles detected changes.

        Args:
            current_state: The current detection results.
        """
        from utils.change_detector import ChangeDetector

        detector = ChangeDetector(self.translator)
        changes = detector.detect_changes(self.previous_state, current_state)

        if changes['has_changes']:
            # Changes detected, print an alert
            self.reporter.print_change_alert(changes)
        else:
            # No changes, brief status update
            self.reporter.print_status_update(
                self.cycle_count + 1,
                datetime.now()
            )

    def _signal_handler(self, signum, frame):
        """
        Handles the Ctrl+C signal.

        Args:
            signum: Signal number.
            frame: Stack frame.
        """
        print(f"\n\n{self.translator.t('monitor.stopping')}")
        self.stop()
        sys.exit(0)

    def stop(self):
        """Stops monitoring."""
        self.running = False
