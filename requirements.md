## Product Requirements Document: Gmail Label to Markdown Converter for NotebookLM

**Product Name:** Email Archiver for NotebookLM (or similar)

**Version:** 1.1

**Date:** October 26, 2023

**Author:** [Your Name/Team]

---

### 1. Introduction

This document outlines the requirements for an internal tool designed to automate the conversion of specific Gmail emails into Markdown files, suitable for use as sources in Google NotebookLM. The tool will allow users to specify a Gmail label (typically client-specific) and convert all emails found under that label into `.md` files, which can then be easily uploaded to NotebookLM for knowledge management and analysis. **Crucially, the converted Markdown files will include key email header information to provide better context and categorization within NotebookLM.**

### 2. Goals

*   Enable staff to quickly convert client-specific email threads into NotebookLM sources.
*   Automate the extraction of email content and its conversion to a consistent Markdown format.
*   **Enhance the contextual understanding of converted emails within NotebookLM by including relevant header data.**
*   Reduce manual effort in preparing email archives for NotebookLM.

### 3. Key Features

#### 3.1. User Interface (Simple Command-Line or Basic GUI)

*   **Input Field:** A method for the user to input the desired Gmail label (e.g., "Client A", "Project X").
*   **Output Directory Selection (Optional but Recommended):** A method to specify where the generated Markdown files should be saved. If not specified, a default directory (e.g., `output/`) will be used.
*   **Start Button/Command:** A trigger to initiate the process.
*   **Status / Progress Display:** Show messages indicating authentication status, number of emails found, conversion progress, and completion status.

#### 3.2. Gmail API Integration & Authentication

*   **OAuth 2.0 Client Flow:** Implement a secure OAuth 2.0 flow for users to authenticate with their Google account and grant necessary permissions (read-only access to Gmail).
    *   The application should store refresh tokens securely (if persistent access is desired, otherwise re-authenticate each session).
*   **Gmail API Calls:**
    *   List messages (`users.messages.list`) based on the user-provided label.
    *   Fetch full message content (`users.messages.get` with `format='full'`).

#### 3.3. Email Content Extraction & Markdown Conversion

*   **MIME Parsing:** Efficiently parse the multipart MIME structure of fetched emails.
*   **Header Extraction:** Extract the following essential headers for contextualization:
    *   **From:** (Sender's Name and Email)
    *   **To:** (Recipient's Name and Email)
    *   **Cc:** (Carbon Copy Recipients' Names and Emails, if present)
    *   **Subject:** (Email Subject Line)
    *   **Date:** (Date and Time the email was sent)
*   **HTML Body Preference:** Prioritize extracting the HTML body of the email. If no HTML body is present, fall back to the plain text body.
*   **HTML to Markdown Conversion:** Convert the extracted HTML content into clean, readable Markdown.
    *   Preserve links, bolding, italics, lists, and basic formatting.
    *   Ignore email headers (From, To, Subject, Date) within the *original HTML body content itself*, focusing only on the actual message.
    *   Handle common HTML entities and clean up superfluous tags.
*   **Combined Markdown Output:** The final Markdown file should prepend the extracted header information **before** the converted email body. A suggested format for the header block within the Markdown file is:

    ```markdown
    ---
    From: [Sender Name <sender@example.com>]
    To: [Recipient Name <recipient@example.com>]
    Cc: [CC Name <cc@example.com>] (Optional)
    Date: [Full Date and Time]
    Subject: [Email Subject Line]
    ---

    [Converted Email Body in Markdown]
    ```

    *   Ensure a clear separator (like `---`) between the header block and the main body.

#### 3.4. File Output & Storage

*   **Local File System:** Save the generated Markdown files to the user's specified (or default) local directory.
*   **Encoding:** Ensure files are saved with UTF-8 encoding to support various characters.
*   **File Naming:** Generated `.md` files should be named descriptively. Recommended format: `[Sanitized_Subject_Line]_[Shortened_Email_ID].md`. The email ID can be truncated for readability.

### 4. Non-Functional Requirements

*   **Security:** Adhere to Google's OAuth 2.0 best practices for client authentication and token management. Do not store user credentials directly.
*   **Reliability:** Robust error handling for API failures, network issues, and malformed email content.
*   **Performance:** Efficiently process a moderate number of emails (e.g., hundreds) without significant delays.
*   **Maintainability:** Code should be well-structured, modular, and easy to understand.
*   **Usability:** Simple and intuitive interface for staff users.

### 5. Technical Stack (Suggested for AI Tool)

*   **Language:** Python
*   **Libraries:**
    *   `google-api-python-client`: For Gmail API interaction.
    *   `google-auth-oauthlib`: For OAuth 2.0 authentication.
    *   `beautifulsoup4` (or `lxml`): For HTML parsing.
    *   `html2text` (or `markdownify`): For HTML to Markdown conversion.
    *   **For GUI (if applicable):** `tkinter` (built-in) or `PyQt`/`PySide` (more robust). For CLI, standard input/output.

### 6. Out of Scope

*   AI-powered summarization or content extraction.
*   Direct integration with NotebookLM upload API (user will manually upload the generated files).
*   Two-way synchronization with Gmail (this is a one-way extraction tool).
*   Handling of email attachments (only body content and specified headers are converted).
*   Deletion or modification of emails in Gmail.

---

This revised PRD provides explicit instructions for extracting and formatting header information, making the output even more valuable for NotebookLM.