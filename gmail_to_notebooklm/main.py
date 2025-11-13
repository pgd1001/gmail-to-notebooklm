"""Command-line interface for Gmail to NotebookLM converter."""

import json
import os
import sys
from pathlib import Path
from typing import Optional

import click

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    # Set console mode for ANSI escape codes
    os.system('')

from gmail_to_notebooklm import __version__
from gmail_to_notebooklm.auth import authenticate, AuthenticationError
from gmail_to_notebooklm.config import load_config, ConfigError
from gmail_to_notebooklm.core import ExportEngine, ProgressUpdate, ExportResult
from gmail_to_notebooklm.gmail_client import GmailClient, GmailAPIError
from gmail_to_notebooklm.utils import get_env_or_default


# Exit codes
EXIT_SUCCESS = 0
EXIT_CONFIG_ERROR = 1
EXIT_AUTH_ERROR = 2
EXIT_API_ERROR = 3
EXIT_NO_RESULTS = 4
EXIT_EXPORT_ERROR = 5
EXIT_USER_CANCEL = 130


@click.command()
@click.option(
    "--config",
    "-c",
    default=None,
    type=click.Path(exists=True),
    help="Path to YAML configuration file",
)
@click.option(
    "--label",
    "-l",
    default=None,
    help="Gmail label to export (case-sensitive)",
)
@click.option(
    "--query",
    "-q",
    default=None,
    help="Gmail search query (uses Gmail search syntax)",
)
@click.option(
    "--after",
    default=None,
    help="Filter emails after this date (YYYY-MM-DD or YYYY/MM/DD)",
)
@click.option(
    "--before",
    default=None,
    help="Filter emails before this date (YYYY-MM-DD or YYYY/MM/DD)",
)
@click.option(
    "--from",
    "from_",
    default=None,
    help="Filter emails from sender(s) (comma-separated)",
)
@click.option(
    "--to",
    default=None,
    help="Filter emails to recipient(s) (comma-separated)",
)
@click.option(
    "--exclude-from",
    default=None,
    help="Exclude emails from sender(s) (comma-separated)",
)
@click.option(
    "--output-dir",
    "-o",
    default=None,
    type=click.Path(),
    help="Output directory for Markdown files (default: ./output)",
)
@click.option(
    "--max-results",
    "-m",
    default=None,
    type=int,
    help="Maximum number of emails to process (default: unlimited)",
)
@click.option(
    "--credentials",
    default=None,
    type=click.Path(exists=True),
    help="Path to credentials.json (default: ./credentials.json)",
)
@click.option(
    "--token",
    default=None,
    type=click.Path(),
    help="Path to save/load token (default: ./token.json)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
@click.option(
    "--overwrite",
    is_flag=True,
    help="Overwrite existing files",
)
@click.option(
    "--create-index",
    is_flag=True,
    help="Create INDEX.md file with table of contents",
)
@click.option(
    "--organize-by-date",
    is_flag=True,
    help="Organize files into date-based subdirectories",
)
@click.option(
    "--date-format",
    default="YYYY/MM",
    type=click.Choice(["YYYY/MM", "YYYY-MM", "YYYY/MM/DD", "YYYY-MM-DD"], case_sensitive=False),
    help="Date format for organization (default: YYYY/MM)",
)
@click.option(
    "--consolidate",
    is_flag=True,
    help="Create single consolidated Markdown file instead of individual files",
)
@click.option(
    "--consolidation-filename",
    default="export.md",
    help="Filename for consolidated document (default: export.md)",
)
@click.option(
    "--consolidation-title",
    default=None,
    help="Title for consolidated document (default: 'Email Export')",
)
@click.option(
    "--consolidation-mode",
    default="all",
    type=click.Choice(["all", "thread", "date", "sender", "recipient"], case_sensitive=False),
    help="Grouping strategy for consolidation (default: all)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Validate settings and show what would be exported without actually exporting",
)
@click.option(
    "--quiet",
    is_flag=True,
    help="Suppress all output except errors (useful for CI/CD)",
)
@click.option(
    "--json-output",
    is_flag=True,
    help="Output results in JSON format (useful for scripting)",
)
@click.option(
    "--list-labels",
    is_flag=True,
    help="List all available Gmail labels and exit",
)
@click.version_option(version=__version__)
def cli(
    config: Optional[str],
    label: Optional[str],
    query: Optional[str],
    after: Optional[str],
    before: Optional[str],
    from_: Optional[str],
    to: Optional[str],
    exclude_from: Optional[str],
    output_dir: Optional[str],
    max_results: Optional[int],
    credentials: Optional[str],
    token: Optional[str],
    verbose: bool,
    overwrite: bool,
    create_index: bool,
    organize_by_date: bool,
    date_format: str,
    consolidate: bool,
    consolidation_filename: str,
    consolidation_title: Optional[str],
    consolidation_mode: str,
    dry_run: bool,
    quiet: bool,
    json_output: bool,
    list_labels: bool,
):
    """
    Convert Gmail emails from a label to Markdown files for NotebookLM.

    Exports emails from the specified Gmail label and converts them to
    clean Markdown format with headers (From, To, Subject, Date) and
    converted HTML body content.

    Example:

        gmail-to-notebooklm --label "Client A" --output-dir "./exports"

    First run will open a browser for Gmail authorization.
    """
    try:
        # Handle quiet mode
        def log(message: str, err: bool = False):
            """Log message unless in quiet mode."""
            if not quiet:
                click.echo(message, err=err)

        # Handle JSON output mode
        json_result = {}

        # Load configuration
        try:
            cfg = load_config(config)
            if verbose and not quiet:
                log(f"Loaded configuration from: {cfg.config_path or 'defaults'}")
        except ConfigError as e:
            log(f"✗ Configuration error: {e}", err=True)
            sys.exit(EXIT_CONFIG_ERROR)

        # Merge CLI args with config (CLI takes precedence)
        cli_args = {
            "label": label,
            "query": query,
            "after": after,
            "before": before,
            "from": from_,
            "to": to,
            "exclude_from": exclude_from,
            "output_dir": output_dir,
            "max_results": max_results,
            "credentials": credentials,
            "token": token,
            "verbose": verbose,
            "overwrite": overwrite,
            "create_index": create_index,
            "organize_by_date": organize_by_date,
            "date_format": date_format,
            "consolidate": consolidate,
            "consolidation_filename": consolidation_filename,
            "consolidation_title": consolidation_title,
            "consolidation_mode": consolidation_mode,
        }
        settings = cfg.merge_with_cli_args(cli_args)

        # Use credentials/token from settings or defaults
        credentials_path = settings.get("credentials", "credentials.json")
        token_path = settings.get("token", "token.json")

        # Handle --list-labels command
        if list_labels:
            log("Authenticating with Gmail...")
            try:
                creds = authenticate(credentials_path=credentials_path, token_path=token_path)
                client = GmailClient(creds)
                labels = client.list_labels()

                if json_output:
                    print(json.dumps({"labels": labels}, indent=2))
                else:
                    log("\nAvailable Gmail labels:")
                    log("=" * 50)
                    for l in sorted(labels):
                        log(f"  • {l}")
                    log("=" * 50)
                    log(f"\nTotal: {len(labels)} labels")

                sys.exit(EXIT_SUCCESS)

            except AuthenticationError as e:
                log(f"✗ Authentication failed: {e}", err=True)
                if json_output:
                    print(json.dumps({"error": str(e), "exit_code": EXIT_AUTH_ERROR}))
                sys.exit(EXIT_AUTH_ERROR)
            except GmailAPIError as e:
                log(f"✗ API error: {e}", err=True)
                if json_output:
                    print(json.dumps({"error": str(e), "exit_code": EXIT_API_ERROR}))
                sys.exit(EXIT_API_ERROR)

        # Determine output directory with fallback
        if settings.get("output_dir") is None:
            settings["output_dir"] = get_env_or_default("GMAIL_TO_NBL_OUTPUT_DIR", "./output")

        # Set default consolidation title if not provided
        if consolidate and not consolidation_title:
            settings["consolidation_title"] = "Email Export"
        elif consolidate and consolidation_title:
            settings["consolidation_title"] = consolidation_title

        # Validate required fields
        if not settings.get("label") and not settings.get("query") and not after and not before and not from_ and not to:
            log(
                "✗ Error: At least one filter is required: --label, --query, --after, --before, --from, or --to",
                err=True,
            )
            if json_output:
                print(json.dumps({"error": "No filters specified", "exit_code": EXIT_CONFIG_ERROR}))
            sys.exit(EXIT_CONFIG_ERROR)

        # Show export info
        if verbose and not quiet:
            log(f"Gmail to NotebookLM Converter v{__version__}")
            if settings.get("label"):
                log(f"Label: {settings['label']}")
            if settings.get("query"):
                log(f"Query: {settings['query']}")
            if after:
                log(f"After: {after}")
            if before:
                log(f"Before: {before}")
            log(f"Output directory: {settings['output_dir']}")
            if max_results:
                log(f"Max results: {max_results}")
            if dry_run:
                log("\n⚠️  DRY RUN MODE - No files will be created")
            log()

        # Create callbacks for progress reporting
        current_step = [0]  # Use list to allow mutation in nested function

        def progress_callback(update: ProgressUpdate):
            """Report progress updates."""
            if quiet or json_output:
                return

            # Only show step changes in non-verbose mode
            if update.step != current_step[0]:
                current_step[0] = update.step
                log(f"\n{update.message}")

            # Show detailed progress in verbose mode
            if verbose and update.total > 0:
                percent = int(update.percent)
                log(f"  Progress: {update.current}/{update.total} ({percent}%)")

        def status_callback(message: str):
            """Report status messages."""
            if verbose and not quiet and not json_output:
                log(f"  {message}")

        # Create export engine
        engine = ExportEngine(
            progress_callback=progress_callback,
            status_callback=status_callback
        )

        # Run export
        if not quiet and not json_output:
            log("Starting export...\n")

        result: ExportResult = engine.export(settings, dry_run=dry_run)

        # Handle results
        if json_output:
            # Machine-readable JSON output
            output = {
                "success": result.success,
                "files_created": result.files_created,
                "output_dir": str(result.output_dir),
                "duration_seconds": result.duration_seconds,
                "stats": result.stats,
                "errors": result.errors,
                "dry_run": dry_run,
                "exit_code": EXIT_SUCCESS if result.success else EXIT_EXPORT_ERROR,
            }
            print(json.dumps(output, indent=2))

        else:
            # Human-readable output
            if not quiet:
                log("\n" + "=" * 50)

                if result.success:
                    if dry_run:
                        log("✓ Dry run completed successfully!")
                        log("=" * 50)
                        log(f"Would export: {result.stats.get('emails_found', 0)} emails")
                        log(f"Output directory: {result.output_dir.absolute()}")
                        log("\nNo files were created (dry run mode)")
                    else:
                        log("✓ Export completed successfully!")
                        log("=" * 50)

                        # Show consolidation or individual file info
                        if result.stats.get("consolidation_mode"):
                            consolidated_file = result.stats.get("consolidation_filename", "export.md")
                            log(f"Consolidated document created: {consolidated_file}")
                        else:
                            log(f"Files created: {result.files_created}")

                        log(f"Output directory: {result.output_dir.absolute()}")

                        if result.errors:
                            log(f"\n⚠️  Warnings: {len(result.errors)} files had errors")

                        log("\nNext steps:")
                        log("1. Review the exported file(s) in the output directory")
                        log("2. Go to https://notebooklm.google.com/")
                        if result.stats.get("consolidation_mode"):
                            log("3. Create a notebook and upload the consolidated Markdown file as a source")
                        else:
                            log("3. Create a notebook and upload these Markdown files as sources")
                else:
                    log("✗ Export failed")
                    log("=" * 50)
                    if result.errors:
                        log(f"\nErrors:")
                        for error in result.errors[:5]:  # Show first 5 errors
                            log(f"  • {error}")
                        if len(result.errors) > 5:
                            log(f"  ... and {len(result.errors) - 5} more")

        # Exit with appropriate code
        if result.success:
            sys.exit(EXIT_SUCCESS)
        elif result.stats.get("emails_found") == 0:
            sys.exit(EXIT_NO_RESULTS)
        else:
            sys.exit(EXIT_EXPORT_ERROR)

    except KeyboardInterrupt:
        if json_output:
            print(json.dumps({"error": "Cancelled by user", "exit_code": EXIT_USER_CANCEL}))
        else:
            log("\n\nOperation cancelled by user.", err=True)
        sys.exit(EXIT_USER_CANCEL)

    except AuthenticationError as e:
        if json_output:
            print(json.dumps({"error": str(e), "exit_code": EXIT_AUTH_ERROR}))
        else:
            log(f"\n✗ Authentication failed: {e}", err=True)
            log("\nFor help with setup, see:", err=True)
            log("  • GETTING_HELP.md - Documentation guide", err=True)
            log("  • ADMIN_SETUP.md - Create your own credentials", err=True)
            log("  • Run: g2n --help-setup", err=True)
        sys.exit(EXIT_AUTH_ERROR)

    except GmailAPIError as e:
        if json_output:
            print(json.dumps({"error": str(e), "exit_code": EXIT_API_ERROR}))
        else:
            log(f"\n✗ Gmail API error: {e}", err=True)
        sys.exit(EXIT_API_ERROR)

    except Exception as e:
        if json_output:
            print(json.dumps({"error": str(e), "exit_code": EXIT_EXPORT_ERROR}))
        else:
            log(f"\n✗ Unexpected error: {e}", err=True)
            if verbose:
                import traceback
                traceback.print_exc()
        sys.exit(EXIT_EXPORT_ERROR)


if __name__ == "__main__":
    cli()
