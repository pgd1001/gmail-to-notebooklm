"""Command-line interface for Gmail to NotebookLM converter."""

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
from gmail_to_notebooklm.converter import MarkdownConverter, ConversionError
from gmail_to_notebooklm.gmail_client import GmailClient, GmailAPIError
from gmail_to_notebooklm.parser import EmailParser, EmailParseError
from gmail_to_notebooklm.utils import (
    create_filename,
    write_markdown_file,
    get_env_or_default,
    build_date_query,
    build_sender_query,
)


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
        # Load configuration
        try:
            cfg = load_config(config)
            if verbose or cfg.get("verbose", False):
                click.echo(f"Loaded configuration from: {cfg.config_path or 'defaults'}")
        except ConfigError as e:
            click.echo(f"✗ Configuration error: {e}", err=True)
            sys.exit(1)

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
        }
        settings = cfg.merge_with_cli_args(cli_args)

        # Extract settings
        label = settings.get("label")
        query = settings.get("query")
        after = settings.get("after")
        before = settings.get("before")
        from_ = settings.get("from")
        to = settings.get("to")
        exclude_from = settings.get("exclude_from")
        output_dir = settings.get("output_dir")
        max_results = settings.get("max_results")
        credentials = settings.get("credentials", "credentials.json")
        token = settings.get("token", "token.json")
        verbose = settings.get("verbose", False)
        overwrite = settings.get("overwrite", False)

        # Validate required fields
        if not label and not query and not after and not before and not from_ and not to:
            click.echo(
                "✗ Error: At least one filter is required: --label, --query, --after, --before, --from, or --to",
                err=True,
            )
            sys.exit(1)

        # Build date query if date filters provided
        try:
            date_query = build_date_query(after, before) if (after or before) else None
        except ValueError as e:
            click.echo(f"✗ Date validation error: {e}", err=True)
            sys.exit(1)

        # Build sender/recipient query if filters provided
        sender_query = (
            build_sender_query(from_, to, exclude_from)
            if (from_ or to or exclude_from)
            else None
        )

        # Combine all queries
        if date_query:
            if query:
                query = f"{query} {date_query}"
            else:
                query = date_query

        if sender_query:
            if query:
                query = f"{query} {sender_query}"
            else:
                query = sender_query

        # Determine output directory with fallback
        if output_dir is None:
            output_dir = get_env_or_default("GMAIL_TO_NBL_OUTPUT_DIR", "./output")

        output_path = Path(output_dir)

        if verbose:
            click.echo(f"Gmail to NotebookLM Converter v{__version__}")
            if label:
                click.echo(f"Label: {label}")
            if query:
                click.echo(f"Query: {query}")
            if after:
                click.echo(f"After: {after}")
            if before:
                click.echo(f"Before: {before}")
            click.echo(f"Output directory: {output_path}")
            if max_results:
                click.echo(f"Max results: {max_results}")
            click.echo()

        # Step 1: Authenticate
        click.echo("Step 1/5: Authenticating with Gmail...")
        try:
            creds = authenticate(credentials_path=credentials, token_path=token)
            click.echo("✓ Authentication successful")
        except AuthenticationError as e:
            click.echo(f"✗ Authentication failed: {e}", err=True)
            sys.exit(1)
        except FileNotFoundError as e:
            click.echo(f"✗ {e}", err=True)
            click.echo("\nSee OAUTH_SETUP.md for setup instructions.", err=True)
            sys.exit(1)

        # Step 2: Initialize Gmail client
        click.echo("\nStep 2/5: Connecting to Gmail API...")
        try:
            client = GmailClient(creds)
            click.echo("✓ Connected to Gmail API")
        except GmailAPIError as e:
            click.echo(f"✗ Failed to connect: {e}", err=True)
            sys.exit(1)

        # Step 3: Fetch emails
        if label and query:
            search_desc = f"label '{label}' with query: {query}"
        elif label:
            search_desc = f"label '{label}'"
        else:
            search_desc = f"query: {query}"

        click.echo(f"\nStep 3/5: Fetching emails from {search_desc}...")
        try:
            messages = client.get_messages_batch(label, max_results, query)
            if not messages:
                click.echo(f"No emails found matching {search_desc}")
                if label:
                    click.echo("\nTip: Label names are case-sensitive.")
                sys.exit(0)
            click.echo(f"✓ Found {len(messages)} email(s)")
        except GmailAPIError as e:
            click.echo(f"✗ Failed to fetch emails: {e}", err=True)
            sys.exit(1)

        # Step 4: Parse emails
        click.echo("\nStep 4/5: Parsing email content...")
        try:
            parser = EmailParser()
            parsed_emails = parser.parse_messages_batch(messages)
            click.echo(f"✓ Parsed {len(parsed_emails)} email(s)")
        except EmailParseError as e:
            click.echo(f"✗ Failed to parse emails: {e}", err=True)
            sys.exit(1)

        # Step 5: Convert to Markdown and save
        click.echo("\nStep 5/5: Converting to Markdown and saving...")
        try:
            converter = MarkdownConverter(include_headers=True, body_width=0)
            converted = converter.convert_emails_batch(parsed_emails)

            # Write files
            saved_count = 0
            for email_id, markdown_content in converted:
                # Find original email to get subject
                original = next(
                    (e for e in parsed_emails if e["id"] == email_id), None
                )
                if original:
                    subject = original.get("subject", "No Subject")
                else:
                    subject = "Unknown"

                # Create filename
                filename = create_filename(subject, email_id)

                # Write file
                try:
                    file_path = write_markdown_file(
                        output_path, filename, markdown_content, overwrite=overwrite
                    )
                    if verbose:
                        click.echo(f"  Saved: {file_path.name}")
                    saved_count += 1
                except Exception as e:
                    click.echo(
                        f"  Warning: Failed to save {filename}: {e}", err=True
                    )

            click.echo(f"✓ Saved {saved_count} Markdown file(s) to {output_path}")

        except ConversionError as e:
            click.echo(f"✗ Failed to convert emails: {e}", err=True)
            sys.exit(1)
        except Exception as e:
            click.echo(f"✗ Failed to save files: {e}", err=True)
            sys.exit(1)

        # Success summary
        click.echo("\n" + "=" * 50)
        click.echo("✓ Export completed successfully!")
        click.echo("=" * 50)
        click.echo(f"Emails exported: {saved_count}")
        click.echo(f"Output directory: {output_path.absolute()}")
        click.echo("\nNext steps:")
        click.echo("1. Review the Markdown files in the output directory")
        click.echo("2. Go to https://notebooklm.google.com/")
        click.echo("3. Create a notebook and upload these files as sources")

    except KeyboardInterrupt:
        click.echo("\n\nOperation cancelled by user.", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"\n✗ Unexpected error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    cli()
