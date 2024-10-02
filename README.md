# econ-raa
Reasearch Assistant Assistant is meant to be a tool to help improve productivity when working with Stata code bases.


## Architecture
The architecture of this tool will follow the one determined with ChatGPT here: https://chatgpt.com/share/66fb5246-3918-8006-b858-f232bba03aa8

The archticture will be expanded on in if the tool moves beyond the prototype stage


### Milestone 1
Milestone 1: Core Parsing and Analysis (Step 1.1)
    Goal: Build the parser that handles:
        Parsing of do files for:
            Global macros.
            Local macros and their usage.
            For and foreach loops (dependency unrolling).
            Dataset input/output tracking.
        Deliverable: A functional parser module that generates a dependency list from a folder of do files.
        Timeline: 2-3 weeks.