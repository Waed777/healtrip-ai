# HealTrip AI — Patient Decision Assistant

HealTrip AI is a prototype AI-powered patient decision assistant designed
to help users identify an appropriate next healthcare step.

The system does not diagnose medical conditions.

## Problem

Patients may not know whether they should:

- seek urgent medical evaluation
- consult a specialist
- visit a hospital
- seek a second opinion
- provide additional information before deciding

HealTrip AI uses an AI agent, safety rules, and verified database tools
to support this decision-making process.

## Architecture

```text
Patient
   |
   v
Streamlit Chat UI
   |
   v
Safety Layer
   |
   v
AI Agent
   |
   +----------------------+
   |                      |
   v                      v
Doctor Search Tool    Hospital Search Tool
   |                      |
   +----------+-----------+
              |
              v
        SQLite Database
              |
              v
       Verified Results
              |
              v
         AI Response
