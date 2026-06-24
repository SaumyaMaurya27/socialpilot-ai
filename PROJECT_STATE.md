# SocialPilot AI - Project Context

## Hackathon

5-Day AI Agents: Intensive Vibe Coding Course With Google (Kaggle Capstone)

## Track

Concierge Agents

## Project Name

SocialPilot AI

## Project Goal

Build a multi-agent AI assistant that helps users create, review, and schedule social media content.

## Current Architecture

User
↓
Orchestrator Agent
↓
Trend Agent
↓
Writer Agent
↓
Safety Agent
↓
Scheduler Agent
↓
Calendar Tool (Mock)

## Completed Components

### Models

* TrendAgentInput
* TrendAgentOutput
* WriterAgentInput
* WriterAgentOutput
* SafetyAgentInput
* SafetyAgentOutput
* OrchestratorInput
* OrchestratorOutput

### Agents

* TrendAgent ✅
* WriterAgent ✅
* SafetyAgent ✅
* SchedulerAgent ✅
* OrchestratorAgent ✅

### Tools

* CalendarTool (Mock) ✅

### Safety Features

* Email detection
* Phone number detection
* API key detection
* Sensitive word detection
* Approve / Review / Reject workflow

### Tests Passing

* app.py
* test_orchestrator.py
* test_scheduler.py

## Current Working Flow

User Topic
↓
Trend Agent
↓
Generate Hashtags
Generate Trends
Generate Audience Keywords
↓
Writer Agent
↓
Generate LinkedIn Post


tree /f output
PS C:\Users\saumy\projects\SocialPilot AI\socialpilot-ai> tree /f
Folder PATH listing for volume ACER
Volume serial number is 000000DF 9467:634A
C:.
│   app.py
│   models.py
│   PROJECT_BRIEF.md
│   README.md
│   requirements.txt
│   test_orchestrator.py
│
├───agents
│   │   orchestrator_agent.py
│   │   safety_agent.py
│   │   scheduler_agent.py
│   │   trend_agent.py
│   │   writer_agent.py
│   │   __init__.py
│   │
│   └───__pycache__
│           orchestrator_agent.cpython-314.pyc
│           safety_agent.cpython-314.pyc
│           scheduler_agent.cpython-314.pyc
│           trend_agent.cpython-314.pyc
│           writer_agent.cpython-314.pyc
│           __init__.cpython-314.pyc
│
├───prompts
├───tests
│   │   test_orchestrator.py
│   │   test_scheduler.py
│   │   test_trend_agent.py
│   │   test_writer_agent.py
│   │   __init__.py
│   │
│   └───__pycache__
│           test_orchestrator.cpython-314.pyc
│           test_scheduler.cpython-314.pyc
│           __init__.cpython-314.pyc
│
│   │   calendar_tool.py
│   │   __init__.py
│   │
│   └───__pycache__
│           calendar_tool.cpython-314.pyc
│           __init__.cpython-314.pyc
│
└───__pycache__
        models.cpython-314.pyc      

