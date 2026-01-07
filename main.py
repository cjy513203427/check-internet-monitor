"""
Network Monitoring Detection Tool
Main entry point for detecting network monitoring and surveillance
"""
import argparse
import sys
from detectors.proxy_detector import ProxyDetector
from detectors.process_detector import ProcessDetector
from detectors.network_detector import NetworkDetector
from detectors.connection_detector import ConnectionDetector
from detectors.certificate_detector import CertificateDetector
from utils.reporter import Reporter
from utils.i18n import translator


def main():
    parser = argparse.ArgumentParser(
        description=translator.t('cli.description'),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=translator.t('cli.epilog')
    )

    parser.add_argument(
        '--json',
        metavar='FILE',
        help=translator.t('cli.help_json')
    )

    parser.add_argument(
        '--quick',
        action='store_true',
        help=translator.t('cli.help_quick')
    )

    parser.add_argument(
        '--lang',
        choices=['zh', 'en'],
        default='zh',
        help=translator.t('cli.help_lang')
    )

    args = parser.parse_args()

    # Update language based on user selection
    translator.set_language(args.lang)

    print(translator.t('progress.starting'))
    print(translator.t('progress.please_wait'))

    # Initialize reporter
    reporter = Reporter(translator)

    # Run all detectors
    detectors = [
        (translator.t('progress.checking_proxy'), ProxyDetector(translator)),
        (translator.t('progress.scanning_processes'), ProcessDetector(translator)),
        (translator.t('progress.analyzing_network'), NetworkDetector(translator)),
        (translator.t('progress.examining_connections'), ConnectionDetector(translator)),
    ]

    # Add certificate detector if not in quick mode
    if not args.quick:
        detectors.append((translator.t('progress.testing_certificates'), CertificateDetector(translator)))
    else:
        print(translator.t('progress.skipping_certificates'))

    # Run each detector
    for message, detector in detectors:
        print(message)
        try:
            result = detector.detect()
            reporter.add_result(result)
        except Exception as e:
            print(translator.t('messages.detector_error', detector=detector.__class__.__name__, error=str(e)))
            reporter.add_result({
                "name": detector.__class__.__name__,
                "risk_level": "LOW",
                "findings": [{
                    "type": "Error",
                    "detail": translator.t('templates.failed_to_run', error=str(e)),
                    "severity": "INFO"
                }]
            })

    # Print report
    reporter.print_report()

    # Export to JSON if requested
    if args.json:
        reporter.export_json(args.json)

    print("\n" + translator.t('messages.note'))
    print(translator.t('messages.note2'))
    print(translator.t('messages.note3'))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(translator.t('messages.cancelled'))
        sys.exit(0)
    except Exception as e:
        print(translator.t('messages.fatal_error', error=str(e)))
        sys.exit(1)
