# Plan: ydk-parser

## Goal
Create a Python script that parses a `.ydk` file into structured data, organised into the three deck sections found in the file: `main`, `extra`, and `side`.

## Files to Create
| File | Location |
|------|----------|
| `parse-ydk-file.py` | repo root |

## Sample `.ydk` file format (from `sample-ydk-files/Mitsurugi.ydk`)
```
#main
13332685
19899073
...
#extra
6983839
46772449
...
!side
76948970
84192580
...
```
- Section headers may have leading or trailing spaces
- Each card is represented by a numeric ID on its own line
- Sections always appear in the order: `#main`, `#extra`, `!side`
- Any of the three sections may be absent or empty — the script should handle this without erroring

## Return value
`process_ydk_data` returns a plain Python dictionary with three keys:
```python
{"main": [], "extra": [], "side": []}
```
Each value is a list of integers (card IDs).

## Script structure
1. Any necessary imports
2. The `process_ydk_data(ydk_data)` function
3. Working code below the function that demonstrates it works

## `process_ydk_data(ydk_data)` function

### Argument
- `ydk_data` — a string containing the full contents of a `.ydk` file

### Parsing logic
- Split `ydk_data` into individual lines
- Use a variable to track which section is currently being read (`"main"`, `"extra"`, `"side"`, or `None`)
- Iterate over lines one at a time:
  - If a line contains `#main`, switch section to `"main"` and continue to next line
  - If a line contains `#extra`, switch section to `"extra"` and continue to next line
  - If a line contains `!side`, switch section to `"side"` and continue to next line
  - Otherwise, if the line is not empty and section is set, parse the line as an integer and append to the appropriate list
- Return the dictionary

### Implementation notes
- Use separate loops (one per section) is acceptable — clarity over conciseness
- Favour breaking logic into separate named variables rather than chaining calls (e.g. strip a line into a variable before parsing it as an int)
- No error handling required
- Use built-in Python only — no imports needed beyond what the logic requires

## Working code (below the function)
- Open `sample-ydk-files/Mitsurugi.ydk` for reading
- Read the file contents into a variable
- Pass the contents to `process_ydk_data()`
- Assign the result to a variable called `deck`
- Print `deck["main"]`, `deck["extra"]`, and `deck["side"]`

## Code style
- Simple and readable — appropriate for a 17-year-old CS pupil
- No classes, no error handling, no abstractions beyond the single function
- Repetition is acceptable in favour of clarity
- Assign intermediate variables rather than chaining calls inline
- Ensure the code does not look AI-generated
