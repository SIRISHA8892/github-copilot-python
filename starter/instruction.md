# GitHub Copilot Instructions

## Project Goal
Refactor the legacy Flask Sudoku application into a clean, modern, maintainable application while preserving existing functionality.

## Coding Standards
- Keep the existing project structure unless a change improves maintainability.
- Write clean, readable, and well-commented Python, JavaScript, HTML, and CSS.
- Prefer reusable functions over duplicated code.
- Do not remove existing features unless requested.
- Preserve backward compatibility.
- Use meaningful variable and function names.
- Keep code modular and easy to understand.

## Styling
- Maintain a responsive layout.
- Support both Light Mode and Dark Mode.
- Ensure text remains readable in all themes.
- Alternate the background colors of the 3×3 Sudoku blocks.

## Game Features
Implement features incrementally without breaking existing functionality:
- Difficulty selector
- Timer
- Hint button
- Check button
- Immediate invalid move highlighting
- Unique Sudoku solution validation
- Player name prompt after completion
- Top 10 leaderboard using Local Storage

## Testing
- Suggest tests before implementing major features.
- Avoid changing unrelated files.
- Explain significant code changes when requested.

## Copilot Behavior
- Make focused changes for one feature at a time.
- Avoid large refactors unless explicitly requested.
- Preserve existing functionality while adding new features.