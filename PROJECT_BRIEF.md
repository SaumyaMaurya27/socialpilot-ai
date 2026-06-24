# SocialPilot AI - MVP

## Goal

Build a multi-agent social media assistant that helps users create and schedule social media content.

## User Flow

User enters:

"I launched an AI Resume Analyzer project today."

The system:

1. Researches relevant trends and hashtags
2. Generates a LinkedIn post
3. Reviews the content for safety
4. Requests user approval
5. Schedules the post in Google Calendar

## Agents

### Orchestrator Agent

Responsibilities:

* Receive user request
* Call Trend Agent
* Call Writer Agent
* Call Safety Agent
* Return final result

### Trend Agent

Responsibilities:

* Generate hashtags
* Suggest trending topics
* Suggest audience keywords

Output:

* hashtags
* trends

### Writer Agent

Responsibilities:

* Generate LinkedIn post
* Generate call-to-action

Output:

* post content

### Safety Agent

Responsibilities:

* Detect email addresses
* Detect phone numbers
* Detect API keys
* Detect sensitive information

Output:

* safety report
* approval recommendation

## MCP Integration

Google Calendar MCP

Purpose:
Create calendar event for scheduled posting.

## Success Criteria

A user can:

✓ Enter a topic

✓ Generate hashtags

✓ Generate LinkedIn content

✓ Pass safety review

✓ Approve content

✓ Create calendar event
