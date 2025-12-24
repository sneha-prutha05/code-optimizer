import re

def analyze_code(code):
    lines = code.split('\n')
    loop_count = 0
    recursion_detected = False
    inefficient_patterns = []
    suggestion_parts = []

    # Detect loops
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('for ') or stripped.startswith('while '):
            loop_count += 1

    # Detect recursion
    function_defs = re.findall(r'def\s+(\w+)\s*', code)
    for func in function_defs:
        pattern = r'\b' + re.escape(func) + r'\s*'
        if re.search(pattern, code.split(f'def {func}')[1]):
            recursion_detected = True
            inefficient_patterns.append("Recursive function without memoization")
            break

    # Inefficient patterns detection
    if '.insert(0' in code or '.pop(0' in code:
        inefficient_patterns.append("Using .insert(0, ...) or .pop(0) on lists (inefficient in Python)")

    if 'for' in code and 'sort(' in code:
        inefficient_patterns.append("Repeated sorting inside loops")

    if 'for' in code and 'in ' in code and ('set' not in code and 'dict' not in code):
        inefficient_patterns.append("Repeated linear search in a list – use set or dict for faster lookup")

    if re.search(r'\+\s*=\s*".*"', code):
        inefficient_patterns.append("String concatenation in loop – use join() instead")

    if re.search(r'for.*for.*for', code):
        inefficient_patterns.append("Triple nested loops (O(n³)) – very inefficient")

    if re.findall(r'list.*', code):
        inefficient_patterns.append("Repeated list creation in loops – avoid recreating objects")

    # Bracket balance check using stack (DSA: Stack)
    def are_brackets_balanced(code_str):
        stack = []
        opening = "([{"
        closing = ")]}"
        pair = {')': '(', ']': '[', '}': '{'}

        for char in code_str:
            if char in opening:
                stack.append(char)
            elif char in closing:
                if not stack or stack[-1] != pair[char]:
                    return False
                stack.pop()
        return len(stack) == 0

    brackets_balanced = are_brackets_balanced(code)

    # Time complexity estimate
    if recursion_detected:
        complexity = "O(2ⁿ) or higher (recursion)"
    elif loop_count == 0:
        complexity = "O(1)"
    elif loop_count == 1:
        complexity = "O(n)"
    elif loop_count == 2:
        complexity = "O(n²)"
    elif loop_count == 3:
        complexity = "O(n³)"
    elif loop_count == 4:
        complexity = "O(n⁴)"
    else:
        complexity = f"O(n^{loop_count})"

    # Suggestions text
    if not brackets_balanced:
        suggestion_parts.append("Unbalanced brackets detected – check for missing parentheses or braces.")

    if inefficient_patterns:
        suggestion_parts.extend(inefficient_patterns)
    elif brackets_balanced:
        suggestion_parts.append("Your code looks efficient for basic use cases.")

    suggestion_text = " | ".join(suggestion_parts)

    return {
        "loops": loop_count,
        "recursion": recursion_detected,
        "complexity": complexity,
        "brackets_balanced": brackets_balanced,
        "suggestion": suggestion_text
    }