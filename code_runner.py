import subprocess
import tempfile
import os
import sys
from typing import Dict
import traceback
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def run_with_timeout(func, args=(), timeout_duration=5):
    """Run a function with timeout."""
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args)
        try:
            return future.result(timeout=timeout_duration)
        except TimeoutError:
            return {"success": False, "error": f"Code execution timed out ({timeout_duration} seconds limit)"}

def execute_python_code(code):
    """Execute Python code and return the output."""
    from io import StringIO
    import contextlib
    
    output_buffer = StringIO()
    with contextlib.redirect_stdout(output_buffer):
        with contextlib.redirect_stderr(output_buffer):
            # First compile to catch syntax errors
            compiled_code = compile(code, '<string>', 'exec')
            exec(compiled_code)
    
    return {"success": True, "output": output_buffer.getvalue()}

def check_code_syntax(code: str, language: str) -> Dict[str, any]:
    """Check code syntax without executing it."""
    if not code.strip():
        return {"success": False, "error": "Code cannot be empty"}
    
    try:
        if language == "python":
            try:
                # First try to compile the code to check syntax
                compile(code, '<string>', 'exec')
                return {"success": True, "message": "Syntax is correct"}
            except SyntaxError as e:
                return {
                    "success": False,
                    "error": f"Line {e.lineno}: {str(e)}"
                }
            
        elif language == "c++":
            with tempfile.NamedTemporaryFile(suffix='.cpp', mode='w', delete=False, encoding='utf-8') as f:
                f.write(code)
                temp_path = f.name
            
            try:
                # Only compile, don't link
                result = subprocess.run(
                    ['g++', '-fsyntax-only', temp_path],
                    capture_output=True,
                    text=True
                )
                os.unlink(temp_path)
                
                if result.returncode != 0:
                    return {"success": False, "error": result.stderr}
                return {"success": True, "message": "Syntax is correct"}
            except FileNotFoundError:
                return {"success": False, "error": "C++ compiler (g++) not found. Please install g++."}
            
        elif language == "java":
            # Extract class name from code
            import re
            class_match = re.search(r'public\s+class\s+(\w+)', code)
            if not class_match:
                return {"success": False, "error": "No public class found. Java code must contain a public class."}
            
            class_name = class_match.group(1)
            with tempfile.NamedTemporaryFile(suffix='.java', mode='w', delete=False, encoding='utf-8') as f:
                f.write(code)
                temp_path = f.name
            
            try:
                # Only compile
                result = subprocess.run(
                    ['javac', temp_path],
                    capture_output=True,
                    text=True
                )
                
                # Clean up
                os.unlink(temp_path)
                class_file = os.path.join(os.path.dirname(temp_path), f"{class_name}.class")
                if os.path.exists(class_file):
                    os.unlink(class_file)
                
                if result.returncode != 0:
                    return {"success": False, "error": result.stderr}
                return {"success": True, "message": "Syntax is correct"}
            except FileNotFoundError:
                return {"success": False, "error": "Java compiler (javac) not found. Please install JDK."}
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error checking syntax: {str(e)}\n{traceback.format_exc()}"
        }

def execute_code(code: str, language: str) -> Dict[str, any]:
    """Execute code and return the output."""
    if not code.strip():
        return {"success": False, "error": "Code cannot be empty"}
    
    try:
        if language == "python":
            try:
                return run_with_timeout(execute_python_code, (code,), 5)
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Runtime Error: {str(e)}"
                }
            
        elif language == "c++":
            with tempfile.NamedTemporaryFile(suffix='.cpp', mode='w', delete=False, encoding='utf-8') as f:
                f.write(code)
                cpp_path = f.name
            
            try:
                # Compile with timeout
                try:
                    exe_path = cpp_path[:-4] + ('.exe' if sys.platform == 'win32' else '')
                    compile_process = subprocess.run(
                        ['g++', cpp_path, '-o', exe_path],
                        capture_output=True,
                        text=True,
                        timeout=10  # 10 second timeout for compilation
                    )
                    
                    if compile_process.returncode != 0:
                        os.unlink(cpp_path)
                        return {"success": False, "error": f"Compilation Error:\n{compile_process.stderr}"}
                    
                    # Execute with timeout
                    try:
                        result = subprocess.run(
                            [exe_path],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        
                        output = result.stdout
                        if result.stderr:
                            output += f"\nErrors:\n{result.stderr}"
                        
                        return {
                            "success": True,
                            "output": output if output.strip() else "Program executed successfully (no output)"
                        }
                    except subprocess.TimeoutExpired:
                        return {"success": False, "error": "Program execution timed out (5 seconds limit)"}
                    finally:
                        # Cleanup
                        if os.path.exists(cpp_path):
                            os.unlink(cpp_path)
                        if os.path.exists(exe_path):
                            os.unlink(exe_path)
                except subprocess.TimeoutExpired:
                    return {"success": False, "error": "Compilation timed out (10 seconds limit)"}
            except FileNotFoundError:
                return {"success": False, "error": "C++ compiler (g++) not found. Please install g++."}
            
        elif language == "java":
            # Extract class name from code
            import re
            class_match = re.search(r'public\s+class\s+(\w+)', code)
            if not class_match:
                return {"success": False, "error": "No public class found. Java code must contain a public class."}
            
            class_name = class_match.group(1)
            with tempfile.NamedTemporaryFile(suffix='.java', mode='w', delete=False, encoding='utf-8') as f:
                f.write(code)
                java_path = f.name
            
            try:
                # Compile
                compile_result = subprocess.run(
                    ['javac', java_path],
                    capture_output=True,
                    text=True
                )
                
                if compile_result.returncode != 0:
                    os.unlink(java_path)
                    return {"success": False, "error": f"Compilation Error:\n{compile_result.stderr}"}
                
                # Execute
                try:
                    result = subprocess.run(
                        ['java', '-cp', os.path.dirname(java_path), class_name],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    output = result.stdout
                    if result.stderr:
                        output += f"\nErrors:\n{result.stderr}"
                    
                    return {
                        "success": True,
                        "output": output if output else "Program executed successfully (no output)"
                    }
                except subprocess.TimeoutExpired:
                    return {"success": False, "error": "Program execution timed out (5 seconds limit)"}
                finally:
                    # Cleanup
                    os.unlink(java_path)
                    class_file = os.path.join(os.path.dirname(java_path), f"{class_name}.class")
                    if os.path.exists(class_file):
                        os.unlink(class_file)
            except FileNotFoundError:
                return {"success": False, "error": "Java compiler (javac) not found. Please install JDK."}
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error executing code: {str(e)}"
        } 